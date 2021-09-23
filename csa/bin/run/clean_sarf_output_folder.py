__author__ = 'sremanda'
__version__ = '1.0'

#Import necessary modules
import os
import sys

#Get the sarf_output_folder from wsa_test_suite.sh
sarf_output_dir = sys.argv[1]
print "Removing sarf output files from : " + sarf_output_dir

#Check if sarf output directory path exists
if os.path.exists(sarf_output_dir):
    #List files in the directory
    files_list = os.walk(sarf_output_dir)
    for dir_name, path, files in files_list:
        #Process only if files found in the directory
        if files:
            #Loop through files to remove each file
            for file_name in files:
                file_path = os.path.join(dir_name, file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
