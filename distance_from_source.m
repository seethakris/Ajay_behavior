function distance_from_source(TMin, TMax)

%Load data
[FileName,PathName,FilterIndex] = uigetfile;
Fish_Data = load([PathName,FileName]);

warning off

%Convert time to frames
TMin1=round(Fish_Data.Fish{1}.Sampling_Rate*TMin);
TMax1=round(Fish_Data.Fish{1}.Sampling_Rate*TMax);

for ii = 1:length(Fish_Data.Fish)
    %Extract time spent per fish and then combine
    X = [Fish_Data.Fish{ii}.X(TMin1:TMax1)];
    Y = [Fish_Data.Fish{ii}.Y(TMin1:TMax1)];
    
    XY = [X;Y];
    
    %Find dist form source as a pythogoras distance. 
    for jj = 1:length(XY)
        Dist_from_source(jj,ii) = sqrt(XY(1,jj).^2 + XY(2,jj).^2);
    end
    
    Mean_Dist(ii) = mean(Dist_from_source(:,ii),1);
    Median_Dist(ii) = median(Dist_from_source(:,ii),1);
    STD_Dist(ii) = std(Dist_from_source(:,ii),[],1);
    
end


Mat_Dat.Mean_Dist = Mean_Dist;
Mat_Dat.Median_Dist = Median_Dist;
Mat_Dat.STD_Dist = STD_Dist;


% Save filename
prompt = {'Enter file name for saving:'};
dlg_title = 'Input';
num_lines = 1;
answer = inputdlg(prompt,dlg_title,num_lines);

%Save as matfile
column_names = fieldnames(Mat_Dat)';
save([PathName,answer{1},'.mat'], 'Mat_Dat', 'column_names');

%Save Parameters for all fish
Temp_Dat = fieldnames(Mat_Dat);
filename = [PathName,answer{1},'.xls'];
fid = fopen(filename, 'w+');

for kk = 1:length(Temp_Dat)
    Xls_Dat{1,kk} = Temp_Dat{kk};
    for ii = 1:size(Mat_Dat.(Temp_Dat{kk}),2)
        temp1 = Mat_Dat.(Temp_Dat{kk})(ii);
        if temp1 ~= 0
            Xls_Dat{ii+1,kk} = temp1;
        else
            Xls_Dat{ii+1,kk} = 0;
        end
    end
    
end

%Save as excel
fid = fopen(filename, 'a');
[nrows,ncols]= size(Xls_Dat);



for row = 1:nrows
    for col = 1:ncols
        if row == 1
            fprintf(fid, '%s\t', Xls_Dat{row,col});
        else
            fprintf(fid, '%4.2f\t', Xls_Dat{row,col});
        end
    end
    fprintf(fid, '\n');
end




