#!/usr/bin/env python
# @author Connor Lange
# A collection of various os tools such as environment variable 
# tools, file management, etc.
# 
# This module handles all operating system related tasks. Despite this, other modules
# are allowed to spawn subprocesses even though the action is technically an OS task
#
# NOTE: This module should NEVER import other custom modules 
#
# Module Prerequisites: 
# 1) Windows is the assumed OS at this time
from sys import platform

from os import system

from subprocess import Popen
from subprocess import call
from subprocess import check_output
from subprocess import PIPE

def javaAvailable(config):
   returnCode = call(['java', '-version'], stderr=PIPE, stdout=PIPE)
   if returnCode != 0:
      print("ERROR: Java is not listed in your PATH environment variable. As a result, operations that use Java (i.e signing, etc.) will not work!")
      response = raw_input("Would you like to put Java into your PATH environment variable? (y/n): ")
      if response == 'y': 
         setSysEnv(config, prompt=False, adb=False, java=True)
      else:
         reponse = raw_input("Would you like to commit the decision to skip environment variable checks to this program's configuration? (y/n) ")
         config['checkJavaPath'] = False
      
def checkDirTree():
   pass
   
def adbAvailable(config):
   process = Popen([config['adbCmd'], 'version'], stdout=PIPE, stderr=PIPE) # Check for adb
   if process.stderr.read() != '':
      if config['adbCmd'] == 'adb':
         print("ERROR: adb is not listed in your PATH enviroment variable. As a result, operations that access your phone will not work!")
         response = raw_input("If you know where the adb executable is located, drag it into this window. Otherwise press enter: ")
         if response == '':
            response = raw_input("adb couln't be located. Would you like to proceed anyway? (y/n) ")
            if response != 'y':
               print("You have chosen not to proceed since adb cannot be used...\nGoodbye!")
               exit()
            response = raw_input("Would you like to commit the decision to skip start-up adb checks to this program's configuration? (y/n) ")
            if response == 'y':
               config['adbEnabled'] = False
         else:
            config['adbCmd'] = response
            # Check again with updated config TODO possibly fix since stack overflow can happen (given enough tries)
            adbAvailable(config)       
   else:
      if config['adbCmd'] != 'adb' and config['checkAdbPath']:
         print("Lack of PATH configuration detected...")
         print("Although adb commands will work within this program, you won't be able to")
         print("simply type 'adb' on the command line. This can be resolved, by setting")
         print("your PATH system environment variable.")
         response = raw_input("Would you like to configure PATH to include adb? (y/n) ")
         if response == 'y':
            setSysEnv(config, prompt=False, adb=True, java=False)
         else:
            reponse = raw_input("Would you like to commit the decision to skip environment variable checks to this program's configuration? (y/n) ")
            config['checkAdbPath'] = False


def getNinePatchImgs(path=""):
   process = Popen(['dir',path], stdout=PIPE, shell=True)
   out = [x.split()[-1] for x in process.stdout.readlines() if len(x) >= 8 and x[-7:-1] == '.9.png']
   return out

def grabNinePatchImgs(config):
   path = raw_input('Enter the path to the directory to copy the nine-patch images from: ')
   location = raw_input('Enter the path to the directory to copy the nine-patch images to: ')

   ninePatchImgs = getNinePatchImgs(path)  
   
   for image in ninePatchImgs:
      print('Copying '+image+' to '+location)
      if call(['copy', image, location]):
         print("COPYING OF "+image+" TO "+location+" FAILED!") 

   raw_input("Done! Press ENTER to continue")
   
def listApks(config):   
   process = Popen(['dir', config['wk']+'*.apk'], stdout=PIPE, shell=True)
   apks = [x.split()[-1] for x in process.stdout.readlines() if len(x) >= 5 and x[-5:-1] == '.apk']
   return apks
      
def setSysEnv(config, prompt=True, adb=True, java=True):
   if platform[:3] == 'win':
      if prompt:
         response = raw_input("Would you like to add adb to your path? (y/n): ")
         if response == 'y':
            print("Drag the FOLDER containing adb.exe to this window: ")
            response = raw_input('Folder: ')
            currentPath = check_output(['echo', '%PATH%'], shell=True).rstrip()
            if currentPath[-1:] == ';':
               currentPath = currentPath[:-1]
            print("Setting variable globally...")
            system('setx PATH "'+currentPath+';'+response+'" /M')
            print("\nSetting variable locally...")
            system('setx PATH "'+currentPath+';'+response+'"')
            print("\nAdded "+response+" to the PATH environment variable")
         response = raw_input("Would you like to add java to your path? (y/n): ")
         if response == 'y':
            print("Drag the FOLDER containing java.exe to this window: ")
            response = raw_input('Folder: ')
            currentPath = check_output(['echo', '%PATH%'], shell=True).rstrip()
            if currentPath[-1:] == ';':
               currentPath = currentPath[:-1]
            print("Setting variable globally...")
            system('setx PATH "'+currentPath+';'+response+'" /M')
            print("\nSetting variable locally...")
            system('setx PATH "'+currentPath+';'+response+'"')
            print("\nAdded "+response+" to the PATH environment variable")
         raw_input("Done! Press ENTER to continue: ")
      else:
         if adb:
            system('setx PATH %PATH%;'+config['adbCmd'][:-7])
         if java: 
            system('setx PATH %PATH%;'+config['javaCmd'][:-8])
   else:
      print("Setting Linux environment variables currently isn't supported")

