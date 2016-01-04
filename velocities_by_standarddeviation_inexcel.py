function velocities_by_standarddeviation_inexcel_Version1_3

% Divide velocities per fish, by the standard deviation above and
% below mean, for different time bins specified by user.
% Frames are currently being converted to seconds

%% User input
Standard_deviations = [-1, -2, -5, 0, 1, 2, 5];
Freezing_Bouts = [1,2,3,4,5]; %in seconds
TMin = 10; %in seconds
TMax = 1000; %in seconds
Frames_for_one_event = 1; %How many frames for 1 event to be classified

%% Algorithm

%Load data
[FileName,PathName,FilterIndex] = uigetfile;
Fish_Data = load([PathName,FileName]);

TMin1=round(Fish_Data.Fish{1}.Sampling_Rate*TMin);
TMax1=round(Fish_Data.Fish{1}.Sampling_Rate*TMax);

warning off

count = 1; %count number of fish
%Plot figures for each fish
for ii = 1:length(Fish_Data.Fish)
    
    disp(['Fish..',int2str(ii)]);
    
    label_exp(count) = {['Fish ', int2str(ii)]};
    count = count+1;
    
    
    %Extract velcoity of fish over the time bin
    V = [Fish_Data.Fish{ii}.V(TMin1:TMax1)];
    Sampling_Rate = round(Fish_Data.Fish{ii}.Sampling_Rate);
    
    % Convert Velcoity from mm/frame to mm/sec
    count1 = 1;
    for vv = 1:Sampling_Rate:length(V)
        if vv+Sampling_Rate>length(V)
            break;
        end
        V_seconds(count1) = sum(V(vv:vv+Sampling_Rate-1));
        count1 = count1+1;
    end
    
    V_nozeros = V(V~=0); %Find V without 0
    
    mean_V(ii) = mean(V_seconds);
    std_V(ii) = std(V_seconds);
    if ii == 1
        mean_std_column_title = {'Mean_Velocity (mm/sec)', 'Std_Velocity (mm/sec)'};
    end
    fprintf('Mean Velocity is ...%0.3f \nStandard Deviation of velocity is ...%0.3f\n', mean_V(ii), std_V(ii));
    
    %% Plot figure and save into figures folder
    plot_histogram_with_mean_and_std(PathName, ii, V_seconds, mean_V(ii), std_V(ii))
    
    %% Count bins of freezing according to user defined bins
    if ii == 1
        freezing_column_title = Freezing_excel_column_title(Freezing_Bouts);
    end
    Number_freezing_events(ii,:) = get_freezingbouts(Freezing_Bouts, V_seconds, freezing_column_title);
    
    %% Count bins of velocity according to user defined standard deviation
    Standard_deviations = sort(Standard_deviations);
    if ii == 1
        std_column_title = standard_deviation_excel_column_title(Standard_deviations);
    end
    Number_of_standardeviation_events(ii, :) = get_velocity_by_standard_deviation(Standard_deviations, Frames_for_one_event, V_seconds, mean_V(ii), std_V(ii), std_column_title);
    
end
create_excel(PathName, FileName, label_exp, mean_std_column_title, std_column_title, freezing_column_title, Number_of_standardeviation_events, Number_freezing_events, mean_V, std_V)
end

%% Get number of events for user defined freezing bouts per fish
function Events = get_freezingbouts(Freezing_Bouts, Velocity, column_title)

V_freezing = Velocity==0; %make all freezing events (V=0) into 1 to find them using delimiter method
V_freezing = sprintf('%d',V_freezing); %convert to string
num_consec = textscan(V_freezing,'%s','delimiter','0','multipleDelimsAsOne',1); %use 0 as delimiter and find number of consecutive 1s
num_consec = num_consec{:}; %Convert cell to array

length_num_consec = [];
for kk = 1:length(num_consec)
    length_num_consec(kk) = length(num_consec{kk});
end

for jj = 1:length(column_title)
    if isempty(length_num_consec)
        Events(jj) = 0;
    elseif jj == length(column_title)
        Events(jj) = size(find(length_num_consec > Freezing_Bouts(end)),2);
    else
        Events(jj) = size(find(length_num_consec == Freezing_Bouts(jj)),2);     
    end
end
end

%% Get velocity per user defined standard deviation bin and return velocity per fish
function Events = get_velocity_by_standard_deviation(Standard_deviations, Frames_for_one_event, Velocity, mean_velocity, std_velocity, column_title)
for jj = 1:length(Standard_deviations)
    if jj == 1
        threshold_min = [];
        threshold_max = (mean_velocity + Standard_deviations(jj+1) * std_velocity);
        Events(jj) = get_events_for_given_std_of_velocity(Velocity, threshold_min, threshold_max,Frames_for_one_event,column_title{jj});
    elseif jj ~= length(Standard_deviations)
        threshold_min = (mean_velocity + Standard_deviations(jj) * std_velocity);
        threshold_max = (mean_velocity + Standard_deviations(jj+1) * std_velocity);
        Events(jj) = get_events_for_given_std_of_velocity(Velocity, threshold_min, threshold_max,Frames_for_one_event,column_title{jj});
    else
        threshold_min = (mean_velocity + Standard_deviations(jj) * std_velocity);
        threshold_max = [];
        Events(jj) = get_events_for_given_std_of_velocity(Velocity, threshold_min, threshold_max,Frames_for_one_event,column_title{jj});
    end
end
end


%% Get number of events in each velocity bin
function Number_bins = get_events_for_given_std_of_velocity(Velocity, threshold_min, threshold_max, Frames_for_events, Current_Std)
% Get velocity as a binary number
if isempty(threshold_max)
    V_std = Velocity >= threshold_min;
