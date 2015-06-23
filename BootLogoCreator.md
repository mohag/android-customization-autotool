## Overview: ##

The Boot Logo Creator (BLC) is the module that handles all of the operations relating to boot logos. It will take a 24-bit BMP image (no flipping or other special edits required) and put it into the Team Black Hat (TBH) flashable boot logo zip. Optionally, it will push the created zip to your SD card


**Module Status: Complete** ([Status Legend](statusLegend.md))

## Tutorial: ##
  1. Create a 24-bit BMP image with dimensions 480 X 182 (width X height) or open the provided Template.bmp in your favorite editor. When creating your boot logo, remember that whatever color the 1px border around the image is will be the color that fills in the rest of the screen.
  1. Save your image as a 24-bit BMP image.
  1. For Windows users, and others that can run .exes, double click on BootImgToFlashZip.exe and follow the instructions on the screen.
    * For those who cannot run .exes, open up a terminal window and type 'python BootImgToFlashZip.pyc'. Note that you will need the [Python Image Library](http://www.pythonware.com/products/pil/PIL) for Python 2.7. Additionally, you'll need to install [Python 2.7](http://www.python.org/) and add it to your PATH (the Windows installer does this automatically).

## Images to Accompany Tutorial: ##
**Initial Out-of-the-Box View**

![http://android-customization-autotool.googlecode.com/svn/trunk/docs/BootLogoCreatorWalkthrough/1.png](http://android-customization-autotool.googlecode.com/svn/trunk/docs/BootLogoCreatorWalkthrough/1.png)

**Saving the logo in Photoshop (notice how it isn't flipped)**

![http://android-customization-autotool.googlecode.com/svn/trunk/docs/BootLogoCreatorWalkthrough/2.png](http://android-customization-autotool.googlecode.com/svn/trunk/docs/BootLogoCreatorWalkthrough/2.png)

**Dragging the file into the program window**

![http://android-customization-autotool.googlecode.com/svn/trunk/docs/BootLogoCreatorWalkthrough/3.png](http://android-customization-autotool.googlecode.com/svn/trunk/docs/BootLogoCreatorWalkthrough/3.png)

**The completed program output. Boot Logo Zip is now on my SD card**

![http://android-customization-autotool.googlecode.com/svn/trunk/docs/BootLogoCreatorWalkthrough/4.png](http://android-customization-autotool.googlecode.com/svn/trunk/docs/BootLogoCreatorWalkthrough/4.png)