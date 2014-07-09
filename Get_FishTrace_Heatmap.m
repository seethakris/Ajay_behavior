function obj = Get_FishTrace_Heatmap(FileName, FishNum)

%% Get data from fish

Import.DATA=importdata(FileName);

if FishNum==1
    X=Import.DATA.Tracker.cXmm001.data;
    Y=Import.DATA.Tracker.cYmm001.data;
    if isfield(Import.DATA.Tracker, 'FBSA001')
        ROI_whole = Import.DATA.Tracker.FBSA001.data;
        obj.trigger_ROI_whole = double(ROI_whole);
    end
    if isfield(Import.DATA.Tracker, 'FBSA003')
        ROI_1 = Import.DATA.Tracker.FBSA003.data;
        obj.trigger_ROI1 = double(ROI_1);
    end
    if isfield(Import.DATA.Tracker, 'FBSA005')
        ROI_2 = Import.DATA.Tracker.FBSA005.data;
        obj.trigger_ROI2 = double(ROI_2);
    end
    
elseif FishNum==2
    X=Import.DATA.Tracker.cXmm002.data;
    Y=Import.DATA.Tracker.cYmm002.data;
    if isfield(Import.DATA.Tracker, 'FBSA002')
        ROI_whole = Import.DATA.Tracker.FBSA002.data;
        obj.trigger_ROI_whole = double(ROI_whole);
    end
    if isfield(Import.DATA.Tracker, 'FBSA004')
        ROI_1 = Import.DATA.Tracker.FBSA004.data;
        obj.trigger_ROI1 = double(ROI_1);
    end
    if isfield(Import.DATA.Tracker, 'FBSA006')
        ROI_2 = Import.DATA.Tracker.FBSA006.data;
        obj.trigger_ROI2 = double(ROI_2);
    end
end

Diff_Time = double(Import.DATA.Tracker.Timestamp.data(end) - min(Import.DATA.Tracker.Timestamp.data))/1000;

obj.Sampling_Rate = 1/(Diff_Time/size(Import.DATA.Tracker.Timestamp.data,2));

obj.X=double(X);
obj.Y=double(Y);
obj.XMax=max(X);
obj.YMax=max(Y);
obj.T=double(Import.DATA.Tracker.Timestamp.data)/1000;

dX=obj.X(2:end)-obj.X(1:end-1);
dY=obj.Y(2:end)-obj.Y(1:end-1);
dT=obj.T(2:end)-obj.T(1:end-1);

VX=dX./dT;
VY=dY./dT;
obj.V=sqrt(VX.^2+VY.^2);


obj.NFish=1;



