clc
clear
close all

% Define the parent directory where simulation folders are located
parentDir = pwd; % Current directory where the script is located

% List all subfolders in the parent directory
subfolders = dir(fullfile(parentDir, 'Job-conv-AA7020-SV-*-EPT-*-IDV-*_history_outputs')); 
%Edit to adjust to other studies, * signify variables


% Loop through each folder
for i = 1:length(subfolders)
    folderName = subfolders(i).name;
    folderPath = fullfile(parentDir, folderName);

    % Extract EPT value from the folder name
    eptMatch = regexp(folderName, 'EPT-(\d+)', 'tokens');
    if isempty(eptMatch)
        warning('Could not extract EPT value from folder: %s', folderName);
        continue;
    end
    eptValue = str2double(eptMatch{1}{1});

     % Extract SV value from the folder name
    svMatch = regexp(folderName, 'SV-(\d+)', 'tokens');
    if isempty(svMatch)
        warning('Could not extract SV value from folder: %s', folderName);
        continue;
    end
    svValue = str2double(svMatch{1}{1});

    % Extract IDV value from the folder name
    idvMatch = regexp(folderName, 'IDV-(\d+)', 'tokens');
    if isempty(idvMatch)
        warning('Could not extract IDV value from folder: %s', folderName);
        continue;
    end
    idvValue = str2double(idvMatch{1}{1});

    % Define the file path for the 'Node INDENTER-1.10.csv' file
    indenterFilePath = fullfile(folderPath, 'Node INDENTER-1.10.csv');

    % Check if the file exists
    if ~isfile(indenterFilePath)
        warning('File not found: %s', indenterFilePath);
        continue;
    end

    % Define the file path for the 'Node INDENTER-1.10.csv' file
    assemblyFilePath = fullfile(folderPath, 'Assembly ASSEMBLY.csv');

    % Check if the file exists
    if ~isfile(assemblyFilePath)
        warning('File not found: %s', assemblyFilePath);
        continue;
    end

    % Define the file path for the 'Node INDENTER-1.10.csv' file
    sheet_1_6FilePath = fullfile(folderPath, 'Node SHEET-1.6.csv');

    % Check if the file exists
    if ~isfile(sheet_1_6FilePath)
        warning('File not found: %s', sheet_1_6FilePath);
        continue;
    end

    % Define the file path for the 'Node INDENTER-1.10.csv' file
    sheet_1_11FilePath = fullfile(folderPath, 'Node SHEET-1.11.csv');

    % Check if the file exists
    if ~isfile(sheet_1_11FilePath)
        warning('File not found: %s', sheet_1_11FilePath);
        continue;
    end

     % Define the file path for the 'Node INDENTER-1.10.csv' file
    sheet_1_19FilePath = fullfile(folderPath, 'Node SHEET-1.19.csv');

    % Check if the file exists
    if ~isfile(sheet_1_19FilePath)
        warning('File not found: %s', sheet_1_19FilePath);
        continue;
    end

    %Extract simulation time

    staName = extractBefore(folderName, '_history_outputs') + ".sta";

    if ~isfile(staName)
        warning('File not found: %s', staName);
        continue;
    end

    % Initialize the variable
    sim_time = NaN;

    % Open the file for reading
    fileID = fopen(staName, 'r');

    % Read the file line by line
    while ~feof(fileID)
        % Read a single line
        line = fgetl(fileID);
        
        % Check if the line contains the target string
        if contains(line, 'WALLCLOCK TIME (SEC)')
            % Extract the numerical value using regular expressions
            tokens = regexp(line, 'WALLCLOCK TIME \(SEC\) =\s+([\d.]+)', 'tokens');
            
            % Convert the extracted value to a number
            if ~isempty(tokens)
                sim_time = str2double(tokens{1}{1});
            end
            break; % Exit the loop after finding the line
        end
    end
    
    % Close the file
    fclose(fileID);


    % Import the CSV file
    try
        %Read tables
        data_indenter = readtable(indenterFilePath);
        data_assembly = readtable(assemblyFilePath);
        data_sheet_1_6 = readtable(sheet_1_6FilePath);
        data_sheet_1_11 = readtable(sheet_1_11FilePath);
        data_sheet_1_19 = readtable(sheet_1_19FilePath);
        
        %Parameters
        dataStruct(i).EPT = eptValue;
        dataStruct(i).SV = svValue;
        dataStruct(i).IDV = idvValue;
        dataStruct(i).staTime = sim_time;

        %Tables
        dataStruct(i).DataIndenter = data_indenter;
        dataStruct(i).DataAssembly = data_assembly;
        dataStruct(i).DataSheet_1_6 = data_sheet_1_6;
        dataStruct(i).DataSheet_1_11 = data_sheet_1_11;
        dataStruct(i).DataSheet_1_19 = data_sheet_1_19;

    catch ME
        warning('Error reading file: %s\n%s', indenterFilePath, ME.message);
        continue;
    end
end


save('conv_study_AA7020.mat', 'dataStruct');