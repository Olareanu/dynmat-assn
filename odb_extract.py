import os

from odbAccess import openOdb
from abaqus import *
from abaqusConstants import *
from visualization import *
import csv
import matplotlib.pyplot as plt


# Function to export history outputs for each region to separate CSV files
def export_history_outputs_by_region(odb, output_folder):
    print(f"Extracting history outputs by region into {output_folder}...")

    try:
        # Get the first step from the ODB
        step_name = list(odb.steps.keys())[0]
        step = odb.steps[step_name]

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Process each region that has history outputs
        for history_region_key, history_region in step.historyRegions.items():
            # Create a CSV file for this region
            region_name = history_region_key.replace("/", "_")  # Replace unsupported characters in filenames
            csv_filename = os.path.join(output_folder, f"{region_name}.csv")

            # Collect data for this region
            history_data = {}
            time_set = set()
            for history_output_key, history_output in history_region.historyOutputs.items():
                data = history_output.data
                history_data[history_output_key] = data
                time_set.update([time for time, _ in data])  # Collect all unique times

            # Sort times
            sorted_time = sorted(time_set)

            # Write region data to the CSV file
            with open(csv_filename, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                # Write header (time + all output variable headers)
                header = ["Time"] + list(history_data.keys())
                writer.writerow(header)

                # Write data for each time
                for time in sorted_time:
                    row = [time]
                    for output_key in history_data.keys():
                        # Lookup the value for the given time
                        matches = [value for t, value in history_data[output_key] if t == time]
                        row.append(matches[0] if matches else None)
                    writer.writerow(row)

            print(f"Exported region {history_region_key} to {csv_filename}")

    except Exception as e:
        print(f"Error exporting history outputs: {e}")


# Function to generate a deformed field image
def capture_deformed_field(odb, image_filename, output_folder):
    print(f"Capturing deformed field image and saving to {image_filename}...")

    try:
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Full image file path
        image_file_path = os.path.join(output_folder, image_filename)


        # Create this through a macro
        session.viewports['Viewport: 1'].setValues(displayedObject=odb)

        session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
            CONTOURS_ON_DEF,))
        session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
        session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
            visibleEdges=FEATURE)
        session.pngOptions.setValues(imageSize=(1080, 672))
        session.printOptions.setValues(vpBackground=ON, reduceColors=False, compass=ON)
        session.printToFile(fileName=(image_file_path + "_1.png"), format=PNG, canvasObjects=(
            session.viewports['Viewport: 1'],))
        session.viewports['Viewport: 1'].view.setValues(session.views['Back'])
        session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
            UNDEFORMED,))
        session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
            CONTOURS_ON_DEF,))
        session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
            visibleEdges=ALL)
        session.viewports['Viewport: 1'].view.setValues(nearPlane=333.126,
                                                        farPlane=465.248, width=89.365, height=55.7612,
                                                        viewOffsetX=-30.4649,
                                                        viewOffsetY=-8.02732)
        session.printToFile(fileName=(image_file_path + "_2.png"), format=PNG, canvasObjects=(
            session.viewports['Viewport: 1'],))

    except Exception as e:
        print(f"Error capture picture with deformed field: {e}")


# Main script
def main():
    # Get all ODB files in the current directory
    odb_files = [f for f in os.listdir('.') if f.endswith('.odb')]

    # Ensure there is at least one ODB file
    if not odb_files:
        print("No .odb files found in the current directory.")
        return

    for odb_file in odb_files:
        # Open the ODB file
        print(f"Processing {odb_file}...")
        odb = openOdb(path=odb_file)

        # Export history outputs by region to a folder
        output_folder = os.path.join(".", os.path.splitext(odb_file)[0] + "_history_outputs")
        export_history_outputs_by_region(odb, output_folder)

        # Capture the deformed field image
        image_filename = f"{os.path.splitext(odb_file)[0]}_deformed"
        capture_deformed_field(odb, image_filename, output_folder)

        # Close the ODB file
        odb.close()

        # Additional cleanup for Abaqus-generated files
        try:
            log_file = "abaqus_acis.log"

            # Check and delete abaqus_acis.log
            if os.path.exists(log_file):
                os.remove(log_file)
                # print(f"File '{log_file}' has been deleted.")

        except Exception as e:
            print(f"Error during cleanup of Abaqus files: {e}")

    # Generate matplotlib plots
    generate_plots()


def generate_plots():
    print("Generating plots from .csv files...")
    # Get all subdirectories for history outputs
    subdirectories = [d for d in os.listdir('.') if os.path.isdir(d) and d.endswith("_history_outputs")]

    for subdir in subdirectories:
        csv_files = [f for f in os.listdir(subdir) if f.endswith('.csv')]
        for csv_file in csv_files:
            csv_path = os.path.join(subdir, csv_file)

            # Read CSV data
            with open(csv_path, 'r') as f:
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
                plt.title(f"History Output: {key} (Region: {csv_file.replace('.csv', '')})", fontsize=14)
                plt.legend(fontsize=10)
                plt.grid()

                # Increase DPI for high-quality output
                plot_filename = os.path.join(subdir, f"{csv_file.replace('.csv', '')}_{key}_plot.png")
                plt.savefig(plot_filename, dpi=300, bbox_inches="tight")  # Save with high DPI and tight layout
                print(f"Plot saved to {plot_filename}")
                plt.close()


if __name__ == "__main__":
    main()
