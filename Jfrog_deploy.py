# ------------------------------------------------------------------------------------------------
# Test script name: Jfrog_deploy.py 
# Project         : L2L3-CCU
# Author 		  : thota srikanth
# purpose : This script will deploy the test reports into the Jfrog Artifactorys
#   As part following jobs handled:
#	+ api key is used for Jfrog Authentication
# 	+ required data can be fetched from the file "config_data.txt"
# 	+ config_data.txt file need to update depending on the requirement in future
# 	+ generated xml and html reports are fetching and Zipped into a folder
# ------------------------------------------------------------------------------------------------
import glob
import os
import shutil
from zipfile import ZipFile
from pathlib import Path

#fetching required data from the config_data file
with open("gen_bin/config_data.txt",'r') as f:
    for line in f:
        if(line.find("report_path") != -1):
            y = line.index("report_path")
            report_path = (line[y + 12:].rstrip())

        if (line.find("number_of_reports") != -1):
            y = line.index("number_of_reports")
            number_of_reports = (line[y + 20:].rstrip())

        if (line.find("dir_path") != -1):
            y = line.index("dir_path")
            dir_path = (line[y + 9:].rstrip())

        if (line.find("artifactory_path") != -1):
            y = line.index("artifactory_path")
            artifactory_path = (line[y + 17:].rstrip())

        if (line.find("api_key") != -1):
            y = line.index("api_key")
            api_key = (line[y + 8:].rstrip())

        if (line.find("Zip_path") != -1):
            y = line.index("Zip_path")
            Zip_path = (line[y + 9:].rstrip())
			
        if (line.find("release") != -1):
            y = line.index("release")
            release = (line[y + 8:].rstrip())

# Create the directory to store latest reports	
directory = "latest_reports"		
final_report = os.path.join(dir_path, directory) 
isExist = os.path.exists(final_report)
if not isExist:
  # Create a new directory because it does not exist 
  os.makedirs(final_report)
  print("%s directory created" % final_report)


# fetch the xml report based on time
xml_file = []
files_xml= os.path.join(report_path, '*xml')

files = sorted(glob.iglob(files_xml), key=os.path.getctime, reverse=True)

for i in range(int(number_of_reports)):
    xml_file.append(files[i])
    shutil.copy(files[i], final_report)

# fetch the html report based on time
html_file = []
files_html = os.path.join(report_path, '*html')

files = sorted(glob.iglob(files_html), key=os.path.getctime, reverse=True)

for i in range(int(number_of_reports)):
    xml_file.append(files[i])
    shutil.copy(files[i], final_report)

# zipping collected reports
reports= os.path.join(Zip_path, release)
zip_file = shutil.make_archive(reports, 'zip', final_report)

#upload files to artifactory

cmd ='curl -H "X-JFrog-Art-Api:'+api_key+'" -T '+'"'+zip_file+'"'+' "'+artifactory_path+'"'

os.system(cmd)

# remove the reports after zipping
shutil.rmtree(final_report)
print("%s directory removed" % final_report)