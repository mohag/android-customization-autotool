#!/usr/bin/env python
# @author Connor Lange
# A collection of various os tools such as environment variable 
# tools, file management, etc.
# 
# This module handles all operating system related tasks. Despite this, other modules
# are allowed to spawn subprocesses even though the action is technically an OS task
#
# Module Prerequisites: 
# 1) Windows is the assumed OS at this time
from sys import platform

from os import system

from subprocess import Popen
from subprocess import call
from subprocess import check_output
from subprocess import PIPE

import autotool # Access to global settings

def getNinePatchImgs(path=""):
   process = Popen(['dir',path], stdout=PIPE, shell=True)
   out = [x.split()[-1] for x in process.stdout.readlines() if len(x) >= 8 and x[-7:-1] == '.9.png']
   return out

def grabNinePatchImgs(prompt=True, path=''):
   if prompt:
      path = raw_input('Enter the path to the directory to copy the nine-patch images from: ')
      location = raw_input('Enter the path to the directory to copy the nine-patch images to: ')
   else:
      location = ninePatch
      Popen(['del', '9patch'], shell=True)
      Popen(['mkdir', '9patch'], shell=True)
   
   ninePatchImgs = getNinePatchImgs(path)  
   
   for image in ninePatchImgs:
      print('Copying '+image+' to '+location)
      if call(['copy', image, location]):
         print("COPYING OF "+image+" TO "+location+" FAILED!") 

   raw_input("Done! Press ENTER to continue")
   
def listApks():   
   process = Popen(['dir', autotool.wk+'*.apk'], stdout=PIPE, shell=True)
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

