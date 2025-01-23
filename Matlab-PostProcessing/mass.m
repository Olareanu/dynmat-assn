function m = mass(struct)

BRV = struct.BRV;
BAV = struct.BAV;
SV = struct.SV;

if struct.MATV == 2
    rho = 2.78e-09;
    thickness = 4;
else
    rho = 7.85e-09;
    thickness = 1.4;
end

A_corr = zeros(73,1);
A_corr(3) = 2 * pi * 15^2;



length = 200;
width = 200;
halfwidth = width/2;
height = 60;

hbend = 2 * BRV * (1-cosd(BAV));
wbend = 2 * BRV * sind(BAV);
hdiag = height - hbend;
wdiag = hdiag * tand(BAV);

halfw = (halfwidth - wdiag - wbend) + sqrt(hdiag^2 + wdiag^2) + 2 * 2 * BRV * BAV / 360;


A = 2 * halfw * length - A_corr(SV);
V = A * thickness;
m = V * rho * 1000;

end