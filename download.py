# Script using wget command to download a specified service from Nexus.

# Uses wget commmand command to download xar file into current directory
# It then makes a directory called 'service' for the content of the xar to be extracted into
# After downloading the file, it unpacks the xar using the tar command
# Opens the config.xml file from the xar extraction and parses through the xml to find the appropriate name of the service 
# This is what the 'service' dir will be renamed as
# Remove the xar file from the current directory


import argparse
import os
import xml.etree.ElementTree as ET
import shutil
parser = argparse.ArgumentParser(description = "Download Service Script")
parser.add_argument('url', type = str, help = "URL of where to download file")
args = parser.parse_args()

#wget command with url input from command line
wget_command = "sudo wget --user interns@1degreeworld.com --ask-password -O service.xar " + args.url

# make directory called 'service' here
mkdir_command = "sudo mkdir service"

# extract contents from xar file and place into the 'service' dir
tar_command = "sudo tar -xf service.xar -C ./service"

os.system(wget_command + " && " + mkdir_command + " && " + tar_command)


curr_dir = os.getcwd()
os.chdir(curr_dir + "/service")

#open the config.xml file in the 'service' dir
fp = open("config.xml","r")
element = ET.parse(fp)

# parse the xml file and find the appropriate name of the service
namespace = "{http://www.neeveresearch.com/schema/x-ddl}"
e = element.findall('{0}systemDetails/{0}name'.format(namespace))

for i in e:
    # New name of service directory
    new_directory = i.text


# go back to the systems directory
os.chdir("..")

old_directory = curr_dir + "/service"
new_directory = curr_dir + "/" + new_directory

# Rename 'service' directory to the appropriate name for the service
os.rename(old_directory, new_directory)

#delete the downloaded xar file
os.system("sudo rm service.xar")
