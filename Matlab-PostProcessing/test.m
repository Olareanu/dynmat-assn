% Example data
mass = [1, 2, 3, 4, 5]; % x-axis values
energy = [10, 20, 15, 30, 25]; % y-axis values
labels = {'Point A', 'Point B', 'Point C', 'Point D', 'Point E'}; % data point labels

% Create scatter plot
figure;
scatter(mass, energy, 'filled');
xlabel('Mass');
ylabel('Energy');
title('Interactive Scatter Plot');

% Enable data cursor mode
dcm = datacursormode(gcf);
datacursormode on;

% Set custom update function to display the label
dcm.UpdateFcn = @(obj, event_obj) myLabelCallback(event_obj, mass, energy, labels);

function txt = myLabelCallback(event_obj, mass, energy, labels)
    % Get the position of the clicked point
    pos = get(event_obj, 'Position');
    % Find the index of the clicked point
    idx = find(mass == pos(1) & energy == pos(2), 1);
    % Display the label corresponding to the point
    if ~isempty(idx)
        txt = sprintf('Mass: %.2f\nEnergy: %.2f\nLabel: %s', pos(1), pos(2), labels{idx});
    else
        txt = 'No data';
    end
end
