clc;
clear;
close all;

BRV = 5;
BAV = 15;
rho = 7.85e-09;
% 2.78e-09


thickness = 1.4;
length = 200;
width = 200;
halfwidth = width/2;
height = 60;

hbend = 2 * BRV * (1-cosd(BAV));
wbend = 2 * BRV * sind(BAV);
hdiag = height - hbend;
wdiag = hdiag * tand(BAV);

halfw = (halfwidth - wdiag - wbend) + sqrt(hdiag^2 + wdiag^2) + 2 * 2 * BRV * BAV / 360;
V = 2 * halfw * length * thickness;
m = V * rho * 1000;



