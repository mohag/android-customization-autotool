#!/usr/bin/env python
# @author Connor Lange
# 
# Copies all the of current Python source files to the sandbox 
# and optionally publishes them to dist 

from utils import copy # User module
from os import path

copy("*.py", path.normpath("../test/testingsandbox"))
response = raw_input("Publish? (y/n): ")
if response == 'y': 
   copy("*.py", path.normpath("../../dist/")) 