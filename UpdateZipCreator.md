**Overview:**

The Update Zip Creator (UZC) is the module that handles all of the operations relating to creating and manipulating update zips. Simply drag and drop a folder containing a _/system_ and/or _/data_ folder in its root directory, and the tool will do the rest. If the _/META-INF_ folder doesn't exist, the tool automatically generates the update-script for you. However, if _/META-INF_ already exists, the tool won't overwrite it.

**EXPERIMENTAL:** In addition to the above capabilities, the tool also offers the ability to run a custom script that you supply before flashing the _/system_ and/or _/data_ updates to your phone. Although this has been tested using a simple echo script with no ill effects, the echo script had no visible effects. Please be careful when using this feature.

**Module Status: Complete** ([Status Legend](statusLegend.md))

**What it means to be "correctly structured":**

A folder is considered correctly structured if it has a /system folder and/or /data folder in its root directory. For example, if you have a folder called update and update has two folders inside of it named system and data, then you have a correctly structured folder. The same would be true if you had either system or data (only one of the folders)

**Tutorial (Windows):**
  1. Extract the files from the download somewhere
  1. Double-click the .exe file
  1. Drag a folder that is correctly structured (see above) into the command-line Window
  1. Follow the on screen instructions
  1. Copy the completed zip to your SD card and flash in Clockwork recovery

**Tutorial (Linux): _If I get enough interest, I'll fix this module to play nicer with Linux_**
  1. Extract the files from the download somewhere
  1. cd into the extracted directory using a terminal window
  1. Download the [two Python files](http://code.google.com/p/android-customization-autotool/source/browse/#svn%2Ftrunk%2Fsrc%2Fstandalones%2FUpdateZipWizard) that make up the tool and place them in the extracted folder
  1. Make sure you have 7zip installed (p7zip-full package on Ubuntu)
    * If you can't find it, try 'aptitude search 7zip' and then install that package. Make sure typing 7za at the command line does something.
  1. type 'python UpdateZipCreator.py'
  1. Drag a folder that is correctly structured (see above) into the command-line window
  1. Follow the on screen instructions
  1. Copy the completed zip to your SD card and flash in Clockwork recovery