#!/usr/bin/env python
# @author Connor Lange
# A Python script that creates an update zip and 
# optionally pushes it to the SD card
#
# This module handles all zip file creation and signing tasks
# 
# Module Prerequisites:
# 1) ADB install and in PATH (adb push functionality only)
import os
from utils import de # directory ending
from utils import progess # monitor operations
from utils import copy

def addScript(phoneDir, updateRoot, script):
   print("If you want to run a script before recursively copying the /"+phoneDir)
   print("folder to your phone, drag it to this window. Otherwise press ENTER")
   response = raw_input("Script: ")
   if response != '':
      copy(response, updateRoot)
      scriptName = response.split(de())[-1] 
      print "Setting up "+scriptName+" to run before copying /"+phoneDir+"...", 
      script.write("run_program PACKAGE:"+scriptName+"\n")
      print "   Done!"

def generateUpdateScript(dir, sys, data, updateRoot):
   response = raw_input("Do you want your zip to run any scripts during the flashing process? (y/n): ")
   scriptsEnabled = False if response == 'n' else True
   
   script = open(dir+de()+"update-script", 'wb')
   script.write("show_progress 0.05 0\n\n")
   if sys:
      if scriptsEnabled: 
         addScript("system", updateRoot, script)
      script.write("copy_dir PACKAGE:system SYSTEM:\n")
   if data: 
      if scriptsEnabled:
         addScript("data", updateRoot, script)
      script.write("copy_dir PACKAGE:data DATA:\n")         
   script.write("\nshow_progress 0.10 2\n\n")
   script.close()

def generateMeta(inFolder, sys, data):
   root = inFolder
   print("META-INF folder not detected... generating tree structure...")
   print("Generating directories...")
   root = inFolder+de()+"META-INF" 
   progress((lambda: os.mkdir(root)), "Creating"+root+"...")
   print "   Done!"
   root += de()+"com"
   print "Creating "+root+"...", 
   os.mkdir(root)
   print "   Done!"
   root += de()+"google"
   os.mkdir(root)
   print "   Done!"
   root += de()+"android"
   os.mkdir(root)
   print "   Done!"
   print "Generating update-script..."   
   generateUpdateScript(root, sys, data, inFolder)
   print "update-script generation complete!"
   response = raw_input("Would you like to inspect the generated script? (y/n): ")
   if response == 'y':
      genScript = open(root+de()+"update-script", 'rb')
      print("###GENERATED SCRIPT:###\n\n")
      print(genScript.read())
      print("\n\n###END GENERATED SCRIPT###\n")
   

def createUpdateZip(config=None):
   # Declarations to prevent errors (cleaner that having to catch them)
   dataPresent = False
   systemPresent = False
   metaPresent = False
   
   outName = raw_input("What do you want to call your update zip? ")
   if outName[-4:] != '.zip':
      print("Filename doesn't end in .zip... Appending .zip...")
      outName = outName+'.zip'
   print("Drag the folder you want to make "+outName+" from to this window...")
   inFolder = raw_input("Folder: ")
   if inFolder == '': 
      inFolder = os.getcwd()
   print("Checking input folder for validity...")
   for root, dirs, files in os.walk(inFolder): 
      for dir in dirs:
         if dir == 'system':
            systemPresent = True
            print("/system detected...")
         elif dir == 'data':
            print("/data detected...")
            dataPresent = True
         elif dir == 'META-INF':
            print("/META-INF detected...")
            metaPresent = True
   if !dataPresent and !systemPresent: # Missing /system and /data     
      print(r"Neither the /system or /data folders were found in the folder you specified.")
      print("When you create an update.zip, you'll need to replicate the Android directory strucure.")
      print("Ex: You should have a 'system' and/or 'data' folder in the root of your input folder.")
      exit()
   if !metaPresent:
      generateMeta(inFolder, dataPresent, systemPresent)
   print "Creating "+outName+" in "+os.getcwd()+de()+"generatedZips"+de()+"...",
   if config is None:
      zipProcess = Popen(["7za", "a", "-tzip", "-mx0", outname, inFolder])   
   else: 
      zipProcess = Popen(["7za", "a", "-tzip", "-mx0", outname, inFolder], cwd=config['tools'])
   print "   Done!"      
   # NOTICE STILL NEED TO SIGN...   
   
   
createUpdateZip()