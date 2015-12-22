function save_triggers_in_excel
%% Plot how many times fish triggered odors

% Time bins in ms
Bin_lengths = {'0-250', '250-1000', '1000-2000', '2000-5000', '5000-15000'};

% Get bins
for ii = 1:length(Bin_lengths)
    Start(ii) = str2double(Bin_lengths{ii}(1:strfind(Bin_lengths{ii},'-')-1)) ;
    End(ii) = str2double(Bin_lengths{ii}(strfind(Bin_lengths{ii},'-')+1:end)) ;
end

Start(end+1) = End(end);
Bin_lengths{end+1} = ['> than ' , int2str(End(end))];

%Load data
[FileName,PathName,FilterIndex] = uigetfile;
Fish_Data = load([PathName,FileName]);

warning off

count = 1; %count number of fish
%Plot figures for each fish
for ii = 1:length(Fish_Data.Fish)
    
    disp(['Fish..',int2str(ii)]);
    
    %Extract time spent
    obj = Fish_Data.Fish{ii};
    
    % If there are bins more than what user has specified for last column -
    % use sampling rate and largest possible bin. 
    Bins_for_sorting = [Start, obj.T(end)*1000]; 

    %% Get time taken for different triggers - Do ROI 1 and ROI2 seperately
    for jj = 1:2 %Seperate ROI 1 and 2
        
        if jj == 1
            trigger = obj.trigger_ROI1; %1-trigger, 0-no trigger
            label_exp(count) = {['Fish ', int2str(ii), ' ROI1']};
        else
            trigger = obj.trigger_ROI2;
            label_exp(count) = {['Fish ', int2str(ii), ' ROI2']};
        end
        number_of_triggers(count) = length(find(trigger==1)) * (1/obj.Sampling_Rate) ; %Total time triggering
        trigger = sprintf('%d',trigger); %convert to string
        num_consec = textscan(trigger,'%s','delimiter','0','multipleDelimsAsOne',1); %use 0 as delimiter and find number of consecutive 1s
        num_consec = num_consec{:}; %Convert cell to array
        
        % Do only if trigggers exist
        if isempty(num_consec)
            bincounts(count, 1:length(Start)) = 0;
            
        else              
            %Get length of triggers in ms and divide into bins
            length_num_consec = [];
            length_num_consec_in_ms =[];
            for kk = 1:length(num_consec)
                length_num_consec(kk) = length(num_consec{kk});
                length_num_consec_in_ms(kk) = length_num_consec(kk)*(1/obj.Sampling_Rate)*1000;
            end
            % Sort into bins
            bincounts(count, :) = histc(length_num_consec_in_ms, Bins_for_sorting);
        end
        
        count = count + 1;
        
    end
end

%% Save all as excel
%Create headings
column_names = {'Fish ID', Bin_lengths{:}, 'Total trigger time (s)'};
filename = [PathName,FileName(1:end-4),'_Trigger_time_in_bins.xls'];

for ii = 1:length(column_names)
    Xls_Dat{1,ii} = column_names{ii};
end
for ii = 1:count-1
    Xls_Dat{ii+1,1} = label_exp{ii};
    for jj = 1:length(Bin_lengths)
        Xls_Dat{ii+1,jj+1} = bincounts(ii,jj);
    end
    Xls_Dat{ii+1,1+length(Start)+1} = number_of_triggers(ii);
end

%Save as excel
fid = fopen(filename, 'w+');
[nrows,ncols]= size(Xls_Dat);

for row = 1:nrows
    for col = 1:ncols
        if row == 1
            fprintf(fid, '%s\t', Xls_Dat{row,col});
        elseif col == 1
            fprintf(fid, '%s\t', Xls_Dat{row,col});
        else    
            fprintf(fid, '%4.3f\t', Xls_Dat{row,col});
        end
    end
    fprintf(fid, '\n');
end


