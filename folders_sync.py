import os
import sys
import time
import shutil
import hashlib

def calculate_hash(file_path):
    """
    Calculate the MD5 hash of a file.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source_folder, replica_folder, log_file):
    """
    Synchronize the source folder to the replica folder.
    """
    # Create replica folder if it doesn't exist
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    # Log file operations
    def log(message):
        with open(log_file, 'a') as f:
            f.write(message + '\n')
        print(message)

    # Synchronize files and folders
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_file_path = os.path.join(root, file)
            replica_file_path = os.path.join(replica_folder, os.path.relpath(source_file_path, source_folder))

            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(replica_file_path), exist_ok=True)

            # Check if file exists in replica folder
            if os.path.exists(replica_file_path):
                # Compare file hashes
                source_hash = calculate_hash(source_file_path)
                replica_hash = calculate_hash(replica_file_path)
                if source_hash == replica_hash:
                    continue  # File is identical, no need to copy
                else:
                    log(f"File '{source_file_path}' has changed, updating in replica folder.")
            else:
                log(f"File '{source_file_path}' does not exist in replica folder, copying.")

            # Copy file from source to replica
            shutil.copy2(source_file_path, replica_file_path)

    # Remove files from replica folder that don't exist in source folder
    for root, dirs, files in os.walk(replica_folder):
        for file in files:
            replica_file_path = os.path.join(root, file)
            source_file_path = os.path.join(source_folder, os.path.relpath(replica_file_path, replica_folder))
            if not os.path.exists(source_file_path):
                log(f"File '{replica_file_path}' does not exist in source folder, removing from replica folder.")
                os.remove(replica_file_path)

if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: python folders_sync.py <source_folder> <replica_folder> <log_file> <sync_interval>")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    log_file = sys.argv[3]
    sync_interval = int(sys.argv[4])

    # Run synchronization loop
    while True:
        sync_folders(source_folder, replica_folder, log_file)
        print("Sync completed at", time.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(sync_interval)  # Sync every X seconds
