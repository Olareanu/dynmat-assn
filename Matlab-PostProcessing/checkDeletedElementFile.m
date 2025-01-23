function fileExists = checkDeletedElementFile(folderpath)
    % Checks if there is a file in the folder with a name containing the phrase 'deleted_element'.
    %
    % Parameters:
    %   folderpath (string): The path to the folder to search in.
    %
    % Returns:
    %   fileExists (logical): True if a file with 'deleted_element' in its name is found, otherwise false.

    % Get a list of all files in the folder
    fileList = dir(folderpath);

    % Initialize the output as false
    fileExists = false;

    % Loop through the files
    for i = 1:length(fileList)
        % Skip directories
        if fileList(i).isdir
            continue;
        end

        % Check if 'deleted_element' is part of the file name
        if contains(fileList(i).name, 'deleted_element', 'IgnoreCase', true)
            fileExists = true;
            return; % Exit the function as we found a match
        end
    end
end