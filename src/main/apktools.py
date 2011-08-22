#!/usr/bin/env python
# @author Connor Lange
# A Python script that decompiles, compiles, and signs APKs using 
# apktool. The script is also a wrapper for various other APK functionality
# 
# This module handles all APK related tasks
# 
# Module Prerequisites:
# 1) Java installed and in PATH

from os import system, devnull

def decompile(config):
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
      system('java -Xmx128m -jar '+config['tools']+'apktool.jar d -f '+wk+config['currentProject']+' '+config['wkdec']+config['currentProject'])
      raw_input("\nDone! Your decompiled file is located in "+config['wkdec']+" \nPress ENTER to continue ")      
   else: 
      system('java -Xmx128m -jar '+config['tools']+'apktool.jar d -f '+response+' '+response+'-decompiled')
      raw_input("\nDone! Your file has been decompiled into the folder "+response+" \nPress ENTER to continue ")      
     
def compile(config): 
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
      system('java -Xmx128m -jar '+config['tools']+'apktool.jar b -f '+config['wkdec']+config['currentProject']+' '+wkcom+config['currentProject'])
      raw_input("\nDone! Your compiled file is located in "+wkcom+" \nPress ENTER to continue ")      
   else: 
      print("If you modified any 9-patch images, you will need to set this apk as a project to compile them")
      print("Compiling "+response+"...")
      system('java -Xmx128m -jar '+config['tools']+'apktool.jar b -f '+response+' '+response[:-4]+'-compiled'+response[-4:])
      raw_input("\nDone! Your file has been compiled into the folder "+response+" \nPress ENTER to continue ")   

def compile9Patch(config):
   imgSrc = config['wkdec']+str(config['currentProject'])+"\\res"
   drawables = []
   fnull = open(devnull, "w+")
   print("Beginning the 9-patch compilation process, this could take a while due")
   print("to the number of file operations and compilations that must occur.\n")
   print "Moving all 9-patch images to "+config['tools']+"\\9patch\\res\\",
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
   process = Popen([config['tools']+'xUltimate-d9pc'], stdout=fnull, cwd=config['tools'])
   process.wait()
   print "  DONE!"
   print "Moving the compiled 9-patch images back to decompiled APK folder...", 
   process = Popen(['xcopy', '/E', '/Y', config['tools']+'done\\9patch\\res', imgSrc], stdout=fnull, shell=True)
   print "   DONE!"   
   fnull.close()
   raw_input("All 9-patch images have been compiled. Press ENTER to continue: ")

      
def sign(config, quiet=False, file=None):
   print("Beginning the signing process...")
   print("Press ENTER to sign the current project or drag a jar/apk to this window to \nsign that file instead\n")
   response = raw_input("File: ")
   if response == '':
      if config['currentProject'] == None:
         print("You haven't selected a current project to work on... Please do so from the main menu")
         raw_input("Press ENTER to continue...")
         return None
      print("Signing "+config['currentProject']+"...")
      system('java -Xmx128m -jar '+config['tools']+'signapk.jar -w '+config['tools']+'testkey.x509.pem '+config['tools']+'testkey.pk8 '+wk+config['currentProject']+' '+wksign+'signed-'+config['currentProject'])
      raw_input("Done! Your signed file is located in "+wksign+"  Press ENTER to continue")      
   else: 
      system('java -Xmx128m -jar '+config['tools']+'signapk.jar -w '+config['tools']+'testkey.x509.pem '+config['tools']+'testkey.pk8 '+response+' '+response[:-4]+'-signed'+response[-4:])
      raw_input("Done! Your signed file is "+response[:-4]+'-signed'+response[-4:]+"  \nPress ENTER to continue")      

def startMenuLoop():
   pass
      
if __name__ == '__main__':
   startMenuLoop()
   