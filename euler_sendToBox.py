import os
import subprocess
import shlex

# Configuration
file_prefix = "Job-conv-DP590-"  # Change this to the prefix you want to filter by
file_extension = ""  # Change this to None if no file extension filter is required
storagebox_url = "u443450.your-storagebox.de"
remote_folder = "Run_0"  # Folder on the remote storage box
username = "your_username"  # Username for the storage box
port = 23  # Port for rsync connection


def select_files(current_folder, prefix, extension):
    """
    Select files in the current folder based on the given prefix and optional file extension.

    :param current_folder: The path to the current folder.
    :param prefix: The prefix that files should start with.
    :param extension: The extension that files should end with, or None if no extension is required.
    :return: A list of matching files.
    """
    files = []
    for file_name in os.listdir(current_folder):
        if file_name.startswith(prefix) and (extension is None or file_name.endswith(extension)):
            files.append(file_name)
    return files


def transfer_files(selected_files, port):
    """
    Transfer the given files to the remote storage box using rsync with compression.

    All files are included in a single rsync command, and compression is enabled with the -z flag.

    :param selected_files: A list of filenames to transfer.
    :param port: The port to use for the rsync connection.
    """
    # Build a single rsync command with all filenames
    remote_path = f"{username}@{storagebox_url}:{remote_folder}"

    # Include all selected files in the rsync command
    file_list = " ".join(shlex.quote(file_name) for file_name in selected_files)
    rsync_command = f"rsync -e 'ssh -p {port}' -avz {file_list} {remote_path}"

    try:
        print("Transferring files (with compression)...")
        # Run the rsync command; the user will be prompted to enter their password once
        process = subprocess.run(
            rsync_command,  # Command as a single string (shell-style command)
            shell=True,
            check=True,
        )
        print("All files transferred successfully.")
    except subprocess.CalledProcessError as e:
        # Print the error return code and error message
        print(f"Error transferring files (status code {e.returncode}):\n")
        print("STDERR:")
        print(e.stderr.decode())
        print("STDOUT:")
        print(e.stdout.decode())


def main():
    # Identify the current working directory
    current_folder = os.getcwd()

    # Select files based on the prefix and optional extension
    selected_files = select_files(current_folder, file_prefix, file_extension)

    # Display how many files were selected and their filter criteria
    files_count = len(selected_files)
    file_desc = f"starting with '{file_prefix}'"
    if file_extension:
        file_desc += f" and ending with '{file_extension}'"

    if files_count == 0:
        print(f"No files {file_desc} were found in the current directory.")
        return

    print(f"{files_count} file(s) {file_desc} were selected:")
    for file_name in selected_files:
        print(f"- {file_name}")

    # User confirmation prompt
    print(
        f"\nSend these file(s) to folder '{remote_folder}' on storage box '{storagebox_url}' using rsync on port {port}? (Y/N)")
    user_response = input("Enter your choice: ").strip().lower()

    if user_response != 'y':
        print("Operation cancelled.")
        return

    # Transfer files using rsync
    print("Starting file transfer...")
    transfer_files(selected_files, port)
    print("File transfer complete.")


if __name__ == "__main__":
    main()