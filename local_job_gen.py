import os


def create_and_run_script(elements_per_thickness, sheet_version=1, indenter_version=1):
    # Define the name of the original script
    original_script_name = "abq_script_model.py"

    # Check if the original script exists
    if not os.path.exists(original_script_name):
        print(f"Error: The script '{original_script_name}' does not exist in the current directory.")
        return

    # Define the base name of the new scripts
    new_script_base_name = "abq_temp_script"

    # Dynamically create the job name
    job_name = f"Job-conv-DP590-SV-{sheet_version}-EPT-{elements_per_thickness}-IDV-{indenter_version}"  # EPT = Elements Per Thickness etc

    # Define the lines to prepend to the script
    prepend_lines = [
        "# Prepended parameters\n",
        f"job_name = '{job_name}'  # Job name dynamically generated\n",
        f"nr_cpus = 4\n"
        f"sim_step_time = 0.0035\n"
        f"bending_radius = 17.0  # Bending radius\n",
        f"bending_angle = 25.0  # Bending angle\n",
        f"sheet_thickness = 1.4  # Thickness\n",
        f"sheet_material = 1 \n"
        f"sheet_version = {sheet_version}  # Sheet version (1: simple, 3: elliptical hole, etc.)\n",
        f"elements_per_thickness = {elements_per_thickness}  # Dynamic value being iterated\n",
        f"smallest_element_length = sheet_thickness / elements_per_thickness\n",
        f"indenter_version = {indenter_version}  # 1 cylindrical indenter, 2 rigid cylindrical indenter\n\n"
    ]

    # Generate a unique script name for this run
    iteration_script_name = f"{new_script_base_name}_SV_{sheet_version}_EPT_{elements_per_thickness}-IDV-{indenter_version}.py"

    try:
        # Create/open the new script for writing
        with open(iteration_script_name, "w") as new_script:
            # Write the prepended lines
            new_script.writelines(prepend_lines)

            # Append the contents of the original script
            with open(original_script_name, "r") as original_script:
                new_script.writelines(original_script)

        # Run the new script using Abaqus CAE
        # Ensure the abaqus command is available in your system's PATH
        # Run with or without opening the GUI

        abaqus_command = f"abaqus cae noGUI={iteration_script_name}"
        # abaqus_command = f"abaqus cae script={iteration_script_name}"

        print(f"Running the script using Abaqus CAE: {abaqus_command}")
        return_code = os.system(abaqus_command)

        # Check the return code of the Abaqus command
        if return_code == 0:
            print(f"Abaqus script '{iteration_script_name}' completed successfully.")
            # Append whatever you want to log
            with open("job_gen_log.txt", "a") as file:
                file.write(f"{job_name}\n", )
        else:
            print(
                f"Warning: Abaqus script '{iteration_script_name}' finished with errors (return code: {return_code}).")

    except Exception as e:
        print(
            f"An error occurred creating or running script for elements_per_thickness={elements_per_thickness}, sheet_version={sheet_version}: {e}")
        return

    finally:
        # Remove the temporary script after execution
        try:
            if os.path.exists(iteration_script_name):
                os.remove(iteration_script_name)
                # print(f"Temporary script '{iteration_script_name}' has been deleted.")
        except Exception as e:
            print(f"Error: Could not delete temporary script '{iteration_script_name}': {e}")

        # Additional cleanup for Abaqus-generated files
        try:
            rpy_file = "abaqus.rpy"
            log_file = "abaqus_acis.log"

            # Check and delete abaqus.rpy
            if os.path.exists(rpy_file):
                os.remove(rpy_file)
                # print(f"File '{rpy_file}' has been deleted.")

            # Check and delete abaqus_acis.log
            if os.path.exists(log_file):
                os.remove(log_file)
                # print(f"File '{log_file}' has been deleted.")

        except Exception as e:
            print(f"Error during cleanup of Abaqus files: {e}")


if __name__ == "__main__":
    # Define the `elements_per_thickness` values to iterate over
    elements_per_thickness_values = [2, 3, 4]  # Modify as needed

    # Define the `sheet_version`
    # Version 4 with max 4 EPT!
    sv_values = [1, 2]

    # Define indenter_version
    idv_values = [2]

    # Call the function to create and run scripts
    for sv in sv_values:
        for ept in elements_per_thickness_values:
            for idv in idv_values:
                create_and_run_script(ept, sv, idv)
