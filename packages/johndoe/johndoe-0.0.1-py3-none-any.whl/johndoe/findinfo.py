from socket import gethostname, getfqdn
import psutil
import getpass
import platform
import subprocess

def findHostName():
	return gethostname()
	
def getDomainName():
	return getfqdn()
	
def getCpu():
	return psutil.cpu_percent()
	
def getUser():
	return getpass.getuser()
	
def getGroupPolicyInfo():
	if platform.system() == "Windows":
		proc = subprocess.Popen(["gpresult", "/r"], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		return out
	return "Not on windows - sorry"
