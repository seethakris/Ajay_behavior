function LoadData_Heatmap

%% Load Data

FolderName=uigetdir;
List=what(FolderName);
MatFiles=List.mat;
iMax=length(MatFiles);
Fish=cell(2*iMax,1);
count = 1;

for i=1:iMax
    if ~strncmpi(MatFiles{i}, '.',1)
        Import.DATA=importdata([FolderName,'/',MatFiles{i}]);
        
        if isfield(Import.DATA,'Tracker')
            
            Fish{2*count-1}=Get_FishTrace_Heatmap([FolderName,'/',MatFiles{i}],1);
            F1=num2str(2*count-1);
            Fish{2*count}=Get_FishTrace_Heatmap([FolderName,'/',MatFiles{i}],2);
            F2=num2str(2*count);
            disp(['Fish{',F1,'} = Fish 001: ',MatFiles{i}]);
            disp(['Fish{',F2,'} = Fish 002: ',MatFiles{i}]);
            
            count = count+1;
        end
    end
end

Fish = Fish(~cellfun('isempty',Fish));

% Save filename
prompt = {'Enter file name for saving:'};
dlg_title = 'Input';
num_lines = 1;
answer = inputdlg(prompt,dlg_title,num_lines);

save([FolderName,'/',answer{1},'.mat'], 'Fish');



