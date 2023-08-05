import copy
import sys
import time
import multiprocessing as mp
import queue
from . import clouds
from .conf import get_aws_config
from . import db
from . import errors
from . import fileio
from . import particleops
from . import util

try:
    import mkl
    mkl.set_num_threads(1)
except ImportError:
    pass

# Stop sentinel value for queues
stop = 'STOP'
# Quantile list
quantiles = [2.5, 50, 97.5]
# Max OPP in queue, for backpressure if writing is slow
max_opp = 100

@util.quiet_keyboardinterrupt
def filter_evt_files(files, dbpath, opp_dir, s3=False, worker_count=1,
                     every=10.0):
    """Filter a list of EVT files.

    Positional arguments:
        files - paths to EVT files to filter
        dbpath = SQLite3 db path
        opp_dir = Directory for output binary OPP files

    Keyword arguments:
        s3 - Get EVT data from S3
        worker_count - number of worker processes to use
        every - Percent progress output resolution
    """
    work = {
        "file": None,  # fill in later
        "s3": s3,
        "cloud_config_items": None,
        "dbpath": dbpath,
        "opp_dir": opp_dir,
        "filter_params": None  # fill in later from db
    }

    if not dbpath:
        raise ValueError("Must provide db path to filter_evt_files()")
    if worker_count < 1:
        raise ValueError("worker_count must be > 0")
    if every <= 0 or every > 100:
        raise ValueError("resolution must be > 0 and <= 100")

    worker_count = min(len(files), worker_count)

    work["filter_params"] = db.get_latest_filter(dbpath)

    if s3:
        aws_config = get_aws_config(s3_only=True)
        work["cloud_config_items"] = aws_config.items("aws")

    # Create input queue with info necessary to filter one file
    work_q = mp.Queue()
    # Create output queues
    stats_q = mp.Queue()  # result stats
    opps_q = mp.Queue(max_opp)   # OPP data
    done_q = mp.Queue()   # signal we're done to main thread

    # Create worker processes
    workers = []
    for _ in range(worker_count):
        p = mp.Process(target=do_filter, args=(work_q, opps_q))
        p.start()
        workers.append(p)

    # Create db output process
    saver = mp.Process(
        target=do_save,
        args=(opps_q, stats_q, len(files))
    )
    saver.start()

    # Create reporting process
    reporter = mp.Process(
        target=do_reporting,
        args=(stats_q, done_q, len(files), every)
    )
    reporter.start()

    # Add work to the work queue
    for f in files:
        work_copy = copy.copy(work)
        work_copy["file"] = f
        work_q.put(work_copy)
    # Put sentinel stop values on the input queue, one for each consumer process
    for _ in range(worker_count):
        work_q.put(stop)

    try:
        # Wait for reporter to tell us we're done
        done = done_q.get()
        if done is not None:
            # Something went wrong, shut child processes down
            print(done, file=sys.stderr)
    finally:
        for w in workers:
            w.terminate()
            w.join()
        saver.terminate()
        saver.join()
        reporter.join()


@util.quiet_keyboardinterrupt
def do_filter(work_q, opps_q):
    """Filter one EVT file, save to sqlite3, return filter stats"""
    work = work_q.get()
    while work != stop:
        work["error"] = ""
        work["all_count"] = 0
        work["evt_count"] = 0
        work["opp"] = None

        evt_file = work["file"]
        fileobj = None

        try:
            if work["s3"]:
                cloud = clouds.AWS(work["cloud_config_items"])
                fileobj = cloud.download_file_memory(evt_file)
            evt_df = fileio.read_evt_labview(path=evt_file, fileobj=fileobj)
        except errors.FileError as e:
            work["error"] = f"Could not parse file {evt_file}: {e}"
            evt_df = particleops.empty_df()
        except Exception as e:
            work["error"] = f"Unexpected error when parsing file {evt_file}: {e}"
            evt_df = particleops.empty_df()

        try:
            evt_df = particleops.mark_focused(evt_df, work["filter_params"])
            work["all_count"] = len(evt_df.index)
            work["noise_count"] = len(evt_df[evt_df["noise"]].index)
            work["saturated_count"] = len(evt_df[evt_df["saturated"]].index)
            work["opp"] = particleops.select_focused(evt_df)
        except Exception as e:
            work["error"] = f"Unexpected error when selecting focused partiles in file {evt_file}: {e}"
        # Write to OPP file if all quantiles have focused data. Would like to
        # write in a different process (do_save) but this quickly becomes a
        # significant bottleneck.
        try:
            if work["opp_dir"]:
                fileio.write_opp_labview(work["opp"], work["file"], work["opp_dir"])
        except Exception as e:
            work["error"] = f"Unexpected error when saving file {evt_file}: {e}"

        opps_q.put(work)
        work = work_q.get()


