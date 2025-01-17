from __future__ import print_function  # For Python 2.7 print function compatibility

import os
import sys

import matplotlib.pyplot as plt
import csv


def generate_plots():
    print("Generating plots from .csv files...")
    # Get all subdirectories for history outputs
    subdirectories = [d for d in os.listdir('.') if os.path.isdir(d) and d.endswith("_history_outputs")]

    for subdir in subdirectories:
        csv_files = [f for f in os.listdir(subdir) if f.endswith('.csv')]
        for csv_file in csv_files:
            csv_path = os.path.join(subdir, csv_file)

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

                # Increase DPI for high-quality output
                plot_filename = os.path.join(subdir, "{}_{}_plot.png".format(csv_file.replace('.csv', ''), key))
                plt.savefig(plot_filename, dpi=300, bbox_inches="tight")  # Save with high DPI and tight layout
                print("Plot saved to {}".format(plot_filename))
                plt.close()


def main():
    generate_plots()

if __name__ == "__main__":
    main()