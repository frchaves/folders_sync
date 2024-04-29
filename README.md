# folders sync

## Description:
A program that synchronizes two folders: source and replica.
It uses Pytest to test the program.

### Setup:

- Run the program with ```python folders_sync.py <source_folder> <replica_folder> <log_file> <sync_interval>```. Sync_interval is in seconds.
- For example ```python folders_sync.py test1 test2 folder_sync_logs 5```

### Tests:

- Create a virtual environment and install Pytest ```pip install pytest```
- Run the tests with ```pytest test_folders_sync.py```
