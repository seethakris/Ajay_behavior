function get_distance_from_tankedge(TMin,TMax, tank_xmm, tank_ymm)
%% Gets distance of fish from edges
%% Input
%TMin - start time
%TMax - end time
%tank_xmm - x dimensions of tank in mm
%tank_ymm - y dimensions of tank in mm

warning off

%Load data
[FileName,PathName,FilterIndex] = uigetfile;
Fish_Data = load([PathName,FileName]);

%Convert seconds to frame
TMin1=round(Fish_Data.Fish{1}.Sampling_Rate*TMin);
TMax1=round(Fish_Data.Fish{1}.Sampling_Rate*TMax);


for ii = 1:length(Fish_Data.Fish)
    
    clear X Y
    
    disp(['Fish..',int2str(ii)]);
    
    %Extract time spent per fish and then combine
    X = [Fish_Data.Fish{ii}.X(TMin1:TMax1)];
    Y = [Fish_Data.Fish{ii}.Y(TMin1:TMax1)];
    
    %Get perpendicular distances from each side of tank
    top_tank = [X;zeros(1,size(X,2))];
    bottom_tank = [X; repmat(tank_ymm,1,size(X,2))];
    left_tank = [zeros(1,size(Y,2)); Y];
    right_tank = [repmat(tank_xmm,1,size(X,2)); Y];
    
    %Get distances - col1:top, col2:bottom, col3:left, col4:right
    distances(:,1) = sqrt((X-top_tank(1,:)).^2 + (Y-top_tank(2,:)).^2);
    distances(:,2) = sqrt((X-bottom_tank(1,:)).^2 + (Y-bottom_tank(2,:)).^2);
    distances(:,3) = sqrt((X-left_tank(1,:)).^2 + (Y-left_tank(2,:)).^2);
    distances(:,4) = sqrt((X-right_tank(1,:)).^2 + (Y-right_tank(2,:)).^2);
    
    %get minimum distance from the edges 
    [minimum_dist, minimum_dist_idx] =  min(distances, [], 2);
    Dat(ii).mean_dist = mean(minimum_dist);
    Dat(ii).median_dist = median(minimum_dist);
    
end

%Save files in excel
Temp_Dat = fieldnames(Dat);
for kk = 1:length(Temp_Dat)
    Xls_Dat{1,kk} = Temp_Dat{kk};
    for jj = 1:length(Dat)
        Xls_Dat{jj+1,kk} = eval(['Dat(jj).',Temp_Dat{kk}]);
    end
end

[nrows,ncols]= size(Xls_Dat);
filename = [PathName,'Distance_from_tankedge.xls'];
fid = fopen(filename, 'w+');

for col = 1:ncols
    fprintf(fid, '%s\t', Xls_Dat{1,col});
end

for row = 2:nrows
    fprintf(fid, '\n');
    for col = 1:ncols
        fprintf(fid, '%3.3f\t', Xls_Dat{row,col});
    end
end

fclose(fid);




