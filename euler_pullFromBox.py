import os
import subprocess
import shlex

# Configuration
file_prefix = "Job-"  # Change this to the prefix you want to filter by
file_extension = ".odb"  # Change this to None if no file extension filter is required
storagebox_url = "u443450.your-storagebox.de"
remote_folder = "Run_0"  # Folder on the remote storage box
username = "your_username"  # Username for the storage box
port = 23  # Port for rsync connection


def filter_remote_files(remote_files, prefix, extension):
    """
    Filter remote files based on the given prefix and optional file extension.
    :param remote_files: A list of remote filenames.
    :param prefix: The prefix that files should start with.
    :param extension: The extension that files should end with, or None if no extension is required.
    :return: A list of filtered filenames.
    """
    filtered_files = []
    for file_name in remote_files:
        if file_name.startswith(prefix) and (extension is None or file_name.endswith(extension)):
            filtered_files.append(file_name)
    return filtered_files


def list_remote_files(port):
    """
    List all files available in the remote folder using SSH.
    :param port: The port to use for the SSH connection.
    :return: A list of filenames in the remote folder.
    """
    ssh_command = f"ssh -p {port} {username}@{storagebox_url} 'ls {shlex.quote(remote_folder)}'"
    try:
        print("Fetching file list from the remote folder...")
        result = subprocess.run(
            ssh_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        remote_files = result.stdout.splitlines()
        return remote_files
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving file list (status code {e.returncode}):\n")
        print("STDERR:")
        print(e.stderr)
        return []


def download_files(filtered_files, port):
    """
    Download the given files from the remote storage box using rsync.
    :param filtered_files: A list of filenames to download.
    :param port: The port to use for the rsync connection.
    """
    remote_path = f"{username}@{storagebox_url}:{remote_folder}"
    file_list = " ".join(f"{shlex.quote(remote_path)}/{shlex.quote(file_name)}" for file_name in filtered_files)
    rsync_command = f"rsync -e 'ssh -p {port}' -avz {file_list} ."
    try:
        print("Downloading files (with compression)...")
        subprocess.run(
            rsync_command,
            shell=True,
            check=True,
        )
        print("All files downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading files (status code {e.returncode}):\n")
        print("STDERR:")
        print(e.stderr)
        print("STDOUT:")
        print(e.stdout)


def main():
    # Fetch the list of all files on the remote storage
    remote_files = list_remote_files(port)
    if not remote_files:
        print("No files found in the remote folder.")
        return

    # Filter the files based on the prefix and optional extension
    filtered_files = filter_remote_files(remote_files, file_prefix, file_extension)

    file_desc = f"starting with '{file_prefix}'"
    if file_extension:
        file_desc += f" and ending with '{file_extension}'"

    if not filtered_files:
        print(f"No files {file_desc} were found in the remote folder.")
        return

    print(f"{len(filtered_files)} file(s) {file_desc} were selected for download:")
    for file_name in filtered_files:
        print(f"- {file_name}")

    # User confirmation prompt
    print(
        f"\nDownload these file(s) to the current directory on the compute cluster? (Y/N)"
    )
    user_response = input("Enter your choice: ").strip().lower()
    if user_response != 'y':
        print("Operation cancelled.")
        return

    # Download the files using rsync
    print("Starting file download...")
    download_files(filtered_files, port)
    print("File download complete.")


if __name__ == "__main__":
    main()