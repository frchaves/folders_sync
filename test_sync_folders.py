import os
import shutil
import time
import subprocess
import pytest

@pytest.fixture
def setup_folders():
    # Set up test environment with 2 files and a subfolder
    shutil.rmtree("test_replica")


    os.makedirs("test_source")
    os.makedirs("test_replica")

    # Create some files in the source folder
    with open("test_source/file1.txt", "w") as f:
        f.write("Hello from file1!")
    with open("test_source/file2.txt", "w") as f:
        f.write("Hello from file2!")
    os.makedirs("test_source/subfolder")
    with open("test_source/subfolder/file3.txt", "w") as f:
        f.write("Hello from file3!")

    # Yield control to the test
    yield

    # Clean up after the test
    shutil.rmtree("test_source")
    shutil.rmtree("test_replica")

@pytest.fixture
def setup_empty_folders():
    # Clean up existing folders if they exist
    if os.path.exists("test_source"):
        shutil.rmtree("test_source")
    if os.path.exists("test_replica"):
        shutil.rmtree("test_replica")

    # Create empty source and replica folders
    os.makedirs("test_source")
    os.makedirs("test_replica")

    # Yield control to the test
    yield

    # Clean up after the test
    shutil.rmtree("test_source")
    shutil.rmtree("test_replica")

def test_sync_script(setup_folders):
    # Run synchronization script
    subprocess.Popen(["python", "folders_sync.py", "test_source", "test_replica", "sync_log.txt", "5"])

    # Wait for synchronization to occur
    time.sleep(10)

    # Verify that replica folder has been updated correctly
    replica_files = os.listdir("test_replica")
    expected_files = ["file1.txt", "subfolder", "file2.txt"]
    assert sorted(replica_files) == sorted(expected_files), "Replica folder does not contain the expected files."

    subfolder_files = os.listdir("test_replica/subfolder")
    assert sorted(subfolder_files) == ["file3.txt"], "Subfolder in replica folder does not contain the expected file."

    with open("test_replica/file1.txt", "r") as f:
        content = f.read()
        assert "Hello from file1!" in content, "File content not updated in replica folder."

def test_empty_folders(setup_empty_folders):
    # Run synchronization script
    subprocess.Popen(["python", "folders_sync.py", "test_source", "test_replica", "sync_log.txt", "5"])

    # Wait for synchronization to occur
    time.sleep(10)

    # Check if both source and replica folders are empty
    source_files = os.listdir("test_source")
    replica_files = os.listdir("test_replica")
    assert not source_files, "Source folder is not empty."
    assert not replica_files, "Replica folder is not empty."