@util.quiet_keyboardinterrupt
def do_save(opps_q, stats_q, files_left):
    while files_left > 0:
        try:
            work = opps_q.get(True, 60)  # We should get one file every minute at least
        except queue.Empty as e:
            stats_q.put("EMPTY QUEUE")
            break
        except Exception:
            stats_q.put("QUEUE ERROR")
            break

        files_left -= 1

        try:
            # Save to DB
            if work["dbpath"]:
                filter_id = work["filter_params"]["id"].unique().tolist()[0]
                db.save_opp_to_db(work["file"], work["opp"], work["all_count"],
                                  work["all_count"] - work["noise_count"],
                                  filter_id, work["dbpath"])
                db.save_outlier(work["file"], 0, work["dbpath"])
        except Exception as e:
            work["error"] = "Unexpected error when saving file {} to db: {}".format(work["file"], e)

        stats_q.put(work)


@util.quiet_keyboardinterrupt
def do_reporting(stats_q, done_q, file_count, every):
    event_count = 0
    noise_count = 0
    signal_count = 0
    saturated_count = 0
    opp_count = 0
    files_ok = 0

    print("")
    print(f"Filtering {file_count} EVT files. Progress for 50th quantile every ~ {every}%")

    t0 = time.time()

    last = 0  # Last progress milestone in increments of every
    event_count_block = 0  # EVT particles in this block (between milestones)
    noise_count_block = 0  # EVT noise particles in this block
    signal_count_block = 0  # EVT signal (not noise) particles in this block
    saturated_count_block = 0  # particles saturating D1 or D2
    opp_count_block = 0  # OPP particles in this block
    files_seen = 0

    # Filter particles in parallel with process pool
    for i in range(file_count):
        work = stats_q.get()  # get next result

        if work in ("EMPTY QUEUE", "QUEUE ERROR"):
            # Something went wrong upstream, exit with an error message
            done_q.put(f"A fatal error occurred after filtering {files_seen}/{file_count} files: {work}")
            sys.exit(1)

        files_seen += 1

        if work["error"]:
            print(work["error"], file=sys.stderr)
        else:
            files_ok += 1

        opp = work["opp"]
        # only consider 50% quantile for reporting
        opp = opp[opp["q50"]]
        event_count_block += work["all_count"]
        noise_count_block += work["noise_count"]
        signal_count_block = event_count_block - noise_count_block
        saturated_count_block += work["saturated_count"]
        opp_count_block += len(opp.index)

        # Print progress periodically
        perc = float(i + 1) / file_count * 100  # Percent completed
        # Round down to closest every%
        milestone = int(perc / every) * every
        if milestone > last:
            event_count += event_count_block
            noise_count += noise_count_block
            signal_count += signal_count_block
            saturated_count += saturated_count_block
            opp_count += opp_count_block
            ratio_noise_block = util.zerodiv(noise_count_block, event_count_block)
            ratio_saturated_block = util.zerodiv(saturated_count_block, event_count_block)
            ratio_evtopp_block = util.zerodiv(opp_count_block, signal_count_block)
            msg = f"File: {i + 1}/{file_count} {perc:5.4}%"
            msg += " events: %d noise: %d (%.04f) sat: %d (%.04f) opp: %d (%.04f) t: %.2fs" % \
                (
                    event_count_block,
                    noise_count_block, ratio_noise_block,
                    saturated_count_block, ratio_saturated_block,
                    opp_count_block, ratio_evtopp_block,
                    time.time() - t0
                )
            print(msg)
            sys.stdout.flush()
            last = milestone
            event_count_block = 0
            noise_count_block = 0
            signal_count_block = 0
            saturated_count_block = 0
            opp_count_block = 0

    # If any particle count data is left, add it to totals
    event_count += event_count_block
    noise_count += noise_count_block
    signal_count += signal_count_block
    saturated_count += saturated_count_block
    opp_count += opp_count_block

    ratio_noise = util.zerodiv(noise_count, event_count)
    ratio_saturated = util.zerodiv(saturated_count, event_count)
    ratio_evtopp = util.zerodiv(opp_count, signal_count)

    summary_text = "Total events: %d noise: %d (%.04f) sat: %d (%.04f) opp: %d (%.04f) t: %.2fs" % \
        (
            event_count,
            noise_count, ratio_noise,
            saturated_count, ratio_saturated,
            opp_count, ratio_evtopp,
            time.time() - t0
        )
    print(summary_text)
    print(f"{files_ok} / {file_count} EVT files parsed successfully")
    done_q.put(None)
