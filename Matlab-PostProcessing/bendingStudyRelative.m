clc;
clear;
close all

load("data_run1.mat");


%Filter data sets

SV_fix = 1;
MATV_fix = 1;
% EPT_fix = 6;


indices = [];

for i = 1:length(dataStruct)
    match = (dataStruct(i).SV == SV_fix) && (dataStruct(i).MATV == MATV_fix);
    % match = (dataStruct(i).SV == SV_fix) && (dataStruct(i).MATV == MATV_fix) && (dataStruct(i).EPT == EPT_fix);
    if match
        indices = [indices, i];
    end
end

fData = dataStruct(indices);

%Filter for BRV 5

BRV_fix = 5;

indices = [];

for i = 1:length(fData)
    match = (fData(i).BRV == BRV_fix);
    if match
        indices = [indices, i];
    end
end

BRV5Data = fData(indices);

%Filter for BRV 8

BRV_fix = 8;

indices = [];

for i = 1:length(fData)
    match = (fData(i).BRV == BRV_fix);
    if match
        indices = [indices, i];
    end
end

BRV8Data = fData(indices);

%Filter for BRV 10

BRV_fix = 10;

indices = [];

for i = 1:length(fData)
    match = (fData(i).BRV == BRV_fix);
    if match
        indices = [indices, i];
    end
end

BRV10Data = fData(indices);



BAV5 = zeros(1,length(BRV5Data));
U5 = BAV5;
dKE5 = U5;
m5 = U5;
for i = 1:length(BRV5Data)
    BAV5(i) = BRV5Data(i).BAV;
    m5(i) = BRV5Data(i).mass;
    U5(i) = maxDisplacement(BRV5Data(i));
    dKE5(i) = absorbedEnergy(BRV5Data(i));
end


BAV8 = zeros(1,length(BRV8Data));
U8 = BAV8;
dKE8 = U8;
m8 = U8;
for i = 1:length(BRV8Data)
    BAV8(i) = BRV8Data(i).BAV;
    m8(i) = BRV8Data(i).mass;
    U8(i) = maxDisplacement(BRV8Data(i));
    dKE8(i) = absorbedEnergy(BRV8Data(i));
end


BAV10 = zeros(1,length(BRV10Data));
U10 = BAV10;
dKE10 = U10;
m10 = U10;
for i = 1:length(BRV10Data)
    BAV10(i) = BRV10Data(i).BAV;
    m10(i) = BRV10Data(i).mass;
    U10(i) = maxDisplacement(BRV10Data(i));
    dKE10(i) = absorbedEnergy(BRV10Data(i));
end



figure
hold on
plot(BAV5,U5.*m5,'r+-','MarkerSize',8, 'DisplayName','BRV = 5 mm')
plot(BAV8,U8.*m8,'b+-','MarkerSize',8, 'DisplayName','BRV = 8 mm')
plot(BAV10,U10.*m10,'g+-','MarkerSize',8, 'DisplayName','BRV = 10 mm')
hold off

legend('show')
xlabel('BAV [\circ]')
ylabel('Maximum displacement*mass [mmkg]')
title('Maximum displacement*mass for different BAV and BRV. SV=1, MATV=1')


figure
hold on
plot(BAV5,dKE5./(m5*1000),'r+-','MarkerSize',8, 'DisplayName','BRV = 5 mm')
plot(BAV8,dKE8./(m8*1000),'b+-','MarkerSize',8, 'DisplayName','BRV = 8 mm')
plot(BAV10,dKE10./(m10*1000),'g+-','MarkerSize',8, 'DisplayName','BRV = 10 mm')
hold off

legend('show')
xlabel('BAV [\circ]')
ylabel('Absorbed energy [J/kg]')
title('Specific absorbed energy for different BAV and BRV. SV=1, MATV=1')
