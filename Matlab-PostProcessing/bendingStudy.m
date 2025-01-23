clc;
clear;
close all

load("data_clamped.mat");


%Filter data sets

SV_fix = 71;
MATV_fix = 2;
EPT_fix = 6;
IDV_fix = 3;


indices = [];

for i = 1:length(dataStruct)
    % match = (dataStruct(i).SV == SV_fix) && (dataStruct(i).MATV == MATV_fix);
    match = all([(dataStruct(i).SV == SV_fix), (dataStruct(i).MATV == MATV_fix), ...
     (dataStruct(i).EPT == EPT_fix), (dataStruct(i).IDV == IDV_fix)]);
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
for i = 1:length(BRV5Data)
    BAV5(i) = BRV5Data(i).BAV;
    U5(i) = maxDisplacement(BRV5Data(i));
    dKE5(i) = absorbedEnergy(BRV5Data(i));
end


BAV8 = zeros(1,length(BRV8Data));
U8 = BAV8;
dKE8 = U8;
for i = 1:length(BRV8Data)
    BAV8(i) = BRV8Data(i).BAV;
    U8(i) = maxDisplacement(BRV8Data(i));
    dKE8(i) = absorbedEnergy(BRV8Data(i));
end


BAV10 = zeros(1,length(BRV10Data));
U10 = BAV10;
dKE10 = U10;
for i = 1:length(BRV10Data)
    BAV10(i) = BRV10Data(i).BAV;
    U10(i) = maxDisplacement(BRV10Data(i));
    dKE10(i) = absorbedEnergy(BRV10Data(i));
end



figure
hold on
plot(BAV5,U5,'r+-','MarkerSize',8, 'DisplayName','BRV = 5 mm')
plot(BAV8,U8,'b+-','MarkerSize',8, 'DisplayName','BRV = 8 mm')
plot(BAV10,U10,'g+-','MarkerSize',8, 'DisplayName','BRV = 10 mm')
hold off

legend('show')
xlabel('BAV [\circ]')
ylabel('Maximum displacement [mm]')
% ylim([3,5])
title(sprintf('Maximum displacement. SV=%d, MATV=%d, IDV=%d', SV_fix, MATV_fix, IDV_fix))


figure
hold on
plot(BAV5,dKE5/1000,'r+-','MarkerSize',8, 'DisplayName','BRV = 5 mm')
plot(BAV8,dKE8/1000,'b+-','MarkerSize',8, 'DisplayName','BRV = 8 mm')
plot(BAV10,dKE10/1000,'g+-','MarkerSize',8, 'DisplayName','BRV = 10 mm')
hold off

legend('show')
xlabel('BAV [\circ]')
ylabel('Absorbed energy [J]')
title(sprintf('Absorbed energy. SV=%d, MATV=%d, IDV=%d', SV_fix, MATV_fix, IDV_fix))
