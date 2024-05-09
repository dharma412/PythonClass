str1="""Involved In development of Test case Scenarios, Testcases as per the requirements and
involved in functional testing of the following components -IOFA, IST.
• Performed Functional Testing of product which is hosted on Kubernetes Cluster.
• Exposure in retrieving pods logs using docker commands for Validations.
• Developed Scripts to Trigger Training and Inference jobs for Testing IOFA and IST bundle.
• Created Synthetic data Generation scripts for executing Training and Inference job.
• Involved in Automation of functional Testcases using Python and PyTest framework with Selenium.
• Involved in continuous integration of automation testcases with Jenkins and"""

str1=str1.split(' ')

d2={}

for i in str1:
    if i in d2.keys():
        d2[i]=d2[i]+1
    else:
        d2[i]=1

print(d2)
