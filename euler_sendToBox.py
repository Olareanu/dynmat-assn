import os
import subprocess
import shlex

# Configuration
file_prefix = "Job"  # Change this to the prefix you want to filter by
file_extension = ".odb"  # Change this to None if no file extension filter is required
storagebox_url = "your_username.your-storagebox.de"
remote_folder = "DynMat_Main/SSH_Test"  # Folder on the remote storage box
username = "your_username"  # Username for the storage box
port = 22  # Port for SCP connection (default changed to 23 for your setup)


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
    Transfer the given files to the remote storage box using SCP.

    :param selected_files: A list of filenames to transfer.
    :param port: The port to use for the SCP connection.
    """
    for file_name in selected_files:
        remote_path = f"{username}@{storagebox_url}:{remote_folder}"

        # Create the SCP command with the specified port, only using relative filenames
        scp_command = f"scp -P {port} {shlex.quote(file_name)} {shlex.quote(remote_path)}"

        try:
            print(f"Transferring {file_name}...")
            # Run the SCP command; the user will be prompted to enter their password
            process = subprocess.run(
                scp_command.split(),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(f"{file_name} transferred successfully.")
        except subprocess.CalledProcessError as e:
            # Print the error return code and error message
            print(f"Error transferring {file_name} (status code {e.returncode}):\n")
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
        f"\nSend these file(s) to folder '{remote_folder}' on storage box '{storagebox_url}' using port {port}? (Y/N)")
    user_response = input("Enter your choice: ").strip().lower()

    if user_response != 'y':
        print("Operation cancelled.")
        return

    # Transfer files using SCP
    print("Starting file transfer...")
    transfer_files(selected_files, port)
    print("File transfer complete.")


if __name__ == "__main__":
    main()