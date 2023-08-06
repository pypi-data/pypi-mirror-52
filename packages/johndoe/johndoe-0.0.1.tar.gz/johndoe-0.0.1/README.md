# johndoe

The intention of this application is to test whether your environment will download any package from PyPi.
PyPi allows anybody (even John Doe) to upload packages to the internet, but a companies infrastructure
should have suitable measures in place so that only trusted packages are downloaded.

The package tries to find some interesting data on your machine and prints them to the console.
If this was a genuinely malicious program, it could be sending the information to an unsavoury destination.

Hopefully the app highlights some flaws in processes, or at least confirms their usefulness.

## Usage
```
from johndoe import findinfo
from pprint import pprint

hostname = findinfo.findHostName()
domainname = findinfo.getDomainName()
cpu_percent = findinfo.getCpu()
user = findinfo.getUser()
gpinfo = findinfo.getGroupPolicyInfo()

print("hostname is {}".format(hostname))
print("domain name is {}".format(domainname))
print("cpu percentaage is {}".format(cpu_percent))
print("user is {}".format(user))
pprint("group policy info is {}".format(gpinfo))
```