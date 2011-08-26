from distutils.core import setup
import py2exe 
from sys import argv

setup(console=['CreateUpdateZip.py'], zipfile=None, options={"py2exe":{"bundle_files": 1, "optimize": 2}})