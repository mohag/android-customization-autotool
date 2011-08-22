#!/usr/bin/env python
# @author Connor Lange
# 
# This module handles everything related to user preferences
# 
# Module Requirements: N/A
from sys import platform
from os import path 
import cPickle

import ostools

def checkConfig(config):
   if config['adbEnabled']: 
      ostools.adbAvailable(config)
   if config['javaEnabled']:
      ostools.javaAvailable(config)   
   ostools.checkDirTree()

def getDefaultPreferences(): 
   config = {'adbEnabled': True, 
             'javaEnabled': True,
             'currentProject': None, 
             'adbCmd': 'adb',
             'javaCmd': 'java',
             'checkAdbPath': True,
             'userOS': None
            }
   config['userOS'] = platform[:3]
   config['wk'] = path.normpath('workspace/')
   config['wksign'] = path.normpath('workspace/signed/')
   config['tools'] = path.normpath('tools/')
   config['wkdec'] = path.normpath('workspace/decompiled/')
   config['wkcom'] = path.normpath('workspace/compiled/')
   config['ninePatch'] = path.normpath('tools/9patch/res/')
   config['ninePatchDone'] = path.normpath('tools/done/res/')   
   return config

def saveUserPreferences():
   while True: 
      try:
         cPickle.dump(config, open('config.pkl', 'wb'))
         break
      except:
         print("Something went wrong while trying to save your preferences.")
         response = raw_input("Would you like to try again? (y/n): ")
         if response != 'y':
            break
         
def getUserPreferences(): 
   try:
      config = cPickle.load(open('config.pkl', 'rb'))
   except (EOFError, IOError):
      config = getDefaultPreferences() 
   checkConfig(config)
   return config