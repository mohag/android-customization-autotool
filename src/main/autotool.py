#!/usr/bin/env python
# @author Connor Lange
# The main AutoTool script that dispatches tasks to other modules

# Standard Library
import cPickle
from os import system
from sys import argv
from sys import platform
from subprocess import Popen
from subprocess import PIPE
from subprocess import call
from subprocess import check_output
from os import stat
from os import walk
from os import path
from os import devnull
 
# Project modules 
from bootlogotools import bootLogoWizard # Boot Logo operations: only one method, just import it
import adbtools # ADB functionality
import ostools # File management, environment variables, etc.

# Function definitions
def javaAvailable(config):
   pass
      
def checkDirTree():
   pass
         
def checkConfig(config):
   if config['adbEnabled']: 
      adbtools.adbAvailable(config)
   if config['javaEnabled']:
      javaAvailable(config)   
   config['userOS'] = platform[:3] # 'win' if Windows, first 3 chars of other OS (garbage) otherwise
   checkDirTree()
   
def printHeader():
   print("\n\nAndroid Autotool V 1.0")
   print("Author: Connor Lange")
   print("Supported operating systems: [Windows]\n")
   
def menuHeader(string):
   print("\n" + ("=" * len(string)))
   print(string)
   print("=" * len(string))

def printProjectStatus():
   print('\nProgram Status: ')
   print('Current Project: '+str(config['currentProject']))
   print('ADB Enabled? '+str(config['adbEnabled']))
   print('Java Enabled? '+str(config['javaEnabled']))
   print('\n')
   
def printMenu():
   printHeader()
   printProjectStatus()
   print(("#" * 25) + " MENU OPTIONS " + ("#" * 25))
   menuHeader('PROGRAM CONFIGURATION:')
   for i in range(1,3):
      print(" "+str(i)+": "+menuOptions[i-1])
   menuHeader('File Management:')
   for i in range(3,4):
      print(" "+str(i)+": "+menuOptions[i-1])
   menuHeader('ADB Operations:')
   for i in range(4,9):
      print(" "+str(i)+": "+menuOptions[i-1])
   menuHeader('APK Operations:')
   for i in range(9,13):
      print(" "+str(i)+": "+menuOptions[i-1])
   menuHeader('Boot Logo Operations:')
   for i in range(13,14):
      print(" "+str(i)+": "+menuOptions[i-1])
   menuHeader('Boot Animation Operations:')
   print("\n" + ("#" * 64))
      
def decompile():
   print("Beginning the decompilation process...")
   print("Press ENTER to decompile the current project or drag a jar/apk to this window")
   print("to decompile that instead. This process will overwrite previously decompiled files\n")
   response = raw_input("File: ")
   if response == '':
      if config['currentProject'] == None:
         print("You haven't selected a current project to work on... Please do so from the main menu")
         raw_input("Press ENTER to continue...")
         return None
      print("Decompiling "+config['currentProject']+"...")
      system('java -Xmx128m -jar '+tools+'apktool.jar d -f '+wk+config['currentProject']+' '+wkdec+config['currentProject'])
      raw_input("\nDone! Your decompiled file is located in "+wkdec+" \nPress ENTER to continue ")      
   else: 
      system('java -Xmx128m -jar '+tools+'apktool.jar d -f '+response+' '+response+'-decompiled')
      raw_input("\nDone! Your file has been decompiled into the folder "+response+" \nPress ENTER to continue ")      
     
def compile(): 
   print("Beginning the compilation process...")
   print("Press ENTER to compile the current project or drag a folder to this window")
   print("to compile that instead. This process will overwrite previously compiled files\n")
   response = raw_input("File: ")
   if response == '':
      if config['currentProject'] == None:
         print("You haven't selected a current project to work on... Please do so from the main menu")
         raw_input("Press ENTER to continue...")
         return None
      response = raw_input("Did you modify and 9-patch images? (y/n): ")
      if response == 'y':
         compile9Patch()
      print("Compiling "+config['currentProject']+"...")
      system('java -Xmx128m -jar '+tools+'apktool.jar b -f '+wkdec+config['currentProject']+' '+wkcom+config['currentProject'])
      raw_input("\nDone! Your compiled file is located in "+wkcom+" \nPress ENTER to continue ")      
   else: 
      print("If you modified any 9-patch images, you will need to set this apk as a project to compile them")
      print("Compiling "+response+"...")
      system('java -Xmx128m -jar '+tools+'apktool.jar b -f '+response+' '+response[:-4]+'-compiled'+response[-4:])
      raw_input("\nDone! Your file has been compiled into the folder "+response+" \nPress ENTER to continue ")   
   
def compile9Patch():
   imgSrc = wkdec+str(config['currentProject'])+"\\res"
   drawables = []
   fnull = open(devnull, "w+")
   print("Beginning the 9-patch compilation process, this could take a while due")
   print("to the number of file operations and compilations that must occur.\n")
   print "Moving all 9-patch images to tools\\9patch\\res\\",
   for root, dirs, files in walk(imgSrc):
      #for subdir in dirs:
      for file in files:
         if(file.find('.9.png') != -1):
            subdir = root[root.find('drawable'):]
            drawables.append((path.join(root,file), subdir))
   for folder in drawables:
      process = Popen(['xcopy','/E','/Y',folder[0],ninePatch+folder[1]+"\\"], stdout=fnull,shell=True)
   print "   DONE!"
   print "Compiling 9-patch images...", 
   process = Popen([tools+'xUltimate-d9pc'], stdout=fnull, cwd=tools)
   process.wait()
   print "  DONE!"
   print "Moving the compiled 9-patch images back to decompiled APK folder...", 
   process = Popen(['xcopy', '/E', '/Y', tools+'done\\9patch\\res', imgSrc], stdout=fnull, shell=True)
   print "   DONE!"   
   fnull.close()
   raw_input("All 9-patch images have been compiled. Press ENTER to continue: ")
   
