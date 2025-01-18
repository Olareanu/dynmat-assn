import os
import subprocess
from datetime import datetime

# Log file (you can customize the name or file location)
log_file = "submission.log"

# Initialize the log file with a timestamp
with open(log_file, "a") as log:
    log.write(f"Job submission log: {datetime.now()}\n")

# Folder containing your files (".", i.e., current folder, by default)
folder = "."

# List all files in the folder starting with "Job-cov"
job_files = [f for f in os.listdir(folder) if f.startswith("Job-conv-") and os.path.isfile(os.path.join(folder, f))]

# Loop through all matched files
for job_file in job_files:
    # Remove the file extension to extract the job name
    job_name = os.path.splitext(job_file)[0]

    # Prepare the sbatch command
    command = [
        "sbatch",
        "-n", "2",
        "-t", "1-0",
        "--mem-per-cpu", "2G",
        "--wrap", f"abaqus job={job_name} double cpus=2 scratch=$TMPDIR"
    ]

    try:
        # Submit the job using subprocess and capture the output
        result = subprocess.run(
            command,
            check=True,          # Raise an exception if the sbatch command fails
            capture_output=True, # Capture standard output and error
            text=True            # Decode output as text
        )

        # Log success
        with open(log_file, "a") as log:
            log.write(f"Submitting job: {job_name}\n")
            log.write(result.stdout + "\n")

    except subprocess.CalledProcessError as e:
        # Log if sbatch fails
        with open(log_file, "a") as log:
            log.write(f"Failed to submit job: {job_name}\n")
            log.write(e.stderr + "\n")

# Append the completion timestamp to the log file
with open(log_file, "a") as log:
    log.write(f"Job submissions completed: {datetime.now()}\n")