% taperedBeam.m
% plot of spring constant of a tapered beam in lateral bending
% see lab book 2008_1 pg. 94
% 


% define constants
b = 20*10^-6;

L = 50:10:80;
L = L*10^-6;
E = 1.75*10^6;

figure;
hold on;

legendStringCells = {};
color = ['b' 'g' 'r' 'k'];
plotHandleVector = [];

for i=1:length(L)
	a = 0.0:0.05:0.95;
	% spring constant as calculated by sage
	k=(a - 1).^3*b^4*E./(6*(2*log(a) + a.^2 - 4.*a + 3)*L(i)^3);
	% matlab can't deal with limit a->1 so we manually put in data point
	k(length(k)+1)=b^4*E/L(i)^3/4;
	a(length(a)+1)=1.0;
	legendStringCells{i}=sprintf('length = %3.3f microns',L(i)*10^6);
	plotHandle(i) = plot(a,k,color(mod(i,4)+1));
	plotHandleVector = [plotHandleVector, plotHandle(i)];
end


legend(plotHandleVector, legendStringCells, 'FontSize', 10, ...
	'Location','SouthEast' );

ylabel('Spring Constant (N/m)')
xlabel('Taper Parameter')
axis([0 1 0 0.2])
bString=sprintf('base = %3.3f microns',b*10^6);
%lString=sprintf('length = %3.3f microns',L*10^6);
eString=sprintf('Youngs Modulus = %3.3f',E);

%title({'Lateral Spring Constant vs. Degree of Taper';bString;lString;eString})
title({'Lateral Spring Constant vs. Degree of Taper';bString;eString})

formatPlot(gcf,gca,'Times New Roman',12);
printPlot(gcf,'taperedBeamPlot',4.0,3.0);

