# Public Server Automator
## V1.0.1

[PublicServerAutomator Github](https://github.com/gnubyte/publicServerAutomator)

## Purpose

This is a package intended to offer a much simpler, no hickups, no learning curve package + software alternative to Ansible/chef/puppet

## Installation

Install via pip
```
pip install publicServerAutomator
```


##  Usage



### When using a private key

```
from publicServerAutomator import Server

dockerInstructions = [
    "apt-get update -y",
    "apt-get install apt-transport-https -y",
    "apt-get install software-properties-common -y",
    "apt-get install curl -y",
    "apt-get install gnupg2 -y",
    "apt-get install git -y",
    "apt-get install acl -y",
    "apt-get install fail2ban -y"
    '''add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"''',
    "apt-get update -y",
    "apt-get install docker-ce -y",
    "docker run hello-world"
]

newDocker = Server(inputKeyPath="publickey.pem", inputKeyPassword='PASS', inputServerIP="0.0.0.0" )
newDocker.set_commands(commandList=dockerInstructions)
newDocker.connect()
newDocker.run_commands()
```

### Without using a private key


```
from publicServerAutomator import Server

dockerInstructions = [
    "apt-get update -y",
    "apt-get install apt-transport-https -y",
    "apt-get install software-properties-common -y",
    "apt-get install curl -y",
    "apt-get install gnupg2 -y",
    "apt-get install git -y",
    "apt-get install acl -y",
    "apt-get install fail2ban -y"
    '''add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"''',
    "apt-get update -y",
    "apt-get install docker-ce -y",
    "docker run hello-world"
]

newDocker = Server(inputServerIP='8.8.8.8',inputUserName='root', inputPassword='123lookatme', inputKeyPath='')
newDocker.set_commands(commandList=dockerInstructions)
newDocker.connect()
newDocker.run_commands()
```