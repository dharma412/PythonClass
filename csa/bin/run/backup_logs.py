#import paramiko to create SSH client
import paramiko
import re
import datetime
global folder
import sys
fo = open("/tmp/new.txt","a+")
def execution(cmd):
	""" The function is to open a SSH client for jenkins.wga client and execute the 
	action specified in the cmd variable"""
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect('jenkins.wga', username='testuser', password='ironport')
	stdin,stdout,stderr = ssh.exec_command(cmd)
	stdin.close()
	out = stdout.readlines()
	return out

def fileoperation():
	"""The function will fetch the build nos like 2015-04-03_05-10-24
	The function will read the txt file which has the files from the location /data/jenkins/jobs/<job_name>/builds/
	It will return the build numbers specific to the job as a list""" 
	fo = open("/tmp/new.txt","r+")
	out = fo.readlines()
	fo.close()
	new_string = ''.join(out)
	directory_1 = re.findall('\s\d+\-\d+\-\d+\_\d+\-\d+\-\d+',new_string)
	directory = [x.strip() for x in directory_1]
	return directory

if __name__ == "__main__":
	try:
		#Jobs names to be given as input for taking backup
		#jobs=['WSA_SRTS_Weeklyrun_common_regression_http']
		job_name = sys.argv[1]
		#For loop is to fetch through each jobs for taking backup of the log files
		#Open a file to copy the list of builds displayed in the /data/jenkins/jobs/<job_name>/builds/ location
		fo = open("/tmp/new.txt","w+")
		cmd = ['cd /data/jenkins/jobs/']
		path = "cd %s"%(job_name)
		cmd.append(path)
		cmd.append('cd builds')
		cmd.append('ls -lrth')
		new = ';'.join(cmd)
		out = execution(new)
		for k in out:
			fo.write(k)
		fo.close()
		#To fetch the build nos using Regular expression from the /data/jenkins/jobs/<job_name>/builds/ folder
		directory = fileoperation()
		for j in directory:
			"""The for loop is to traverse through /data/jenkins/jobs/<job_name>/builds/<build_no>/robot-plugin folder 
			where the actual log files present"""
			str = "cd %s"%(j)
			cmd.append(str)
			cmd.append('cd robot-plugin')
			#For temporary action the log files will be moved to /tmp/ location
			copy_cmd = "mv wsa_qa.log.html wsa_qa.debug wsa_qa.report.html /tmp/"
			cmd.append(copy_cmd)
			#Deleting Files one by one from the specific build
			cmd.append("ls -1 * | sed 's/^/rm -f /'")
			out1 = execution(';'.join(cmd))
			cmd.pop()
			for x in out1:
				if re.findall('\w+\s\-\w+\s[\w.-]+',x):
					cmd.extend(re.findall('\w+\s\-\w+\s[\w.-]+',x))
			#After removing the unwanted files the log files are moved back from /tmp/ location
			cmd.append('mv /tmp/wsa_qa.log.html /tmp/wsa_qa.debug /tmp/wsa_qa.report.html .')
			out = execution(';'.join(cmd))
			for k in range(len(cmd)):
				"""For loop is to pop the list cmd to achieve ['/data/jenkins/jobs','<Job_name>','cd builds','ls -lrth']
				so that the function can continue for the next build of the same job"""
				if k > 3:
					cmd.pop()
		print "Completed taking backup for %s",(job_name)
	except:
		exit()
