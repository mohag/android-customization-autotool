#!/usr/bin/env python
# @author Connor Lange
# A simple Python script that takes a newly created 24-bit .bmp file 
# and performs the correct hex edits  
from subprocess import call
from sys import platform
from subprocess import Popen
from subprocess import PIPE

def bootLogoHex(): 
   print("BootLogo Auto Hex-Edit V 1.0...\n\n")
   print("Drag your boot logo .bmp file into this window to proceed.")
   response = raw_input("File: ")
   if response == '' or response[-4:] != '.bmp':
      print("Invalid boot logo. The boot logo MUST be a .bmp image")
      raw_input("Press ENTER to continue: ")
      return None
   logoFile = open(response, 'rb').read() # read the entire image file

   # More error checking
   if len(logoFile) == 262136: # File size of .bmp correctly created in Photoshop
      print("Removing the first 54 bytes, and the last 2 bytes from your image...")
      logoImg = logoFile[54:-2] # Since Photoshop adds two extra bytes, remove them (remove first 54 bytes and last 2 bytes)
   elif len(logoFile) == 262134: # File size of a .bmp correctly created elsewhere 
      print("Removing the first 54 bytes from your image...")
      logoImg = logoFile[54:] # Other applications don't add two extra bytes (remove first 54 bytes)
   else:
      print("The file you supplied is not of the correct size.")
      print("Please supply a file of size 262136 bytes (Edited in Photoshop) ")
      print("or 262134 bytes (Edited elsewhere) || Your file size was: "+str(len(logoFile))+" bytes")
      raw_input("Press ENTER to continue: ")
      return None
   print("Reversing the bytes in your image...")   
   logoImg = logoImg[::-1] # Reverse the bytes
   logoBinName = response[:-4]+'.bin'
   finishedLogo = open(logoBinName, 'wb') # make a new file named the same thing as the input file, but with a .bin extension
   finishedLogo.write(logoImg) # Write out the modified image to (bootLogoFileName.bin) 
   finishedLogo.close()
   print("\nYour new boot logo has been created!!\nIt has been named "+response[:-4]+ ".bin")
   print("You will need to rename it to logo.bin and put it into the TBH LogoReplacer.zip")
   print("before flashing. Would you like to do that now?")
   decision = raw_input("y/n?: ")
   if decision == 'y':
      if platform[:3] == 'win':
         finishedLogo = open('tools\\logo.bin', 'wb')
      else:
         finishedLogo = open(r'tools/logo.bin', 'wb')
      finishedLogo.write(logoImg)
      finishedLogo.close()
      process = Popen(['tools\\7za', 'u', 'BootLogo.zip', 'logo.bin'], cwd='tools\\', stderr=PIPE)
      process.wait()
      errors = process.stderr.read()
      if errors: 
         print("The follow errors occured in 7-zip:")
         print(errors)
         print("\nNote that yout boot logo has still been created")
         print(r"in \tools\ as boot.bin")
      else:
         print(r"Your flashable boot logo replacer has been created as 'tools\BootLogo.zip'")
         print("You will need to move this zip to your SDcard. Then you'll need to reboot into")
         print("Clockwork and flash it. Would you like to copy the .zip to the root of your SDcard?")
         response = raw_input("y/n?: ")
         if response == 'y': 
            process = Popen(['adb','push','tools\\BootLogo.zip','/sdcard/'], stderr=PIPE,stdout=PIPE)
            print(process.stderr.read())
            if process.stderr.read() != '':
               print("You seem to have your phone in USB Storage mode. Put it into 'Charge Only' mode")
               raw_input("and press ENTER: ")
               print("Attempting to push again...")
               call(['adb','push','tools\\BootLogo.zip','/sdcard/'])
   raw_input("Press ENTER to continue: ")
   