#!/usr/bin/env python
# @author Connor Lange
# A Python script that creates an update zip and 
# optionally pushes it to the SD card
#
# This module handles all zip file creation and signing tasks
# 
# Module Prerequisites:
# 1) ADB installed and in PATH (adb push functionality only) //TODO
# 2) Java installed and in PATH (signing functionality)
 
import os
from utils import de # directory ending
from utils import progress # monitor operations
from utils import copy
from subprocess import Popen, PIPE

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

def generateUpdateScript(dir, data, sys, updateRoot):
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

def generateMeta(inFolder, data, sys):
   root = inFolder
   print("META-INF folder not detected...")
   print("Generating tree structure...")
   print("Generating directories...")
   root = inFolder+de()+"META-INF" 
   progress((lambda: os.mkdir(root)), "Creating "+root+"...") # Validate progress function, wide-use later
   root += de()+"com"
   print "Creating "+root+"...", 
   os.mkdir(root)
   print "   Done!"
   root += de()+"google"
   print "Creating "+root+"...",
   os.mkdir(root)
   print "   Done!"
   root += de()+"android"
   print "Creating "+root+"...",
   os.mkdir(root)
   print "   Done!"
   print "Generating update-script..."   
   generateUpdateScript(root, data, sys, inFolder)
   print "update-script generation complete!"
   response = raw_input("Would you like to inspect the generated script? (y/n): ")
   if response == 'y':
      genScript = open(root+de()+"update-script", 'rb')
      print("###GENERATED SCRIPT (line numbers not written to file):###\n\n")
      i = 1
      for line in genScript.readlines():
         print str(i)+": "+line,
         i += 1
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
   if inFolder[:1] == '"':
      # Strip the "'s that occur in Windows when dragging cross-partition files/folders 
      inFolder = inFolder[1:-1]
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
   if not(dataPresent) and not(systemPresent): # Missing /system and /data     
      print(r"Neither the /system or /data folders were found in the folder you specified.")
      print("When you create an update.zip, you'll need to replicate the Android directory strucure.")
      print("Ex: You should have a 'system' and/or 'data' folder in the root of your input folder.")
      exit()
   if not(metaPresent):
      generateMeta(inFolder, dataPresent, systemPresent)
   outPath = os.path.normpath(os.getcwd()+"/generatedZips/"+outName)
   print "\nCreating "+outName+" in "+os.path.dirname(outPath)+"..."
   if config is None:
      zipProcess = Popen(["7za", "a", "-tzip", "-mx0", outPath, inFolder+de()+"*"], stdout=PIPE, stderr=PIPE)   
   else: 
      zipProcess = Popen(["7za", "a", "-tzip", "-mx0", outPath, inFolder+de()+"*"], stdout=PIPE, stderr=PIPE, cwd=config['tools'])
   zipProcess.wait()
   if zipProcess.returncode:
      print("An error occurred when creating the zip. See the errors below for details:\n")
      print(zipProcess.stderr.read())
      exit()
   print "Zip successfully created!" 
   print "Signing "+outName+"..."
   os.system('java -Xmx128m -jar signapk.jar -w testkey.x509.pem testkey.pk8 '+outPath+' '+outPath)
   print "Zip successfully signed!"
   
createUpdateZip()