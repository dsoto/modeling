% taperedBeamSpringConstants.m
% spring constant of a tapered beam in normal bending
% 30 December 2008 15:24:02 PST


% define constants
b = 20*10^-6;
L = 52*10^-6;
E = 1.75*10^6;
a = 0.05;

kAxial = E * b^2 / L * (a-1) / log(a);
kShear = (a - 1)^3 * b^4 * E / (6*(2*log(a) + a^2 - 4*a + 3)*L^3);

fileHandle = 1;
fprintf(fileHandle,'\n');
fprintf(fileHandle,'Base Width = %3.3f micron\n',b*10^6);
fprintf(fileHandle,'Length = %3.3f micron\n',L*10^6);
fprintf(fileHandle,'Youngs Modulus = %3.3f \n',E);
fprintf(fileHandle,'Taper Factor = %3.3f \n',a);
fprintf(fileHandle,'Axial Spring Constant = %3.3f N/m\n', kAxial);
fprintf(fileHandle,'Shear Spring Constant = %3.3f N/m\n', kShear);
fprintf(fileHandle,'\n');