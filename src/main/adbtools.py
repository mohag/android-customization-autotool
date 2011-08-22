#!/usr/bin/env python
# @author Connor Lange
# A collection of various adb tools such as push, pull, shell, etc.
# 
# This module handles all ADB related tasks
#
# Module Prerequisites: 
# 1) Android SDK/ADB

from subprocess import Popen
from subprocess import call
from subprocess import PIPE

from os import system

# An adb pull wrapper
# @param config the current configuration of the AutoTool
def adbPull(config):
   if config['adbEnabled']:
      print("What file(s) would you like to grab?\n[Ex: /system/app/Dialer.apk gets the Dialer app, whereas /system/app/ gets all system apps!]")
      source = raw_input("Source: ")
      print("Where would you like to put the files retrieved from your phone? \n[Ex: C:\Users\user\Desktop] Press ENTER to place the files in the same folder as this script!")
      destination = raw_input("Destination: ")
      print("\nExecuting adb pull operation...\n")
      if destination == '':
         while call('adb pull '+source):
            print("An error occurred. Please ensure you have USB debugging")
            print("enabled and your phone is connected to your computer")
            if raw_input("Would you like to try again? (y/n): ") != 'y':
               break
      else:         
         while call('adb pull '+source+' '+destination):
            print("An error occurred. Please ensure you have USB debugging")
            print("enabled and your phone is connected to your computer")
            if raw_input("Would you like to try again? (y/n): ") != 'y':
               break
   else: 
      print('You opted out of adb operations. Action cannot proceed!')
      response = raw_input("Would you like to re-enable adb operations in this program? (y/n) ")
      if response == 'y':
         adbAvailable(config)
   raw_input("\nDone! Press ENTER to continue...")

   
def adbPush(config):
   if config['adbEnabled']:
      print("What file/directory would you like to send?\nType it in, or drag it to this window")
      source = raw_input("Source: ")
      print("Where would you like to send the file(s)?\n [Ex: /system/app/ will send the file(s) to where system APKs are stored]")
      destination = raw_input("Destination: ")
      print("\nExecuting adb push operation...\n")
      system('adb push '+source+' '+destination)
   else: 
      print('You opted out of adb operations. Action cannot proceed!')
      response = raw_input("Would you like to re-enable adb operations in this program? (y/n) ")
      if response == 'y':
         adbAvailable(config)
   raw_input("\nDone! Press ENTER to continue...")

def adbShell(config):
   if config['adbEnabled']:
      response = raw_input("Do you want to run more than one shell command? (y/n) ")
      if response == 'y':
         print("Remember 'exit' quits the shell")
         print("Starting shell...\n")
         supress = call('adb shell')             
      else: 
         response = raw_input("adb shell ")
         system('adb shell '+response)
   else: 
      print('You opted out of adb operations. Action cannot proceed!')
      response = raw_input("Would you like to re-enable adb operations in this program? (y/n) ")
      if response == 'y':
         adbAvailable(config)
   raw_input("\nDone! Press ENTER to continue...")
   
def adbReboot(config):
   if config['adbEnabled']:
      response = raw_input("Do you want to reboot normally or reboot into recovery (not Clockwork)? (n/r): ")
      mode = '' # stays empty for normal reboot, but changes for recovery
      if response != 'r':      
         print("Rebooting your phone...\n")
      else: 
         print("Rebooting your phone into stock recovery...\n")
         mode = 'recovery'
      while call(['adb', 'reboot', mode]):
         print("\nAn error occurred. Please ensure you have USB debugging")
         print("enabled and your phone is connected to your computer")
         if raw_input("Would you like to try again? (y/n): ") != 'y':
            break 
         print("\n") # pad between response and adb output
      print("Success! Phone is going down for reboot now!")
   else: 
      print('You opted out of adb operations. Action cannot proceed!')
      response = raw_input("Would you like to re-enable adb operations in this program? (y/n) ")
      if response == 'y':
         adbAvailable(config)
   raw_input("\nDone! Press ENTER to continue...")

def testBootAnim(config):
   print("Beginning test of bootanimation, press CTRL+C (SIGINT) to exit...")
   if config['adbEnabled']:
      try: 
         supressRes = call('adb shell bootanimation')
      except KeyboardInterrupt:
         raw_input("Test complete, press ENTER to continue: ")   
   else: 
      print('You opted out of adb operations. Action cannot proceed!')
      response = raw_input("Would you like to re-enable adb operations in this program? (y/n) ")
      if response == 'y':
         adbAvailable(config)