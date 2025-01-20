clc;
clear;
close all

load("conv_study_AA7020.mat");


%Filter data sets
EPT_v = 6;
SV_v = 1;
indices = [];

for i = 1:length(dataStruct)
    if dataStruct(i).EPT == EPT_v &&  dataStruct(i).SV == SV_v
        indices = [indices, i];
    end
end

fData = dataStruct(indices);

figure()
hold on

for i = 1:length(fData)
    table = fData(i).DataIndenter;
    time = table{:,1};
    U2 = table{:,5};
    IDVvalue = fData(i).IDV;

    plot(time,U2,'LineWidth',2, 'DisplayName',sprintf('IDV-%d', IDVvalue))
end
hold off

legend('show')
xlabel('Time [s]')
ylabel('Displacement [mm]')
title('Vertical displacement of the indenter against time')

table_1 = fData(1).DataIndenter;
time_1 = table_1{:,1};
U2_1 = table_1{:,5};

table_2 = fData(2).DataIndenter;
time_2 = table_2{:,1};
U2_2 = table_2{:,5};

per_err = 100 * abs(U2_1-U2_2)./abs(U2_1);

figure
hold on
plot(time_1,per_err, 'LineWidth',2)
xlabel('Time [s]')
ylabel('Relative error [%]')
title('Relative error between indenter types against time')
hold off


max(per_err)


