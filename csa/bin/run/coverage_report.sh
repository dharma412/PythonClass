#!/usr/local/bin/bash
# $Id $
# $DateTime $
# $Author $
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This script is written and maintained by the WSA Automation Team.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

echo Code Coverage Automated Data Collection: Starting.
SUITE_FILENAME="/data/home/code_coverage/cc_test_suite_names.txt"  #"`ls -1tr /data/home/code_coverage/ | tail -n1`
TIMESTAMP=`date +%Y%m%d_%H%M%S`
echo "Get the test suite name from $SUITE_FILENAME"

if [ -e $SUITE_FILENAME ] && [ -s $SUITE_FILENAME ]
then
	
	SUITE_NAME=`tail -n1 /data/home/code_coverage/cc_test_suite_names.txt`
	echo "Generating CC report after the execution of Suite:" $SUITE_NAME  

	echo "Create directory to store the coverage files"
	Dir_Coverage_Files="/data/home/CoverageReport_files"
	if [ -d $Dir_Coverage_Files ]
	then
		#rm -rf $Dir_Coverage_Files
		echo " Coverage report files folder already exists"
	else
		 mkdir $Dir_Coverage_Files	
	fi	

	# C Code Coverage
	Dir_C_Code="/usr/build/iproot/coeus/prox/prox.coveragedir"
	C_Log_FileName=$Dir_Coverage_Files"/"$SUITE_NAME"_C_Coverage_Log.txt"
	C_Coverage_FileName=$Dir_Coverage_Files"/"$SUITE_NAME"_C_Coverage.tar"

	if [ -d $Dir_C_Code ]
	then
	  
		echo "Instrumented folder for C exists." 
		cd $Dir_C_Code  
	
		echo "Generate C gcov files."
		ls -l
		/usr/bin/gcov *.c >$C_Log_FileName
       
		#Zip the Coverage data files
		if [ -e $C_Log_FileName ] && [ -s $C_Log_FileName ]
		then
			echo "Zip the C Coverage data files ..."
			tar -cvf $C_Coverage_FileName ./*.c.gcov
			echo "Location of Coverage report files...."$Dir_Coverage_Files 
			echo "C coverage report/file name:" $C_Log_FileName $C_Coverage_FileName	
		else
			echo  "C gcov files are not generated."	
		fi 

	else
		echo $Dir_C_Code " not found, Cant generate C gcov files." 
	fi

# Python Code Coverage
	# Dir_Python_Code="/data/release/coeus-*/etc/heimdall"
	Dir_Python_Code="/data/coverage_data"
	Dir_Python_Coverage="/data/release/coeus-*/bin/coverage"
	Python_Log_FileName=$Dir_Coverage_Files"/"$SUITE_NAME"_Python_Coverage_Log.xml"
	Python_Coverage_FileName=$Dir_Coverage_Files"/"$SUITE_NAME"_Python_Coverage.tar"

	if [ -d $Dir_Python_Code ]
	then

		echo "Instrumented folder for Python exists........"
		echo "Clean the coverage directories ..."
		cd /data/ 
		rm -rf coverage_data_raw
		rm -rf coverage_data_combined
		rm -rf coverage_annotated
		rm -rf coverage_files

		echo "Back up the coverage data..."
		# cd /data
		cp -rf coverage_data coverage_data_raw
		cp -rf coverage_data coverage_data_combined
 
		echo "Combine the coverage files........"
		cd coverage_data_combined
		$Dir_Python_Coverage combine  #check this later ...
          
		echo "Copy the coverage to /data so that coverage annotate can detect ipoe files in /data/lib/python/"
		cd /data
		if [ -e ".coverage" ]
		then
			rm .coverage
		fi 
		cp /data/coverage_data_combined/.coverage /data/
          
		echo "Move the .coveragec .coveragec_source to another directory."
		cd /data/
		mkdir coverage_files
		mv .coveragerc .coveragerc_source coverage_files/.
       
		#"Generate annotated coverage files......"
		if [ ! -e .coveragec ] && [ ! -e .coveragerc_source ]
		then
			echo "Generate annotated coverage files."
			$Dir_Python_Coverage  annotate -i -d coverage_annotated
		fi
	   
#  "Generate the coverage report....."
		Dir_Python_Coverage_Annotated="/data/coverage_annotated"
		if [ -d $Dir_Python_Coverage_Annotated ]
		then
          
			echo "Generate the coverage report....."
			#cd $Dir_Python_Coverage_Annotated
			cd /data/coverage_data_combined/
			#$Dir_Python_Coverage report -m >$Python_Log_FileName
			#$Dir_Python_Coverage report >$Python_Log_FileName
			$Dir_Python_Coverage xml -i >$Python_Log_FileName
		fi
		 	
		# Zip the Python Coverage data files
		if [ -e $Python_Log_FileName ] && [ -s $Python_Log_FileName ]
		then
			echo "Zip the Python Coverage data files."
			cd /data/
			tar -cvf $Python_Coverage_FileName coverage_annotated
			echo "Location of Coverage report files: " $Dir_Coverage_Files
			echo "C coverage report/file name: " $Python_Log_FileName $Python_Coverage_FileName
		fi
          
		echo "Move the .coveragec .coveragec_source back to the data folder."
		cp /data/coverage_files/.coverage* /data/.  
	else
		echo $Dir_Python_Code " not found, Cant generate python coverage files."
	fi

else
	echo "CC report not generated as the Suite detailes are not available at" $SUITE_FILENAME
fi

#Restore Coverage Backed up files
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This part of script restores the code coverage files
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
COVERAGE_BACKUP_FOLDER=/data/home/code_coverage_backup/
echo Restore the coverage files: Starting.

if [ -d $COVERAGE_BACKUP_FOLDER ] 
then
	Dir_C_Code="/usr/build/iproot/coeus/prox/prox.coveragedir"
	if [ -d $Dir_C_Code ]
	then
		echo Restore the coverage files for C Code.
		cp -rf $COVERAGE_BACKUP_FOLDER/prox.coveragedir $Dir_C_Code/../
	fi
		
	Dir_Python_Code="/data/coverage_data"
	Dir_Python_Coverage="/data/release/coeus-*/bin/coverage"

	if [ -d $Dir_Python_Code ]
	then
		echo Restore the coverage files for Python Code.
		cp -rf $COVERAGE_BACKUP_FOLDER/coverage_data $Dir_Python_Code/../
	fi

	#if [ -d $Dir_Python_Coverage ]
	#then
	#	cp -rf $COVERAGE_BACKUP_FOLDER/coverage $Dir_Python_Coverage/../
	#fi
fi
echo Restore the coverage files: Done.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

echo Restore the coverage files: Done.
echo Code Coverage Automated Data Collection: Done.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
