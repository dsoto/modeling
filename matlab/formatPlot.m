function output = formatPlot ( figureHandle, axesHandle, fontName, fontSize )
% formatPlot.m
% function output = formatPlot ( figureHandle, axesHandle, fontName, fontSize )
% applies formatting to figureHandle and axesHandle


%fontSize   = 24;
%fontName   = 'Times New Roman';
fontWeight = 'Normal';
axesProps  = get(axesHandle);

set ( axesHandle, 'FontSize', fontSize );
set ( axesHandle, 'FontName', fontName );
set ( axesHandle, 'FontWeight', fontWeight );
set ( axesHandle, 'Box', 'on' );

xHandle     = axesProps.XLabel;
yHandle     = axesProps.YLabel;
titleHandle = axesProps.Title;

set(xHandle,    'FontName',   fontName,...
                'FontSize',   fontSize,...
                'FontWeight', fontWeight);
set(yHandle,    'FontName',   fontName,...
                'FontSize',   fontSize,...
                'FontWeight', fontWeight);
set(titleHandle,'FontName',fontName,...
                'FontSize',   fontSize,...
                'FontWeight', fontWeight);
