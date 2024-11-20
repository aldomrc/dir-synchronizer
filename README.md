# Directory Synchronizer

This Python script provides a simple solution for one way synchronation between a source and a replica directory.
It ensures that changes in the source directory are mirrored in the replica directory at regular, user-defined intervals.

## Features

- Synchronizes files and subdirectories from a source to a replica directory.
- Ensures updated files are copied, new files/directories are created, and removed files/directories in the source are deleted from the replica.
- Compares files using MD5 hashes to detect changes.
- Supports periodic synchronization with user-defined intervals.
- Generates logs for synchronization operations; create, update and remove.

## Requirements

- Python 3.x
- Libraries: `os`, `time`, `logging`, `argparse`, `hashlib`, `shutil`

## Installation

Clone or download this repository to your local machine.

## Usage

```bash
python dir_synch.py source replica [--log LOG] [--interval INTERVAL]
```

The script requires the following arguments:
- source: Path to the source directory to be replicated. Must be a valid path to an existing directory.
- replica: Path to the target replica directory. Will be created if it doesn't exist.
- --log: (Optional) Path to the log file. Default is sync.log.
- --interval: (Optional) Synchronization interval in seconds. Default is 60 seconds.

## Example

```bash
python dir_synch.py /path/to/source /path/to/replica --log sync.log --interval 120
```

This will:
- Synchronize files between /path/to/source and /path/to/replica every two minutes.
- Log synchronization activities to sync.log.

## Stopping the Script

To stop the script, use CTRL+C.

## Logging

The script writes simple logs for file and directory creation, update, or deletion.
Logs are saved in the file specified using the --log option. By default, the log file is found at `./sync.log`.
