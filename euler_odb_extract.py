import os
import sys
import time
import argparse
from odbAccess import openOdb
from abaqus import *
from abaqusConstants import *
from visualization import *
import csv
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior


def is_python2():
    return sys.version_info[0] == 2


# Function to export history outputs for each region to separate CSV files
def export_history_outputs_by_region(odb, output_folder):
    print("Extracting history outputs by region into {}...".format(output_folder))
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
            csv_filename = os.path.join(output_folder, "{}.csv".format(region_name))
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
            mode = 'wb' if is_python2() else 'w'
            kwargs = {} if is_python2() else {'newline': ''}
            with open(csv_filename, mode, **kwargs) as csv_file:
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
            print("Exported region {} to {}".format(history_region_key, csv_filename))
    except Exception as e:
        print("Error exporting history outputs: {}".format(e))


def export_field_outputs_of_deleted_element(odb, field_filename, output_folder):
    print("Extracting field outputs for deleted elements into {}...".format(output_folder))
    try:
        # Get the first step from the ODB
        step_name = list(odb.steps.keys())[0]
        step = odb.steps[step_name]
        # Find the first deleted element in the last frame
        last_frame = step.frames[-1]
        status_field = last_frame.fieldOutputs['STATUS']
        failure_detected = False
        for value in status_field.values:
            if value.data == 0:  # STATUS = 0 indicates the element is deleted
                failure_detected = True
        first_deleted = None
        for frame in step.frames:
            field = frame.fieldOutputs['STATUS']
            for value in field.values:
                if value.data == 0:  # Element is deleted
                    first_deleted = value.elementLabel  # Get the element label
                    break
            if first_deleted:
                break
        if not first_deleted:
            print("No elements were deleted in the simulation.")
            return
        print("First deleted element: {}".format(first_deleted))
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # Prepare for data extraction
        field_variables = [
            'CENER', 'DMENER', 'LE', 'LODE', 'PE', 'PEEQ',
            'PENER', 'S', 'SENER', 'TEMP', 'TRIAX', 'VENER'
        ]
        # Collect data for the first deleted element
        field_data = []
        headers = ['Frame', 'Time'] + field_variables
        for frame_index, frame in enumerate(step.frames):
            time = frame.frameValue  # Simulation time
            row = [frame_index, time]
            for variable in field_variables:
                try:
                    field_output = frame.fieldOutputs[variable]
                    element_value = next(
                        val for val in field_output.values if val.elementLabel == first_deleted
                    )
                    row.append(element_value.data)
                except KeyError:
                    row.append("N/A")  # Variable not found
                except StopIteration:
                    row.append("N/A")  # Element data not found
            field_data.append(row)
        # Write data to a CSV file
        csv_filename = os.path.join(output_folder, "{}_deleted_element.csv".format(field_filename))
        mode = 'wb' if is_python2() else 'w'
        kwargs = {} if is_python2() else {'newline': ''}
        with open(csv_filename, mode, **kwargs) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)  # Write the header row
            writer.writerows(field_data)  # Write the data rows
        print("Field data for the deleted element exported to {}".format(csv_filename))
    except Exception as e:
        print("Error exporting field outputs: {}".format(e))


# Function to generate a deformed field image
def capture_deformed_field(odb, image_filename, output_folder):
    print("Capturing deformed field image and saving to {}...".format(image_filename))
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
        print("Error capturing picture with deformed field: {}".format(e))


# Main script
def main():

    # Get all ODB files in the current directory
    odb_files = [f for f in os.listdir('.') if f.endswith('.odb')]

    # Filter ODB files if a filter string is provided
    print(sys.argv)
    if len(sys.argv) > 10:
        odb_files = [f for f in odb_files if sys.argv[-1] in f]
        print("hello bro")

    # Ensure there is at least one ODB file
    if not odb_files:
        print("No .odb files found matching the specified criteria.")
        return

    for odb_file in odb_files:
        # Open the ODB file
        print("Processing {}...".format(odb_file))
        odb = openOdb(path=odb_file)

        # Export history outputs by region to a folder
        output_folder = os.path.join(".", os.path.splitext(odb_file)[0] + "_history_outputs")
        export_history_outputs_by_region(odb, output_folder)

        # Export field outputs of deleted element
        field_name = "{}".format(os.path.splitext(odb_file)[0])
        export_field_outputs_of_deleted_element(odb, field_name, output_folder)

        # Capture the deformed field image
        image_filename = "{}_deformed".format(os.path.splitext(odb_file)[0])
        capture_deformed_field(odb, image_filename, output_folder)

        # Close the ODB file
        odb.close()


if __name__ == "__main__":
    main()