import os
import subprocess


def submit_jobs():
    # Define an internal list of job names. If the string is contained in the name, it will get its own sbatch
    job_names = ["BAV-15-BRV-5", "BAV-15-BRV-8", "BAV-15-BRV-10", "BAV-30-BRV-5", "BAV-30-BRV-8", "BAV-30-BRV-10",
                 "BAV-45-BRV-5", "BAV-45-BRV-8", "BAV-45-BRV-10"]  # Replace these with your actual job names

    # Parameters for the sbatch script creation
    num_cpus = 2
    time_limit = "1-0"  # Format: days-hours
    memory_per_cpu = 2560  # in MB

    # Loop through job names and submit jobs
    for job_name in job_names:
        # Construct the sbatch command with the parameter for euler_odb_extract.py
        sbatch_command = (
            f"sbatch -n {num_cpus} -t {time_limit} --mem-per-cpu {memory_per_cpu} "
            f"--wrap \"abaqus cae noGUI=euler_odb_extract.py -- {job_name}\""
        )

        # Print the command for reference (optional)
        print(f"Submitting job: {job_name}")
        print(f"Command: {sbatch_command}")

        # Execute the sbatch command
        try:
            # Use subprocess to run the sbatch command
            result = subprocess.run(sbatch_command, shell=True, check=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            print(f"Submitted job '{job_name}', SLURM response: {result.stdout.decode().strip()}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to submit job '{job_name}'. Error: {e.stderr.decode().strip()}")


if __name__ == "__main__":
    submit_jobs()
