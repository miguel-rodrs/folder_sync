import argparse
import os
import time
import glob
import shutil
import logging
from log_system import create_log

DEFAULT_SOURCE_PATH = r"./src_path"
DEFAULT_REPLICA_PATH = r"./rep_path"
DEFAULT_LOG_PATH = r"./log.log"
DEFAULT_INTERVAL = "60"

SOURCE_HELP_MSG = ("File path to the source folder. The path can be relative or absolute. This argument is optional "
                   "and the default path is '{}'.".format(DEFAULT_SOURCE_PATH))
REPLICA_HELP_MSG = ("File path to the replica folder. The path can be relative or absolute. This argument is optional "
                    "and the default path is '{}'.".format(DEFAULT_REPLICA_PATH))
LOG_PATH_HELP_MSG = ("Path where the log will be created and written. The path can be relative or absolute. This "
                     "argument is optional and the default path is '{}'.".format(DEFAULT_LOG_PATH))
INTERVAL_HELP_MSG = ("Interval between each synchronization in seconds. This argument is optional and the default "
                     "interval is '{}' seconds.".format(DEFAULT_INTERVAL))

REMOVE_DIR_MSG = "Removing: '{}' and all it's contents"
REMOVE_FILE_MSG = "Removing: '{}'"
COPY_MSG = "Copying '{}' to '{}'"
SUCCESS_MSG = "Successful operation."

def arg_parse():
    """Parses the arguments to the script and returns all the args."""
    parser = argparse.ArgumentParser(
        prog='SyncDir',
        description='This script synchronizes 2 directories, one of them being the source folder and the other one '
                    'being the replica folder using an interval between each synchronization and logging every '
                    'operation to a log file.')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-s', '--source', help=SOURCE_HELP_MSG)
    parser.add_argument('-r', '--replica', help=REPLICA_HELP_MSG)
    parser.add_argument('-l', '--log', help=LOG_PATH_HELP_MSG)
    parser.add_argument('-i', '--interval', help=INTERVAL_HELP_MSG)

    args = parser.parse_args()
    return args


def get_all_paths(root_path):
    res = glob.glob(root_path + "\\**", recursive=True)
    res = [os.path.relpath(path, root_path) for path in res]
    return res[1:]  # Removes the '.' path


def sync_dirs(src, rep):
    logging.debug("Initiating synchronization")
    paths_src = get_all_paths(src)
    paths_rep = get_all_paths(rep)
    for path in paths_src:
        abs_path_src = os.path.join(src, path)
        if path in paths_rep:
            abs_path_rep = os.path.join(rep, path)
            stat_src = os.stat(abs_path_src)
            stat_rep = os.stat(abs_path_rep)
            if not (stat_src.st_size == stat_rep.st_size and stat_src.st_mtime_ns == stat_rep.st_mtime_ns):
                if os.path.isfile(abs_path_rep):
                    logging.info(REMOVE_FILE_MSG.format(abs_path_rep))
                    os.remove(abs_path_rep)
                else:
                    logging.info(REMOVE_DIR_MSG.format(abs_path_rep))
                    shutil.rmtree(abs_path_rep)
                abs_path_rep = os.path.split(abs_path_rep)[0]
                logging.info(COPY_MSG.format(abs_path_src, abs_path_rep))
                if os.path.isfile(abs_path_src):
                    shutil.copy2(abs_path_src, abs_path_rep)
                else:
                    shutil.copytree(abs_path_src, abs_path_rep)
                logging.info(SUCCESS_MSG)
        else:
            abs_path_rep = os.path.join(rep, path)
            logging.info(COPY_MSG.format(abs_path_src, abs_path_rep))
            if os.path.isfile(abs_path_src):
                shutil.copy2(abs_path_src, abs_path_rep)
                paths_rep.append(path)
            else:
                shutil.copytree(abs_path_src, abs_path_rep)
                paths_rep = get_all_paths(rep)
            logging.info(SUCCESS_MSG)
    paths_src = get_all_paths(src)
    paths_rep = get_all_paths(rep)
    diff = [p for p in paths_rep if p not in paths_src]
    for path in diff:
        abs_path = os.path.join(rep, path)
        if os.path.isfile(abs_path):
            logging.info(REMOVE_FILE_MSG.format(abs_path))
            os.remove(abs_path)
        else:
            logging.info(REMOVE_DIR_MSG.format(abs_path))
            shutil.rmtree(abs_path)
            rem = [temp for temp in diff if temp.startswith(path + "\\")]
            for item in rem:
                diff.remove(item)
        logging.info(SUCCESS_MSG)


def main():
    args = arg_parse()

    source = os.path.abspath(DEFAULT_SOURCE_PATH if not args.source else args.source)
    replica = os.path.abspath(DEFAULT_REPLICA_PATH if not args.replica else args.replica)
    log = os.path.abspath(DEFAULT_LOG_PATH if not args.log else args.log)
    interval = int(DEFAULT_INTERVAL if not args.interval else args.interval)

    create_log(log)

    if not os.path.exists(source):
        os.mkdir(source)

    if not os.path.exists(replica):
        os.mkdir(replica)

    while True:
        sync_dirs(source, replica)
        logging.debug("Synchronization done. Entering sleep mode for " + str(interval) + " seconds.")
        time.sleep(interval)
    pass


if __name__ == "__main__":
    main()
