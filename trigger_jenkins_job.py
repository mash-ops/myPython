#! env python3
#Author          : Manjesh.Munegowda@sap.com
#Purpose         : Trigger jenkins job from command line

import sys, time

sys.path.append('/usr/local/lib/python3.9/site-packages')

import jenkins

jenkins_client = jenkins.Jenkins('http://localhost:8080',username='jenkinsbuild',password='SuperSecret')
user = jenkins_client.get_whoami()
version = jenkins_client.get_version()
print ("Jenkins Version: {}".format(version))
print ("Jenkins User: {}".format(user['id']))

job_name = 'azure-windows-market-image-build'
output = jenkins_client.build_job(job_name, {'build_vm_name':'sdow161004a115','disk_size':'128','image_name':'sdo-win2012r2-dc-oct15-azure-latest'})

next_build_number = jenkins_client.get_job_info(job_name)['nextBuildNumber']
time.sleep(10)
build_info = jenkins_client.get_build_info(job_name, next_build_number)

print("Jenkins Build URL: {}".format(build_info['url']))
print("Jenkins build number : {}".format(build_info['number']))
#print("Jenkins Build URL: {}".format(output['url']))
#print("Jenkins Build URL  : {}".format(output))
