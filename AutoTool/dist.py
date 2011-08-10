#!/usr/bin/env python
from py_compile import compile
files = ['theme.py', 'makelogobin.py']

for script in files:
   compile(script)
   