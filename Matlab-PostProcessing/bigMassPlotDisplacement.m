clc;
clear;
close all

load("data_clamped.mat");


%Filter data sets


IDV_fix = 3;

indices = [];

for i = 1:length(dataStruct)
    
    match = (dataStruct(i).IDV == IDV_fix);
    % if (dataStruct(i).MATV == 2) && (dataStruct(i).EPT ==3)
    %     match = false;
    % end
    if match
        indices = [indices, i];
    end
end

fData = dataStruct(indices);

m = zeros(length(fData),1);
dE = m;
maxd = m;
mat = m;
labels = cell(length(fData),1);

for i = 1:length(fData)
    m(i) = fData(i).mass;
    dE(i) = absorbedEnergy(fData(i));
    maxd(i) = maxDisplacement(fData(i));
    mat(i) = fData(i).MATV;
    labels{i} = (fData(i).label);
end



% figure
% hold on
% scatter(m,dE,[],mat, 'filled')
% % plot(m,dE,'r+', "MarkerSize",5)
% 
% colororder("reef")
% hold off
% xlabel("Mass [kg]")
% ylabel("Absorbed energy [mJ]")





figure
hold on
scatter(m, maxd,[],mat,'filled')
colororder("reef")
hold off
xlabel("Mass [kg]")
ylabel("Max displacement [mm]")
xlim([0,0.66])
ylim([0,22])
% Enable data cursor mode
dcm = datacursormode(gcf);
datacursormode on;
% Set custom update function to display the label
dcm.UpdateFcn = @(obj, event_obj) myLabelCallback(event_obj, m, maxd, labels);




function txt = myLabelCallback(event_obj, m, dE, labels)
    % Get the position of the clicked point
    pos = get(event_obj, 'Position');
    % Find the index of the clicked point
    idx = find(m == pos(1) & dE == pos(2), 1);
    % % Display the label corresponding to the point
    if ~isempty(idx)
        txt = sprintf('Mass: %.2f kg\nMax. displacement: %.2f mm\nConfig: %s', pos(1), pos(2), labels{idx});
    else
        txt = 'No data';
    end
end

