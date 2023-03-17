#!/usr/bin/python
#Author          : Manjesh.Munegowda
#Purpose         : To extract ldap UID's and format the input for use with VM's
#Scripted        : started Jan 05 2018, Jan 08 2018 - Verison 1.0
#Ref for getopts : https://gist.github.com/dideler/2395703
#Bugs	           : Email: manjesh.munegowda@nutanix.com
#

import sys, os
from os.path import basename
#print(sys.argv)

# ldapsearch -x -H 'ldaps://yourdoamin.nutanix.com:636' -b "dc=corp,dc=nutanix,dc=com" -w 'ldapPasswd' -D "CORP\ldapsearch.svc" "(SamAccountName=$1)" |egrep 'sAMAccountName|uidNumber'|awk -F':' '{print $2}'|xargs|tr '.' '-' ; """

def getopts(argv):
 try:
  opts={} 
  while argv:
    if argv[0][0] == '-':
      opts[argv[0]] = argv[1]
    argv=argv[1:]
  return opts
 except IndexError:
  usage()
  exit()

def usage():
    #print " Usage: ldap_users [-o] -i FileName "
    print "\nUsage: " + basename(__file__) + " [-o] -i <Input FileName>"
    print "        Options: -o is optional for writing to output.txt file, if used needs -i option too"
    print "                 -i for inputfile, Input FileName is required along with this option\n"
    print "                 -h this Usage...\n\n" 
    print "        Input File Format : One LDAP UserId per line, Eg. manjesh.munegowda\n\n"
 
def main():
   from sys import argv
   #import subprocess
   myargs=getopts(argv)
   if not myargs:
      usage()
   cmd1="/usr/bin/ldapsearch -x -H 'ldaps://drtitcorpdcprd1.corp.nutanix.com:636' -b " 
   cmd2="\"dc=corp,dc=nutanix,dc=com\" -w 'yourLdapPasswd' -D "
   cmd3="\"CORP\ldapsearch.svc\" \"(SamAccountName=" 
   cmd4=")\" |egrep 'sAMAccountName|uidNumber'|awk -F':' '{print $2}'|xargs|tr '.' '-'"
   oFH=""
   if '-h' in myargs:
      usage()
      exit()
   if '-o' in myargs:
   #if str(myargs['-o']) =="" :
    oFH=open("output.txt","w")
   if '-i' in myargs:
      try:
       with open(str(myargs['-i'])) as iFH:
        for fil in iFH:
         fil=fil.strip()
         #print(cmd1 + cmd2 + cmd3 + fil + cmd4)
         sysCall=str(cmd1 + cmd2 + cmd3 + fil + cmd4) #assamble the command to make the systemCall
         #print sysCall
         #sysOut=os.system(sysCall) #this method stores 0, hence below method used 
         sysOut=os.popen(sysCall).read()
         print sysOut.strip()
         if oFH: #if output option (-o) used write to the output.txt
           oFH.write(str(sysOut))
       #except IOError:
      except:
        error=sys.exc_info()[1]
        print(error)
        exit()
      if oFH:
        print("\nNOTE: Option : \"-o\" used, writing data to " + os.getcwd() + "/output.txt ...\n")
        oFH.close()
main()
