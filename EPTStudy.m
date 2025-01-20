clc;
clear;
close all

load("conv_study_AA7020.mat");


%Filter data sets

IDV_v = 1;
indices = [];

for i = 1:length(dataStruct)
    match = dataStruct(i).IDV == IDV_v;
    if match
        indices = [indices, i];
    end
end

fData = dataStruct(indices);

table = fData(end).DataIndenter;
time = table{:,1};
maxt = 1e-3 * ones(size(time));

[~,IDMAX] = min(abs(time-maxt))


figure()
hold on

for i = 1:length(fData)
    table = fData(i).DataIndenter{1:IDMAX,:};
    time = table(:,1);
    U2 = table(:,5);
    EPTvalue = fData(i).EPT;

    plot(time,U2,'LineWidth',1, 'DisplayName',sprintf('EPT-%d', EPTvalue))
end
hold off

legend('show')
xlabel('Time [s]')
ylabel('Displacement [mm]')
title('Vertical displacement of the indenter against time')

figure
hold on
for i = 3:(length(fData)-1)
    table = fData(i).DataIndenter{1:IDMAX,:};
    table_next = fData(i+1).DataIndenter{1:IDMAX,:};
    time = table(1:IDMAX,1);
    U2 = table(:,5);
    U2_next = table_next(:,5);

    rel_error = 100 * abs(U2_next - U2)./abs(U2_next);
    EPTvalue = fData(i).EPT;

    plot(time,rel_error,'LineWidth',1, 'DisplayName',sprintf('EPT-%d', EPTvalue))
end
hold off

legend('show')
xlabel('Time [s]')
ylabel('Relative error [%]')
title('Relative error compared to next EPT value')




