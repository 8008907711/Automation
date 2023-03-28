#Test Script Name :jfrog_resolve.py
#Author           :Srikanth Thota
#Modified Date    :15/09/2022
#Purpose          :This file will download the binaries from Jfrog artifactory  
#                  inputs will be fetch from the config_data.txt
#-----------------------------------------------------------------------------------
import os
import zipfile
from os import listdir, rmdir
from os.path import join
from shutil import move

#fetching data from the config file
with open("config_data.txt",'r') as f:
    for line in f:
         if (line.find("api_key") != -1):
            y = line.index("api_key")
            api_key = (line[y + 8:].rstrip())
       
         if (line.find("Binaries_path") != -1):
            y = line.index("Binaries_path")
            Binaries_path  = (line[y + 14:].rstrip())
            
         if (line.find("Jfrog_url") != -1):
            y = line.index("Jfrog_url")
            Jfrog_url  = (line[y + 10:].rstrip())   
            
         if (line.find("release") != -1):
            y = line.index("release")
            release  = (line[y + 8:].rstrip())
 
#release version creation creation from release name
tail = "_mcu"
extension = ".zip"
release_mcu_ext = ''+release+''+tail+''+extension+''
release_mcu = ''+release+''+tail+''

#Creating Directory if not exist
c_drive = 'C:/'
final_path = os.path.join(c_drive, Binaries_path) 
isExist = os.path.exists(final_path)
if not isExist:
  # Create a new directory because it does not exist 
  os.makedirs(final_path)
  print("%s directory created" % final_path)
 			
#****************************************************************************************************************************************************************************************************
#                                                                   Downloading MCU Binaries
#****************************************************************************************************************************************************************************************************

#commad to download the MCU Biaries from the artifactory
cmd_mcu = 'cd '+Binaries_path +' && curl -s --retry 9999 --retry-delay 3 --speed-limit 2048 --speed-time 10 --retry-max-time 0 -C - -H "X-JFrog-Art-Api:'+api_key+'" -O '+Jfrog_url+''+release_mcu_ext+''
os.system(cmd_mcu)

#MCU Binaries Path
Bin_directory = "Mcu_Binaries"	
destination = ''+final_path+'/'+Bin_directory+''
os.chdir(Binaries_path) # change directory from working dir to dir with files

for item in os.listdir(Binaries_path): # loop through items in dir
    if item.endswith(extension): # check for ".zip" extension
        file_name = os.path.abspath(item) # get full path of files
        #file_name = Binaries_path + "/" + item
        zip_ref = zipfile.ZipFile(file_name) # create zipfile object
        zip_ref.extractall(destination) # extract file to dir
        zip_ref.close() # close file
        os.remove(file_name) # delete zipped file   
        print("MCU binaries stored in directory",destination)
		
#Moving the biaries to the 'Mcu_Binaries' Directory	
for filename in listdir(join(destination, ''+release_mcu+'')):
    move(join(destination, ''+release_mcu+'', filename), join(destination, filename))
rmdir(join(destination, ''+release_mcu+''))
        
#****************************************************************************************************************************************************************************************************
        






