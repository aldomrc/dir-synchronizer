import os
import time
import logging
import argparse
import hashlib
import shutil

def rm_dirs(path):
    paths_replica = os.listdir(path)
    for path in paths_replica:
        full_path_rep = os.path.join(replica, path)
        # for files
        if os.path.isfile(full_path_rep):
            os.remove(full_path_rep)
            log_msg = f'{full_path_rep}: file removed.'
            logging.info(log_msg)
            print(log_msg)
        # for directories
        elif os.path.isdir(full_path_rep):
            rm_dirs(full_path_rep)
            log_msg = f"{full_path_rep} directory removed."
            logging.info(log_msg)
            print(log_msg)

# compare file content MD5 hash
def cmp_file(f1, f2):
    return cmp_file_hash(f1, f2)

def cmp_file_hash(ff1, ff2):
    with open(ff1, "rb") as f1, open(ff2, "rb") as f2:
        return hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()

# simpler file comparison over date last modified - not used
def cmp_file_mtime(f1, f2):
    return os.path.getmtime(f1) == os.path.getmtime(f2)

def cmp_dirs(source, replica):
    # queue used to search nested directories breadth first
    dirs_queue = ['']
    while dirs_queue != []:
        paths_source = os.listdir(os.path.join(source, dirs_queue[0]))
        paths_replica = os.listdir(os.path.join(replica, dirs_queue[0]))
        for path in paths_source:
            full_path_src = os.path.join(source, os.path.join(dirs_queue[0], path)) 
            full_path_rep = os.path.join(replica, os.path.join(dirs_queue[0], path)) 
            # for files
            if os.path.isfile(full_path_src):
                if path in paths_replica:
                    # if different file, remove replica file and copy from source
                    if not cmp_file(full_path_src, full_path_rep):
                        os.remove(full_path_rep)
                        shutil.copy2(full_path_src, full_path_rep)
                        log_msg = f'{full_path_rep}: file updated.'
                        logging.info(log_msg)
                        print(log_msg)
                    # if files match, ignore
                else:
                    shutil.copy2(full_path_src, full_path_rep)
                    log_msg = f'{full_path_rep}: file created.'
                    logging.info(log_msg)
                    print(log_msg)
            # for directories
            elif os.path.isdir(full_path_src):
                dirs_queue.append(os.path.join(dirs_queue[0], path))
                if path not in paths_replica:
                    os.makedirs(full_path_rep)
                    logging.info(f'{full_path_rep}: directory created')
        dirs_queue.pop(0)

    dirs_queue = ['']

    while dirs_queue != []:
        # loop checks for files in replica that should be removed
        paths_source = os.listdir(os.path.join(source, dirs_queue[0]))
        paths_replica = os.listdir(os.path.join(replica, dirs_queue[0]))
        for path in paths_replica:
            full_path_src = os.path.join(source, os.path.join(dirs_queue[0], path)) 
            full_path_rep = os.path.join(replica, os.path.join(dirs_queue[0], path)) 
            # for files
            if os.path.isfile(full_path_rep):
                if path not in paths_source:
                    os.remove(full_path_rep)
                    log_msg = f'{full_path_rep}: file removed.'
                    logging.info(log_msg)
                    print(log_msg)
            # for directories
            elif os.path.isdir(full_path_rep):
                if path not in paths_source:
                    rm_dirs(full_path_rep)
                    print(f'Removing {full_path_rep}')
                    log_msg = f"{full_path_rep} directory removed."
                    logging.info(log_msg)
                    print(log_msg)
                else:
                    dirs_queue.append(os.path.join(dirs_queue[0], path))
        dirs_queue.pop(0)

    return 0

def synch_dirs(source, replica, interval):
    if not os.path.isdir(source):
        raise argparse.ArgumentError(None, 'Source directory not found.')
    if not os.path.isdir(replica):
        os.makedirs(replica)
    
    logging.info(f'Directory synchronization params: \
                 \n\tsource:   {source} \
                 \n\treplica:  {replica} \
                 \n\tinterval: {interval}')
    
    while True:
        try:
            logging.info('Syncing directories...')
            print('Syncing directories...')
            cmp_dirs(source, replica)
            logging.info('Sync over.')
            print('Sync over.')
            time.sleep(interval)
        except KeyboardInterrupt:
            logging.info('System Exit.')
            print('System Exit.')
            raise SystemExit

if __name__ == '__main__': 
    parser = argparse.ArgumentParser('dir_synchronizer')
    parser.add_argument('source', help='Source directory to be replicated', type=str)
    parser.add_argument('replica', help='Replica of the source directory', type=str)
    parser.add_argument('--log', default='sync.log', help='Path to log file', type=str)
    parser.add_argument('--interval', default=60, help='Interval for periodic directory synchronization', type=int)

    args = parser.parse_args()
    source = args.source
    replica = args.replica
    logs = args.log
    interval = args.interval

    logging.basicConfig(filename=logs, level=logging.INFO,
                        format='%(asctime)s [%(levelname)s]: %(message)s')
    logging.info(f'Running!')
    synch_dirs(source, replica, interval)
