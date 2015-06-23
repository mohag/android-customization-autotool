## About: ##
The Android Customization Autotool project aims to provide both new and existing Android customization tools in an easy to use all-in-one interface. In addition to consolidating customization knowledge and tools into one location/tool, this project also aims to provide customization options to those who previously either didn't know enough to use them or weren't confident enough (based on tutorials which are often scattered and incomplete or outdated) to take advantage of those options. For more information on this project, see the summary information below or check out our [Project Wiki](wikiIndex.md).

## Code Terms: ##
This project is open-source and you are free to modify and use it. All I ask is that you give credit where credit is due. Enjoy!

## Main Project Specs: ##

#### Development Language: ####
The Autotool is written in Python and deployed using Py2Exe for Windows users

#### Supported Operating Systems: ####
Some of the functionality is Windows only at this time, but some support Linux as well.

#### Functionality currently provided by this project: ####
  1. Create a Clockwork-flashable boot logo from a 24-bit BMP image
  1. Test boot animations without having to restart your phone (adb bootanimation wrapper)
  1. Put files on your phone without mounting the SD card (adb push wrapper)
  1. Get files from your phone without mounting the SD card (adb pull wrapper)
  1. Reboot your phone (adb reboot/reboot recovery wrapper)
  1. Set PATH system environment variables **Windows only**
  1. Compile APKs (using apktool)
  1. Decompile APKs (using apktool)
  1. Sign APKs (using signapk.jar)

#### Functionality to be provided by this project _soon_... ####
  1. Ensure that decompiled apps (especially framework-res.apk) always work
  1. Upgrade the boot animation capabilities of the program
  1. _Ideas?_

## Modules (some are stand-alone tools) ##
  1. [Boot Logo Creator v1.1](BootLogoCreator.md)
  1. [Update Zip Creator v1.0](UpdateZipCreator.md)