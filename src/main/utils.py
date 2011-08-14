#!/usr/bin/env python
# @author Connor Lange
# Generic utility functions for the Autotool
#
# This module handles common tasks for all other modules
from sys import platform
from subprocess import Popen, PIPE

# Returns the directory ending character (i.e '/' or  '\')
def de(): 
   try:
      return de.ending
   except AttributeError: 
      if platform[:3] == 'win':
         de.ending = '\\'
      else: 
         de.ending = '/'
      return de.ending

def progress(func, msg):
   print msg, 
   func()
   print "   Done!"   
   
# Copy utility
def copy(src, dest, dir=False):
   if platform[:3] == 'win':
      process = Popen(['xcopy','/Q','/E','/Y', src, dest], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
      if dir: 
         output = process.communicate("D") # Tell xcopy its a directory if it asks
      else: 
         output = process.communicate("F") # Tell xcopy its a file if it asks
      return process.returncode
   else: # Linux
      if dir:
         process = Popen(['cp','-r','-f',src, dest], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
         process.wait()
      else:
         process = Popen(['cp','-f',src, dest], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
         process.wait()
      return process.returncode 
      
         