elseif isempty(threshold_min)
    V_std = Velocity <= threshold_max;
else
    V_std = (Velocity >= threshold_min & Velocity<=threshold_max);
end

if any(V_std)
    V_std = sprintf('%d',V_std); %convert to string
    num_consec = textscan(V_std,'%s','delimiter','0','multipleDelimsAsOne',1); %use 0 as delimiter and find number of consecutive 1s
    num_consec = num_consec{:}; %Convert cell to array
    
    length_num_consec = [];
    events = 0;
    for kk = 1:length(num_consec)
        length_num_consec = length(num_consec{kk});
        events = events + fix(length_num_consec/Frames_for_events);
        %         disp(['Length.. ' , int2str(length_num_consec), ' Events in there.. ', int2str(fix(length_num_consec/Frames_for_events)) ,' Total Event therefore..', int2str(events)])
    end
    
    Number_bins = events;
    disp(['Total Events for ', Current_Std, ' between ', int2str(threshold_min), ' and ', int2str(threshold_max), ' is....', int2str(Number_bins)])
else
    Number_bins = 0;
end

end

%% Function for plotting velocity histograms
function plot_histogram_with_mean_and_std(Result_Path, Fish_number, Velocity, mean_velocity, std_velocity)
fs = figure(1);
set(fs,'color','white','visible','off');
hist(Velocity,10);
line([mean_velocity, mean_velocity],get(gca,'YLim'),'Color',[1 0 0], 'linestyle', '-.', 'linewidth', 2);
line([mean_velocity-std_velocity, mean_velocity-std_velocity],get(gca,'YLim'),'Color',[0 1 1], 'linestyle', '-', 'linewidth', 2);
line([mean_velocity+std_velocity, mean_velocity+std_velocity],get(gca,'YLim'),'Color',[1 0 1], 'linestyle', '-', 'linewidth', 2);
legend({'histogram of velocity', 'mean', 'mean-std', 'mean+std'});
set(gca, 'TickDir','out')
xlabel('Velocity mm/frame','FontSize',12)
ylabel('Number','FontSize',12)
box off
%Save figures
Result_Folder = [Result_Path, 'Figures/Velocity/'];
mkdir(Result_Folder);

name_file = ['Velocity_histogram','_','Fish_',int2str(Fish_number)];
print(fs, '-djpeg', [Result_Folder, name_file]);
end

%% Get column titles for user defined times for freezing bouts in excel
function column_title = Freezing_excel_column_title(Freezing_Bouts)
for jj = 1:length(Freezing_Bouts)
    column_title{jj} = [int2str(Freezing_Bouts(jj)) , ' sec'];
end
column_title{jj+1} = ['> than ' , int2str(Freezing_Bouts(jj)) , ' sec'];
end

%% Get column titles for user defined standard deviation bins in excel
function column_title = standard_deviation_excel_column_title(Standard_deviations)
for jj = 1:length(Standard_deviations)
    if jj == 1
        column_title{jj} = ['< than ' , int2str(Standard_deviations(jj)) , ' STD'];
    elseif jj ~= length(Standard_deviations)
        column_title{jj} = [int2str(Standard_deviations(jj)) , ' STD to ' , int2str(Standard_deviations(jj+1)) , ' STD'];
    else
        column_title{jj} = ['> than ' , int2str(Standard_deviations(jj)) , ' STD'];
    end
end
end

%% Save as excel
function create_excel(PathName, FileName, Fish_number, Column_title_for_mean, Column_title_for_std,  Column_title_for_freezing,  Velocity_events, Freezing_events, mean_velocity, std_velocity)

%Create headings
column_names = {'Fish ID', Column_title_for_mean{:}, ' ', Column_title_for_std{:}, ' ', Column_title_for_freezing{:}};
filename = [PathName,FileName(1:end-4),'_velocity_related_events.xls'];

index_std = cellfun('length',regexp(column_names,Column_title_for_std{1})) == 1;
Xls_Dat{1,index_std} = 'Velocity events by Standard Deviation';

index_freezing = cellfun('length',regexp(column_names,Column_title_for_freezing{1})) == 1;
Xls_Dat{1,index_freezing} = 'Freezing Events by Length';

row_count = 2;

for ii = 1:length(column_names)
    Xls_Dat{row_count,ii} = column_names{ii};
end

for ii = 1:length(Fish_number)
    Xls_Dat{ii+row_count,1} = Fish_number{ii};
    Xls_Dat{ii+row_count,2} = mean_velocity(ii);
    Xls_Dat{ii+row_count,3} = std_velocity(ii);
    
    col_count = 4;
    for jj = 1:length(Column_title_for_std)
        col_count = col_count+1;
        Xls_Dat{ii+row_count,col_count} = Velocity_events(ii,jj);
    end
    
    col_count = col_count+1; %Leave a column gap between Standard deviation and freezing
    
    for jj = 1:length(Column_title_for_freezing)
        col_count = col_count+1;
        Xls_Dat{ii+row_count,col_count} = Freezing_events(ii,jj);
    end
end

%Save as excel
fid = fopen(filename, 'w+');
[nrows,ncols]= size(Xls_Dat);

for row = 1:nrows
    for col = 1:ncols
        if row == 1 || row == 2
            fprintf(fid, '%s\t', Xls_Dat{row,col});
        elseif col == 1
            fprintf(fid, '%s\t', Xls_Dat{row,col});
        elseif col == 2 || col == 3
            fprintf(fid, '%4.3f\t', Xls_Dat{row,col});
        else
            fprintf(fid, '%d\t', Xls_Dat{row,col});
        end
    end
    fprintf(fid, '\n');
end

end
