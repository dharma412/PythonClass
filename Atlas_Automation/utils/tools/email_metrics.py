#!/usr/bin/python
import smtplib
import email.message
import sys
import os
from os.path import basename
import math
from email.mime.application import MIMEApplication
from datetime import datetime
from datetime import timedelta
from robot.api import ExecutionResult, ResultVisitor
import email.mime.application
from email.mime.multipart import MIMEMultipart
import argparse
from email.mime.text import MIMEText

# Create the parser
arg_parser = argparse.ArgumentParser(description='Emails Test Execution Report For Atlas')

# Add the arguments
arg_parser.add_argument('--sender_email',
                       type=str,
                       help='Sender email address')

arg_parser.add_argument('--recipient_email',
                       type=str,
                       help='Recipient email address')

arg_parser.add_argument('--smtp_server',
                       type=str,
                       help='SMTP server')

arg_parser.add_argument('--report_path',
                       type=str,
                       help='Path Of Report XML Of Robot')

arg_parser.add_argument('--build_version',
                       type=str,
                       help='Build version')

args = arg_parser.parse_args()

ignore_library = [
    'BuiltIn',
    'SeleniumLibrary',
    'String',
    'Collections',
    'DateTime',
    ]

# Ignores following type keywords count in email report
ignore_type = [
    'foritem',
    'for',
    ]


# Read output.xml file
build_version = args.build_version
report_path = args.report_path
output_xml=os.path.join(report_path, "output.xml")
result = ExecutionResult(output_xml)

result.configure(stat_config={'suite_stat_level': 2,
                              'tag_stat_combine': 'tagANDanother'})

total_suite = 0
passed_suite = 0
failed_suite = 0

class SuiteResults(ResultVisitor):
    
    def start_suite(self,suite):
       
        suite_test_list = suite.tests
        if not suite_test_list:
            pass
        else:        
            global total_suite
            total_suite+= 1
            if suite.status== "PASS":
                global passed_suite
                passed_suite+= 1
            else:
                global failed_suite
                failed_suite += 1

result.visit(SuiteResults())

suitepp = math.ceil(passed_suite*100.0/total_suite)

elapsedtime = datetime(1970, 1, 1) + timedelta(milliseconds=result.suite.elapsedtime)
elapsedtime = elapsedtime.strftime("%X")

myResult = result.generated_by_robot
generator = "Atlas Robot Framework"
stats = result.statistics
total= stats.total.all.total
passed= stats.total.all.passed
failed= stats.total.all.failed

testpp = round(passed*100.0/total,2)

total_keywords = 0
passed_keywords = 0
failed_keywords = 0

class KeywordResults(ResultVisitor):
    
    def start_keyword(self,kw):
        # Ignore library keywords
        keyword_library = kw.libname

        if any (library in keyword_library for library in ignore_library):
            pass
        else:
            keyword_type = kw.type            
            if any (library in keyword_type for library in ignore_type):
                pass
            else:
                global total_keywords
                total_keywords+= 1
                if kw.status== "PASS":
                    global passed_keywords
                    passed_keywords+= 1
                else:
                    global failed_keywords
                    failed_keywords += 1

result.visit(KeywordResults())

kwpp = round(passed_keywords*100.0/total_keywords,2)


email_content = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>CES Automation Robot Framework Metrics</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="viewport" content="width=device-width, initial-scale=1.0 " />
      <style>
         body {
			 background-color:#F2F2F2; 
         }
         body, html, table,span,b {
			 font-family: Calibri, Arial, sans-serif;
			 font-size: 1em; 
         }
         .pastdue { color: crimson; }
         table {
			 border: 1px solid silver;
			 padding: 6px;
			 margin-left: 30px;
			 width: 600px;
         }
         thead {
			 text-align: center;
			 font-size: 1.1em;        
			 background-color: #B0C4DE;
			 font-weight: bold;
			 color: #2D2C2C;
         }
         tbody {
			text-align: center;
         }
         th {
            word-wrap:break-word;
         }
		 td {
            height: 25px;
         }
      </style>
   </head>
   <body>
   <span>Hi Team,<br>Following are the last build execution status.<br><br><b>Metrics:<b><br><br></span>
      <table>
         <thead>
            <th style="width: 25vh;"> Stats </th>
            <th style="width: 20vh;"> Total </th>
            <th style="width: 20vh;"> Pass </th>
            <th style="width: 20vh;"> Fail </th>
			      <th style="width: 15vh;"> Perc (%%)</th>
         </thead>
         <tbody>
            <tr>
               <td style="text-align: left;font-weight: bold;"> SUITE </td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
			         <td style="text-align: center;">%s</td>
            </tr>
            <tr>
               <td style="text-align: left;font-weight: bold;"> TESTS </td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
			         <td style="text-align: center;">%s</td>
            </tr>
            <tr>
               <td style="text-align: left;font-weight: bold;"> KEYWORDS </td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
			         <td style="text-align: center;">%s</td>
            </tr>
         </tbody>
      </table>
<span><br><b>Info:<b><br><br></span>
 <table>
         <tbody>
            <tr>
               <td style="text-align: left;font-weight: normal;width: 30vh;"> Execution Time </td>
               <td style="text-align: center;font-weight: normal;">%s h</td>
            </tr>
            <tr>
               <td style="text-align: left;font-weight: normal;width: 50vh;"> Generated By </td>
               <td style="text-align: center;font-weight: normal;">%s</td>
            </tr>
         </tbody>
      </table>
<span style="text-align: left;font-weight: normal;"><br>Please refer to attached reports for detailed info.<br><br>Regards,<br>Atlas Automation Team</span>
</body></html> 
"""%(total_suite,passed_suite,failed_suite,suitepp,total,passed,failed,testpp,total_keywords,passed_keywords,failed_keywords,kwpp,elapsedtime,generator)


me = args.sender_email
recipients = args.recipient_email.split(',')

# Create message container - the correct MIME type is multipart/alternative.
for you in recipients:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Test execution summary on {} build".format(build_version)
        msg['From'] = me
        msg['To'] = you
        text = "Email after execution on {}".format(build_version)
        part = MIMEText(email_content, 'html')
        msg.attach(part)
        file=os.path.join(report_path, "log.html")
        msg.attach(MIMEText(text))
        with open(file, "rb") as fil:
       		part = MIMEApplication(
		fil.read(),
		Name=basename(file)
		)
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
        msg.attach(part)

        # Send the message via local SMTP server.
        s = smtplib.SMTP(args.smtp_server)
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(me, you, msg.as_string())
        s.quit()
        print("Email has be sent")
