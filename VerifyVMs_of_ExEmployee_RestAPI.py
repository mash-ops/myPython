#!/usr/bin/python
#Author          : Manjesh.Munegowda
#Purpose         : Script to verify and power off DevVm’s of ex-employees, while parsing the 
#                  vmNames against the LDAP data to determine if the users is active.

import json, os, random, requests, sys, traceback, pprint, string, re, itertools

class TestRestApi():                
  def __init__(self):
    self.serverIpAddress = "10.4.26.27"
    self.username = "numatix"
    self.password = "YourPasswd"
    #BASE_URL = 'https://%s:9440/PrismGateway/services/rest/v1/'
    BASE_URL = 'https://%s:9440/PrismGateway/services/rest/v2.0/'
    self.base_url = BASE_URL % self.serverIpAddress
    #print "Inside TestRestApi(); base_url is set; calling get_server_session"
    self.session = get_server_session(self, self.username, self.password)

def get_server_session(self, username, password):
    session = requests.Session()
    session.auth = (username, password)
    session.verify = False                                            
    session.headers.update(
        {'Content-Type': 'application/json'})
        #{'Content-Type': 'application/json; charset=utf-8'})
    return session

def getClusterInformation(self):
    #clusterURL = self.base_url + "/cluster"
    clusterURL = self.base_url + "vms"
    #print "Getting cluster information for cluster %s" % self.serverIpAddress
    serverResponse = self.session.get(clusterURL)
    #print "Response code: %s" % serverResponse.status_code
    return serverResponse.status_code, json.loads(serverResponse.text)

if __name__ == "__main__":
  try:    
    pp = pprint.PrettyPrinter(indent=2)
    print "Entered Main()..."
    testRestApi = TestRestApi()
    print ("=" * 79)
    #print "Calling ClusterInformation from Main()..."
    #status, cluster = testRestApi.getClusterInformation()
    status, cluster = getClusterInformation(testRestApi)
    print ("=" * 79)
    print ("=" * 79)
    #LDAP
    cmd1="/usr/bin/ldapsearch -x -H 'ldaps://ldapserver.corp.nutanix.com:636' -b " 
    cmd2="\"dc=corp,dc=nutanix,dc=com\" -w 'LdapPasswd' -D "
    cmd3="\"CORP\ldapsearch.svc\" \"(SamAccountName=" 
    cmd4=")\" | grep userAccountControl |awk -F':' '{print $2}'"
 
    print "Status code: %s" % status
    print ("=" * 79)
    print ("*" * 79)
    numVm=len(cluster['entities'])
    i=0
    vm1,vm2,vm3,vmDis,vmNum= ([] for i in range(5))
    if 'entities' in cluster:
       for key,val in cluster.items():
         #print key,"=>",val 
         while (i < numVm):
          #print val[i]['name']
          vmName=val[i]['name']
          vmMem=val[i]['memory_mb']
          vmVcpu=val[i]['num_vcpus']
          vmPow=val[i]['power_state']
          vLength=len(vmName.split('-'))
          if (vLength == 1):
           vm1.append(str(vmName))
          if (vLength == 2):
           vName=str(vmName)
           #print vName
           dashToDot=vName.translate(string.maketrans('-',"."))
           chkNum=re.sub('[.]','',dashToDot)
           #print chkNum
           if (chkNum.isalpha()):
            sysCall=str(cmd1 + cmd2 + cmd3 + dashToDot + cmd4) #assamble the command to make the systemCall
            sysOut=os.popen(sysCall).read()
            if ((sysOut.strip()) == str(514)):
              #print(dashToDot, vmMem, vmVcpu, str(vmPow))
              vmDis.extend([dashToDot,vmMem,vmVcpu,vmPow])
            else:
              vm2.append(dashToDot)
           else:
            vmNum.append(dashToDot)
          if (vLength > 2):
           vm3.append(str(vmName))
          i+=1
    print("Total Vm's :" + str(i))
    #print("Vm's with single word:" + str(vm1))
    print("Vm's with LDAP disabled user:" + str(vmDis))
    #print("Vm's with LDAP disabled user:")
    [vmDis[j:j + 4] for j in xrange(0, len(vmDis), 4)]
    print ("*" * 79)
  except Exception as ex:
    print ex
    print "entered Exception scope..."
    sys.exit(1)
