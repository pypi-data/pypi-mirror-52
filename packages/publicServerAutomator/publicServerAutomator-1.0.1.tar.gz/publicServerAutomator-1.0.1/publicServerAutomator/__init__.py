import paramiko
import json
import os
import time

class Server:
    '''
    Represents a single server as an object
    TODO: move configs to a JSON config reader
    TODO: wrap in tkinter interface, load in multi configs at the same time
    '''
    
    def __init__(self, inputKeyPath=None, inputKeyPassword=None, inputServerIP='127.0.0.1', inputHostName='null', inputUserName='root', inputPassword=None):
        if (inputKeyPath != None):
            self.pathToKey = os.path.abspath(inputKeyPath)
        else:
            self.pathToKey = None
        self.LoadedKey = None
        self.keyPassword = inputKeyPassword
        self.connection = None
        self.serverIP = str(inputServerIP)
        self.hostName = str(inputHostName)
        self.userName = str(inputUserName)
        self.passWord = str(inputPassword)
        self.isConnected = False
        self.commandsRecipe = []


    def connect(self):
        '''
        Attempts to make a connection over SSH via private key file
        Will auto add SSH Client Host
        '''
        loadKeyCheck = self.__loadkey()
        if (loadKeyCheck == 0):
            # Key successfully parsed + loaded
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.connection.connect(hostname = self.serverIP, username = self.userName, pkey = self.LoadedKey)
        if (self.passWord == None and loadKeyCheck == True):
            raise Exception('There was no password set and no SSH key provided - please supply one or the other or both')
        else:
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connection.connect(hostname = self.serverIP, username = self.userName, password=self.passWord)

    def __loadkey(self):
        '''
        Private Function
        Loads SSH key before attempting to connect
        Remember... we need permissions to the key + directory...especially in Linux or secure environments
         ---
         Return Values:
         - Returns value 0/false if runtime successful
         - Returns value 1/true if runtime failed, and prints error code...long term need to tie in logging
        '''
        try:
            if (self.keyPassword != None and self.pathToKey != None):
                self.keyPassword = str(self.keyPassword)
                self.LoadedKey = paramiko.RSAKey.from_private_key_file(self.pathToKey,password=self.keyPassword)
            else:
                print('No password for private key file was provided or pathToKey was none')
                print('Omitting keypassword value as it is a password...')
                print('Path to key value:')
                print(self.pathToKey)
                self.LoadedKey = paramiko.RSAKey.from_private_key_file(self.pathToKey)
                return True
            return False
        except Exception as ErrorCode1:
            ErrorCode1 = str(ErrorCode1)
            print('Error Code 1: ERROR occured in Server.__loadkey with message: %s ' %(ErrorCode1))
            return True
            raise ValueError("Error Code 1: ERROR occurred in Server.__loadkey with message: %s " %(ErrorCode1))
        
    def __disconnect(self):
        '''
        Private Function
        Disconnects from server
        '''
        try:
            self.connection.close()
        except Exception as ErrorCode2:
            ErrorCode2 = str(ErrorCode2)
            print('Error Code 2 WARNING: while calling Server.__disconnect from server: '+ErrorCode2)
            pass # nondisconnect is OK in current simple code state
            
    def set_commands(self, commandList = None, inputJson = None):
        '''
        Loads in a list of commands, OR decodes a JSON object to use as a recipe
        inputJSON should be a text blob parsed, with the array name being Commands
        '''
        if (commandList !=None and inputJson != None):
            raise ValueError("In Server.set_commands both a commandList and json were supplied. Pick one please.")
        if (commandList != None):
            self.commandsRecipe = commandList
            return 0
        if (inputJson!= None):
            jsondata = json.loads(inputJson)
            commandList = jsondata['Commands']

    def run_commands(self):
        '''
        Runs the commands set
        '''
        if (self.connection != None):
            for command in self.commandsRecipe:
                print("Current Command: "+command)
                stdin, stdout, stderr = self.connection.exec_command(command)
                Output = stdout.read()
                Errors = stderr.read()
                if (command == 'apt-get update'):
                    print("sleeping")
                    time.sleep(60)                
                else:
                    print('sleeping')
                    time.sleep(15)
                if (Output or Errors):
                    print(Output)
                    print(Errors)
            self.__disconnect()
            return 0
        else:
            raise ValueError("Error Code 05A: in Server.run_commands, server connection was not open")
        
    def __exit__(self):
        '''
        On destruction of this Server object/termination of code, run this deconstruction instruction set
        '''
        if (self.connection != None):
            print('Closing Connection')
            self.connection.close()
            print('Connection to server %s closed' % (self.serverIP))
            


