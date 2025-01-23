clc;
clear;
close all

load("data_clamped.mat");


%Filter data sets



indices = [];

for i = 1:length(dataStruct)
    
    match = dataStruct(i).damage;

    if match
        indices = [indices, i];
    end
end

fData = dataStruct(indices);


labels = fData.label

for i =1:length(fData)
    disp(fData(i).label)
end

