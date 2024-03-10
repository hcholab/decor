x = 1:1.5:100;
y = sin(x/10);
p1 = polyfit(x,y,1);
p2 = polyfit(x,y,2);
p4 = polyfit(x,y,4);
p3 = polyfit(x,y,3);
p5 = polyfit(x,y,5);
hf = figure();
hold on; % ensure all plots are held

original = plot(x,y,'k.', 'LineWidth', 1.3);
line1 = plot(x,polyval(p1,x),'r', 'LineWidth', 1.3);
line2 = plot(x,polyval(p2,x),'g', 'LineWidth', 1.3);
line3 = plot(x,polyval(p3,x),'color',[1 .5 0], 'LineWidth', 1.3);
line4 = plot(x,polyval(p4,x),'b', 'LineWidth', 1.3);

%line5 = plot(x,polyval(p5,x),'m', 'LineWidth', 1.3);


grid on;
box on

% Set y-axis limits
ylim([-1.5 1.5]);

% Adding a legend with LaTeX strings inside the graph
%h = legend([original, line1, line2, line3, line4], {"data", "d=1", "d=2", "d=3", "d=4"}, "location", "southwest");
%set(h, "interpreter", "latex"); % set the interpreter for the legend text to latex

% other plot adjustments
% set(gca,'xaxislocation','zero');
% set(gca,'yaxislocation','zero');



print('curve_fitting.svg');
print(hf, "curve_fitting.pdf", "-dpdflatexstandalone");
system("pdflatex curve_fitting");

