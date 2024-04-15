import hashlib
import json
import os
import shutil
import sys
import tarfile
import zipfile


def load_previous_state(json_file):
    """
    Load the previous state from a JSON file.
    Returns a dictionary with directory and file information.
    """
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"directories": [], "files": []}


def save_current_state(json_file, current_state):
    """
    Save the current state to a JSON file.
    """
    with open(json_file, "w") as f:
        json.dump(current_state, f, indent=4)


def compare_states(previous_state, current_state):
    """
    Compare previous and current states to find new directories and files.
    """
    new_directories = set(current_state["directories"]) - set(
        previous_state["directories"]
    )
    new_files = set(current_state["files"]) - set(previous_state["files"])
    return new_directories, new_files


def traverse_directory(directory):
    """
    Recursively traverse the directory tree and collect directories and files.
    """
    directories = []
    files = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.relpath(os.path.join(root, filename), directory))
        for dirname in dirnames:
            directories.append(os.path.relpath(os.path.join(root, dirname), directory))
            # print(os.path.relpath(os.path.join(root, dirname), directory))
    return directories, files


def create_zip_archive(directory, output_filename, new_directories, new_files):
    """
    Create a ZIP archive containing new directories and files.
    """
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for new_dir in new_directories:
            zipf.write(os.path.join(directory, new_dir), arcname=new_dir)
        for new_file in new_files:
            zipf.write(os.path.join(directory, new_file), arcname=new_file)


def create_tar_gz_archive(directory, output_filename, new_directories, new_files):
    """
    Create a .tar.gz archive containing new directories and files.
    """
    with tarfile.open(output_filename, "w:gz") as tar:
        for new_dir in new_directories:
            tar.add(os.path.join(directory, new_dir), arcname=new_dir)
        for new_file in new_files:
            tar.add(os.path.join(directory, new_file), arcname=new_file)


def sha1(input_string):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(input_string.encode("utf-8"))
    return sha1_hash.hexdigest()


def main():
    if len(sys.argv) < 2:
        print("Specify directory name to monitor and target archive name")
        sys.exit(1)

    directory_to_monitor = sys.argv[1]
    output_filename = sys.argv[2]

    # directory_to_monitor = "/Users/feodor/.python-for-android/dists/mydist"
    h = sha1(directory_to_monitor)
    json_file = f"previous_state_{h}.json"

    # Load previous state
    previous_state = load_previous_state(json_file)

    # Get current state (directories and files)
    current_directories, current_files = traverse_directory(directory_to_monitor)
    current_state = {"directories": current_directories, "files": current_files}

    # Compare states
    new_directories, new_files = compare_states(previous_state, current_state)

    # Create ZIP archive
    create_zip_archive(
        directory_to_monitor, output_filename, new_directories, new_files
    )

    # Save current state for the next session
    save_current_state(json_file, current_state)


if __name__ == "__main__":
    main()
