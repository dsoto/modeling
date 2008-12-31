% taperedBeamNormal.m
% plot of spring constant of a tapered beam in normal bending
% 30 December 2008 15:24:02 PST


% define constants
b = 20*10^-6;
L = 50:10:80;
L = L*10^-6;
E = 1.75*10^6;

close all;
figure;
hold on;

legendStringCells = {};
color = ['b' 'g' 'r' 'k'];
plotHandleVector = [];

for i=1:length(L)
	a = 0.0:0.01:0.99;
	k = E * b^2 / L(i) .* (a-1) ./ log(a);
	% matlab can't deal with limit a->1 so we manually put in data point
	k(length(k)+1) = E * b^2 / L(i);
	a(length(a)+1)=1.0;
	legendStringCells{i}=sprintf('length = %3.3f microns',L(i)*10^6);
	plotHandle(i) = plot(a,k,color(mod(i,4)+1));
	plotHandleVector = [plotHandleVector, plotHandle(i)];
end


legend(plotHandleVector, legendStringCells, 'FontSize', 10, ...
	'Location','SouthEast' );

ylabel('Spring Constant (N/m)')
xlabel('Taper Parameter')
%axis([0 1 0 0.2])

bString=sprintf('base = %3.3f microns',b*10^6);
eString=sprintf('Youngs Modulus = %3.3f',E);

title({'Normal Spring Constant vs. Degree of Taper';bString;eString})

formatPlot(gcf,gca,'Times New Roman',12);
printPlot(gcf,'taperedBeamPlot',4.0,3.0);

