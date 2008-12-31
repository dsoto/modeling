% function output = printPlot ( figureHandle, filename )

function output = printPlot ( figureHandle, filename, xSize, ySize )

% printPlot.m
% function output = printPlot ( figureHandle, filename, xSize, ySize )
% sets paper size and saves a copy of figureHandle
% with filename.pdf

%if nargin < 2 
%	filename = 'output_plot.pdf';
%end

% xSize = 8;
% ySize = 6;

set ( figureHandle, 'PaperUnits', 'inches' );
set ( figureHandle, 'PaperSize', [xSize ySize] );
set ( figureHandle, 'PaperPositionMode', 'manual' );
set ( figureHandle, 'PaperPosition', [0.0 0.0 xSize ySize] );

[pathstr, name, ext, versn] = fileparts(filename);

%plotFilename = strcat( pathstr, '/', name, '.pdf' );
plotFilename = strcat( name, '.pdf' );
saveas( figureHandle, plotFilename, 'pdf' )

plotFilename = strcat( name, '.fig' );
saveas( figureHandle, plotFilename, 'fig' )

%plotFilename = strcat( name, '.eps' );
%saveas( figureHandle, plotFilename, 'eps' )

