function Plot_Mean_Heatmap(TMin,TMax)

% Radius
Rad = 3; 

%Colorbar scaling
cmin = 0;
cmax = 4; 

%Load data
[FileName,PathName,FilterIndex] = uigetfile;
Fish_Data = load([PathName,FileName]);

warning off

TMin1=round(Fish_Data.Fish{1}.Sampling_Rate*TMin);
TMax1=round(Fish_Data.Fish{1}.Sampling_Rate*TMax);

Time_spent = zeros(33,80, length(Fish_Data.Fish));

for ii = 1:length(Fish_Data.Fish)
    clear X Y
    
    disp(['Fish..',int2str(ii)]);
    
    %Extract time spent per fish and then combine
    X = [Fish_Data.Fish{ii}.X(TMin1:TMax1)];
    Y = [Fish_Data.Fish{ii}.Y(TMin1:TMax1)];
    
    XY = [X;Y];
    
    for jj = 1:length(XY)
        if round(XY(1,jj)) == 0 || round(XY(2,jj)) == 0
            continue;
        end
        Time_spent(round(XY(1,jj)), round(XY(2,jj)), ii) = Time_spent(round(XY(1,jj)), round(XY(2,jj)), ii) + 1;
    end
end

% Average time spent
Mean_Time_spent = squeeze(mean(Time_spent,3));

% Filter it
S=+(bwdist(padarray(1,[1,1]*double(round(Rad*1.5))))<=Rad);
Filt_Time_spent=double(convn(Mean_Time_spent,S,'same'));
Filt_Time_spent = smoothn(Filt_Time_spent,5);


%Plot figure and save
Result_Folder = [PathName, 'Figures/'];
mkdir(Result_Folder);

fs2 = figure(2);
set(fs2,'color','white')
pcolor((Filt_Time_spent(1:33,1:80)./Fish_Data.Fish{1}.Sampling_Rate)')
caxis([cmin cmax]) % Colorbar setting
colormap(jet(2000))
shading interp
set(gcf,'Position',[350,300, 2*180, 2*380]);
set(gca, 'TickDir','out', 'FontSize',12)
box off
set(gca, 'YDir','reverse')
xlabel('x distance (mm)', 'FontSize',12);
ylabel('y distance (mm)', 'FontSize',12);


name_file = ['Fish_Average_Heat Map'];

set(gcf, 'PaperPositionMode','auto','InvertHardCopy', 'off')
saveas(fs2, [Result_Folder, name_file], 'jpg');