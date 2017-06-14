import glob
import os
import datetime,time
import csv
import codecs

month_number = '0'
while int(month_number)>12 or int(month_number)<1:
    month_number = input('Please enter the month with numbers between 1 and 12 (ex:1,2,3): ')
    
month_dict = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun','7':'Jul','8':'Aug'
              ,'9':'Sep','10':'Oct','11':'Nov','12':'Dec'} 

path = os.path.dirname(os.path.abspath(__file__)) #get file path
create_time = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')) #create time
dcn_files=glob.glob(path+'\*.dcn') #get all .dcn file
log_files=glob.glob(path+'\*.log')  #get all .log file
csvfile = open(month_dict[month_number]+'_errors'+create_time+'.csv','a',newline='')
no_error_file = open(month_dict[month_number]+'_no_errors'+create_time+'.csv','a',newline='')
csvwriter = csv.writer(csvfile)
no_error_writer = csv.writer(no_error_file)
csvwriter.writerow(['IP','error_name','error_count'])
no_error_writer.writerow(['IP'])

total_dict = {} #total count dictionary
ipname_error_dict = {} #ipname_errorname_errorcount format dictionary
ranking_dict = {} #dictionary for ranking



#count error
def count_error(test_file):
    lines_file = test_file.readlines()       

    for i in range(len(lines_file)):
            if 'Log Buffer' in lines_file[i]:       #the error information is under the 'Log Buffer'
                index_line = i+1
                break
            
    while index_line>0:
        error_info = lines_file[index_line].split(': ')        #'time:errorname:cause' is the format of error in .log 
        if 'show run' in lines_file[index_line]:            #the error information is above on the 'show run'
            break
        if len(error_info)>2 and month_dict[month_number] in error_info[0]:
            error_name = error_info[1]                  #error_info='time:errorname:cause'
            if error_name not in error_dict:
                error_dict[error_name]=1                
            else:
                error_dict[error_name]+=1                
            if error_name not in total_dict:                
                total_dict[error_name]=1
            else:               
                total_dict[error_name]+=1
            ipname_error_dict[ip_file] =error_dict
        index_line += 1        
    index_line = 0


#write error
def write_error():    
    if error_dict:
        csvwriter.writerow([ip_file])   
        for error_name,error_count in error_dict.items():               
            csvwriter.writerow(['',error_name,error_count])
    else:
        no_error_writer.writerow([ip_file])
        

#write total error count
def write_total_error_count(total_dict):
    for total_error_name,total_error_count in total_dict.items():    
        csvwriter.writerow(['',total_error_name,total_error_count])
        
        
#write ranking error
def write_ranking_error(ranking_dict):
    for error_name,ip_count_dict in ranking_dict.items():
        ip_count_dict = sorted(ip_count_dict.items(),key=lambda x:x[1],reverse=True) #sort the error with counts
        times = 1 #ranking index
        csvwriter.writerow(['Ranking',error_name,''])
    
        for ip_name,error_count in ip_count_dict:
            if len(ip_count_dict)<11:   #display all ranking if not larger than 10
                csvwriter.writerow([times,ip_name,error_count])
                times += 1
            else:
                if times<11:    #display top ten ranking
                    csvwriter.writerow([times,ip_name,error_count])
                    times += 1
      


    
#main function
for file_name in dcn_files:
    ip_file = file_name.split('\\')[-1]
    with open(file_name,'r',encoding='utf-8') as test_file:   
        #test_file = open(file_name,'r',encoding='utf-8') #utf-8 encoding for .dcn files
        error_dict = {} #error_count format dictionary 
        index_line = 0 #the index of 'Log Buffer' line
        error_count = 0 #the count of error
        count_error(test_file)
        write_error()

for file_name in log_files:    
    ip_file = file_name.split('\\')[-1]
    csvwriter.writerow([ip_file])
    with open(file_name,'r') as test_file:
        #test_file = open(file_name,'r')
        
        
        error_dict = {} #error_count format dictionary 
        index_line = 0 #the index of 'Log Buffer' line
        error_count = 0 #the count of error
        count_error(test_file)
        write_error()        


#display total counts for each error
csvwriter.writerow(['Total errors'])
write_total_error_count(total_dict)
    

for ip_name,error_dict in ipname_error_dict.items():
    for error_name,error_count in error_dict.items():        
        if error_name not in ranking_dict:          
            ranking_dict[error_name]={}        
            if ip_name not in ranking_dict[error_name]:
                ranking_dict[error_name][ip_name]=error_count
        else:
            if ip_name not in ranking_dict[error_name]:
                ranking_dict[error_name][ip_name]=error_count



#display top ten error ip for each error
csvwriter.writerow(['Error ranking'])
write_ranking_error(ranking_dict)


    
    
