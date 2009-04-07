% lumped parameter modeling
% March 28, 2008 1:10:05 PM PDT

%create trajectory file
%feed into lumped parameter model
%output time trace and force space curves

%refinement : add contact diode relationship for sliding friction and adhesion

% define force expressions

% create trajectory

% set preload depth
% set preload angle

clear all;

preloadDepth = 100;     % in microns
dragLength   = 600;     % in microns
timeStep     = 0.01;   % in seconds

l = 200; % in microns
kt = .1; % in newton * meter
ks = 1; % in newton / meter

% angles in units of radians
angle(1) = -30 / 180 * pi; % preloadAngle
angle(2) =   0 / 180 * pi; % dragAngle
angle(3) =  90 / 180 * pi; % pulloffAngle

% velocities in units of microns per second
velocity(1) = 100; % preloadVelocity
velocity(2) = 100; % dragVelocity
velocity(3) = 100; % pulloffVelocity

% times in units of seconds
% duration of each phase of LDP
duration(1) = preloadDepth / velocity(1);
duration(2) = dragLength / velocity(2);
duration(3) = preloadDepth / velocity(3);

% duration of entire LDP
durationTotal = sum(duration);

% vector of discrete time values
% currently no checking for roundoff values of time...
time = [0:timeStep:durationTotal];

beginPreloadIndex = 2;
endPreloadIndex = duration(1) / timeStep + 1;
beginDragIndex = endPreloadIndex + 1;
endDragIndex = (duration(1)+duration(2)) / timeStep + 1;
beginPulloffIndex = endDragIndex + 1;
beginPulloffIndex = endDragIndex;

endPulloffIndex = (duration(1)+duration(2)+duration(3)) / timeStep + 1;
endPulloffIndex = endDragIndex;

% no pulloff hack
velocity(3) = 0;

i = 1;
x(i,1) = 0;
x(i,2) = 0;
x(i,3) = 0;
t(i) = 0;


for i = beginPreloadIndex:endPreloadIndex
	x(i,1) = velocity(1) * cos(angle(1)) * timeStep + x(i-1,1);
	x(i,2) = velocity(1) * sin(angle(1)) * timeStep + x(i-1,2);
end

for i = beginDragIndex:endDragIndex
	x(i,1) = velocity(2) * cos(angle(2)) * timeStep + x(i-1,1);
	x(i,2) = velocity(2) * sin(angle(2)) * timeStep + x(i-1,2);
end

for i = beginPulloffIndex:endPulloffIndex
	x(i,1) = velocity(3) * cos(angle(3)) * timeStep + x(i-1,1);
	x(i,2) = velocity(3) * sin(angle(3)) * timeStep + x(i-1,2);
end

% plot(x(:,1),x(:,2))


shearDisplacement = x(:,1);
normalDisplacement = x(:,2);
ds = shearDisplacement;
dn = normalDisplacement;
dn = -dn;


% equations for rigid wedge atop torsional spring
%normalForce = kt*asin(ds/l).*ds/l^2 + ks.*(sqrt(l^2-ds.^2)-l-dn);
%shearForce = kt*asin(ds/l).*sqrt(l^2-ds.^2)/l^2;


% equations for linear spring atop torsional spring
% this is the TE model
lf = sqrt(ds.^2+(l-dn).^2);
theta = asin(ds./lf);
normalForceTorsion = kt*theta.*ds./lf.^2;
normalForceLinear = -ks*(lf-l).*(l-dn)./lf;
shearForceTorsion = kt*theta.*(l-dn)./lf.^2;
shearForceLinear = ks*(lf-l).*ds./lf;
normalForce = normalForceTorsion + normalForceLinear;
shearForce = shearForceTorsion + shearForceLinear;

subplot(1,2,1)
plot(shearForce,normalForce,'kx')
titleString = sprintf('force space length=%3.0f k_s=%3.1f k_t=%3.1f',l,ks,kt);
title(titleString)

subplot(1,2,2)
plot(x(:,1),x(:,2),'kx')
title('trajectory')


return;



subplot(1,2,1)
plot(normalForceLinear,'kx')
subplot(1,2,2)
plot(lf/l,'kx')

return;


% plot trajectory

plot(displacementX, displacementY)

% loop through trajectory displacement data
	% create error checking for displacement limits
	% is shear displacement greater than length of lever?
	% then shear displacement and shear force is fixed
	% this could also be due to angle constraint
	
	% output time, displacement, and forces to matrix

% display data in force time trace graph	
% display data in force space graph