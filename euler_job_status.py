import os
import glob

# Define ANSI escape codes for text colors
RED = '\033[31m'  # Red color for "Failed" jobs
YELLOW = '\033[33m'  # Yellow color for "Incomplete" jobs
BLUE = '\033[34m'  # Blue color for "Running" jobs
RESET = '\033[0m'  # Reset to default terminal color


def parse_status_and_memory(sta_file, simdir_folder):
    """
    Parse the .sta file to extract the Abaqus job status, wallclock time, and memory used.
    Check for Running status based on presence of a .simdir folder.
    """
    status = None
    wallclock_time_seconds = None
    wallclock_time_hours = None
    memory_used = None

    # Check if the job is running based on the presence of the .simdir folder
    if os.path.isdir(simdir_folder):
        status = "Running"

    # Parse the .sta file to extract additional information, regardless of Running status
    try:
        with open(sta_file, 'r') as f:
            lines = f.readlines()
        # Check if the file is empty
        if not lines:  # Empty file
            if status != "Running":  # If not "Running," it must be "Failed"
                status = "Failed"
            return status, wallclock_time_seconds, wallclock_time_hours, memory_used

        # Iterate over lines to extract required information
        for line in lines:
            # Check for completion status
            if "THE ANALYSIS HAS COMPLETED SUCCESSFULLY" in line:
                status = "Completed"
            # Check if STEP 1 was started, implies job is Incomplete
            if "STEP 1" in line and status is None:
                status = "Incomplete"
            # Extract wallclock time
            if "WALLCLOCK TIME (SEC)" in line:
                wallclock_time_seconds = float(line.split('=')[1].strip())
                wallclock_time_hours = wallclock_time_seconds / 3600  # Convert to hours
            # Extract memory used
            if "Total memory used for step 1 is approximately" in line:
                memory_used = line.split("approximately")[1].strip().split()[0]  # Extract memory value
    except Exception as e:
        print(f"Error reading file {sta_file}: {e}")
        if status != "Running":  # If the file couldn't be read and there's no .simdir folder
            status = "Failed"

    # If no status was determined but the file was not empty, set it to Incomplete
    if status is None:
        status = "Failed"

    return status, wallclock_time_seconds, wallclock_time_hours, memory_used


def check_job_status_and_time(job_directory):
    """
    Traverse all .sta files in a given directory to check job status, timing, and memory usage.
    """
    # Find all .sta files in the directory
    sta_files = glob.glob(os.path.join(job_directory, '*.sta'))
    results = []
    for sta_file in sta_files:
        job_name = os.path.splitext(os.path.basename(sta_file))[0]
        simdir_folder = os.path.join(job_directory, f"{job_name}.simdir")
        # Check the status and memory usage
        status, wallclock_time_seconds, wallclock_time_hours, memory_used = parse_status_and_memory(sta_file,
                                                                                                    simdir_folder)
        # Append result for this job
        result = {
            'Job Name': job_name,
            'Status': status,
            'Wallclock Time (s)': wallclock_time_seconds,
            'Wallclock Time (hours)': wallclock_time_hours,
            'Memory Used': memory_used
        }
        results.append(result)
    return results


if __name__ == "__main__":
    # Get the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Run the function to check job statuses and times
    job_results = check_job_status_and_time(script_directory)

    # Sort the results alphabetically by job name
    job_results = sorted(job_results, key=lambda x: x['Job Name'])

    # Print the results
    for result in job_results:
        # Use color-coded output based on the status
        if result['Status'] == "Failed":
            color = RED
        elif result['Status'] == "Incomplete":
            color = YELLOW
        elif result['Status'] == "Running":
            color = BLUE
        else:  # Completed
            color = ""

        # Format wallclock time hours properly, handle None case
        wallclock_time_hours = f"{result['Wallclock Time (hours)']:.2f}" if result[
                                                                                'Wallclock Time (hours)'] is not None else "None"

        # Print the result with color
        print(color + f"{result['Job Name']} - Status: {result['Status']} - "
                      f"Wallclock Time (s): {result['Wallclock Time (s)']}, "
                      f"Wallclock Time (hours): {wallclock_time_hours}, "
                      f"Memory Used: {result['Memory Used']} " + RESET)