def sign():
   print("Beginning the signing process...")
   print("Press ENTER to sign the current project or drag a jar/apk to this window to \nsign that file instead\n")
   response = raw_input("File: ")
   if response == '':
      if config['currentProject'] == None:
         print("You haven't selected a current project to work on... Please do so from the main menu")
         raw_input("Press ENTER to continue...")
         return None
      print("Signing "+config['currentProject']+"...")
      system('java -Xmx128m -jar '+tools+'signapk.jar -w '+tools+'testkey.x509.pem '+tools+'testkey.pk8 '+wk+config['currentProject']+' '+wksign+'signed-'+config['currentProject'])
      raw_input("Done! Your signed file is located in "+wksign+"  Press ENTER to continue")      
   else: 
      system('java -Xmx128m -jar '+tools+'signapk.jar -w '+tools+'testkey.x509.pem '+tools+'testkey.pk8 '+response+' '+response[:-4]+'-signed'+response[-4:])
      raw_input("Done! Your signed file is "+response[:-4]+'-signed'+response[-4:]+"  \nPress ENTER to continue")      
   
def clr():
   system(['cls', 'clear'][platform[0:3] != 'win'])

def setCurrentProject(config):
   i = 1
   response = 50000
   print("Which number apk in the list below do you want to start working on?")
   apkList = ostools.listApks()
   print('\n'+('#' * 10)+" APK LIST "+('#' * 10))
   for apk in apkList:
      print(str(i) + ": " + apk)
      i += 1
   print('#'*30)   
   if i == 1:
      print('\nOops! You need to put at least one APK in the "workspace" folder \nbefore you can edit an APK!')  
      raw_input("Press ENTER to continue...")      
      return None
   while response > len(apkList):
      response = input("\nEnter the number of the APK you want to set as the current project: ")   
   print(response)
   config['currentProject'] = apkList[response-1]
   return None
      
### MAIN ###
try:
   config = cPickle.load(open('config.pkl', 'rb'))
except (EOFError, IOError):
   config = {'adbEnabled': True, 
             'javaEnabled': True,
             'currentProject': None, 
             'adbCmd': 'adb',
             'javaCmd': 'java',
             'checkAdbPath': True,
             'userOS': None
             }
checkConfig(config)
## Relative paths...
if config['userOS'] == 'win':
   wk = 'workspace\\'
   wksign = 'workspace\\signed\\'       
   tools = 'tools\\'
   wkdec = 'workspace\\decompiled\\'
   wkcom = 'workspace\\compiled\\'
   ninePatch = 'tools\\9patch\\res\\'
   ninePatchDone = 'tools\\done\\res\\'
else: 
   wk = r'./workspace/'
   wksign = r'./workspace/signed/'
   tools = r'./tools/'
   wkdec = r'./workspace/decompiled/'
   wkcom = r'./workspace/compiled/'
   ninePatch = r'./tools/9patch/res/'
   ninePatchDone = r'./tools/done/res/'
#Set menu options here to make life easier --> auto numbering!
menuOptions = ["Set current project", 
               'Configure system environment variables for adb and Java (Windows only)',
               'Grab all 9patch images from a folder',
               'Grab files and APKs from your phone (adb pull)',
               "Put files and APKs onto your phone (adb push)",
               "Execute shell commands (adb shell)",
               "Reboot phone (adb reboot)",
               "Test boot animation (adb shell bootanimation)",
               "Decompile Apk",
               "Compile Apk",
               "Sign Apk",
               "Compile all 9-patch images in current project",
               "Create a flashable boot logo zip from a 24-bit BMP image (Droid2 and Droid X only)"]
#Set menu functions here to make life easier --> zip ftw
menuFunctions = [setCurrentProject, ostools.setSysEnv, ostools.grabNinePatchImgs,
                 adbtools.adbPull, adbtools.adbPush, adbtools.adbShell, 
                 adbtools.adbReboot, adbtools.testBootAnim, 
                 decompile, compile, sign, compile9Patch, bootLogoWizard]

while True:
   try: 
      stat(wk+str(config['currentProject'])) # Make sure the project still exists
   except WindowsError:
      print("You seem to have moved your current project. Setting the current project to nothing")
      config['currentProject'] = None
   clr()
   printMenu()
   response = raw_input('Please make a decision or type q to quit: ')
   if response == 'q':
      cPickle.dump(config, open('config.pkl', 'wb'))
      exit()
   try:    
      operation = dict(zip(range(1,len(menuFunctions)+1),menuFunctions)).get(int(response), None)
   except ValueError:
      print("\n\nERROR: '" + response + "' is not a valid option, please check the menu again")
      raw_input("Press ENTER to continue...")
      clr()
      continue
   clr()
   print("\n\n") # Pad the vertical space a bit so they don't have to look at the top bar...
   if operation.__code__.co_argcount > 0:
      operation(config)
   else: 
      operation()