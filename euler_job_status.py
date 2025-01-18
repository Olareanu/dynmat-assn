import os
import glob

# Define ANSI escape codes for text colors
RED = '\033[31m'  # Red color for errors
RESET = '\033[0m'  # Reset to default terminal color


def parse_wallclock_time_and_status(sta_file):
    """
    Parse the .sta file to extract the Abaqus job status and wallclock time.
    """
    job_completed = False
    wallclock_time_seconds = None
    wallclock_time_hours = None

    with open(sta_file, 'r') as f:
        for line in f:
            # Check for successful completion
            if "THE ANALYSIS HAS COMPLETED SUCCESSFULLY" in line:
                job_completed = True
            # Extract wallclock time
            if "WALLCLOCK TIME (SEC)" in line:
                wallclock_time_seconds = float(line.split('=')[1].strip())
                wallclock_time_hours = wallclock_time_seconds / 3600  # Convert to hours

    return job_completed, wallclock_time_seconds, wallclock_time_hours


def check_job_status_and_time(job_directory):
    """
    Traverse all .sta files in a given directory to check job completion status and timing.
    """
    # Find all .sta files in the directory
    sta_files = glob.glob(os.path.join(job_directory, '*.sta'))
    results = []

    for sta_file in sta_files:
        job_name = os.path.splitext(os.path.basename(sta_file))[0]
        job_completed, wallclock_time_seconds, wallclock_time_hours = parse_wallclock_time_and_status(sta_file)

        # Append result for this job
        result = {
            'Job Name': job_name,
            'Completed': job_completed,
            'Wallclock Time (s)': wallclock_time_seconds,
            'Wallclock Time (hours)': wallclock_time_hours
        }
        results.append(result)

    return results


if __name__ == "__main__":
    # Get the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Run the function to check job statuses and times
    job_results = check_job_status_and_time(script_directory)

    # Print the results
    for result in job_results:
        if result['Completed']:
            # Print for completed jobs (normal output)
            print(f"{result['Job Name']} - Completed: {result['Completed']} - "
                  f"Wallclock Time (s): {result['Wallclock Time (s)']}, "
                  f"Wallclock Time (hours): {result['Wallclock Time (hours)']:.2f}")
        else:
            # Print in red for jobs that did not complete successfully
            print(RED + f"{result['Job Name']} - Completed: {result['Completed']} - "
                        f"Wallclock Time (s): {result['Wallclock Time (s)']}, "
                        f"Wallclock Time (hours): {result['Wallclock Time (hours)']}" + RESET)