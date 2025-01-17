from __future__ import print_function  # For Python 2.7 print function compatibility

import os
import sys
import matplotlib.pyplot as plt
import csv

# Set your desired path here
BASE_PATH = r"D:\03_Projects\Dynamic_Materials\Dyn_Mat_Project\Convergence_1_2_output"  # Use raw string (r) to handle Windows paths


def is_python2():
    return sys.version_info[0] == 2


def generate_plots():
    print(f"Generating plots from .csv files in {BASE_PATH}...")

    # Ensure the base path exists
    if not os.path.exists(BASE_PATH):
        print(f"Error: Path '{BASE_PATH}' does not exist")
        return

    # Get all subdirectories for history outputs
    subdirectories = [d for d in os.listdir(BASE_PATH)
                      if os.path.isdir(os.path.join(BASE_PATH, d))
                      and d.endswith("_history_outputs")]

    for subdir in subdirectories:
        subdir_path = os.path.join(BASE_PATH, subdir)
        csv_files = [f for f in os.listdir(subdir_path) if f.endswith('.csv')]

        for csv_file in csv_files:
            csv_path = os.path.join(subdir_path, csv_file)

            # Read CSV data
            mode = 'rb' if is_python2() else 'r'
            with open(csv_path, mode) as f:
                reader = csv.reader(f)
                header = next(reader)  # Read the header row

                # Extract time and all other outputs
                columns = {col: [] for col in header}
                for row in reader:
                    for i, col in enumerate(header):
                        columns[col].append(float(row[i]) if row[i] else None)  # Handle missing data

            # Times for plotting
            times = columns["Time"]

            # Create plots for each history output
            for key in header[1:]:  # Skip "Time"
                plt.figure(figsize=(8, 8))  # Set square figure size (8x8 inches)
                plt.plot(times, columns[key], label=key)
                plt.xlabel("Time", fontsize=12)  # Larger font for readability
                plt.ylabel(key, fontsize=12)
                plt.title("History Output: {} (Region: {})".format(key, csv_file.replace('.csv', '')), fontsize=14)
                plt.legend(fontsize=10)
                plt.grid()

                # Create output directory if it doesn't exist
                output_dir = os.path.join(subdir_path, "plots")
                os.makedirs(output_dir, exist_ok=True)

                # Increase DPI for high-quality output
                plot_filename = os.path.join(output_dir, "{}_{}_plot.png".format(csv_file.replace('.csv', ''), key))
                plt.savefig(plot_filename, dpi=300, bbox_inches="tight")  # Save with high DPI and tight layout
                print("Plot saved to {}".format(plot_filename))
                plt.close()


def main():
    generate_plots()


if __name__ == "__main__":
    main()