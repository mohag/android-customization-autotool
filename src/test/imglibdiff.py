# Quick diff script to verify the image library is identical to Photoshop
import Image

# Load the "normal" image flip it an save
Image.open('testimage.bmp').transpose(Image.FLIP_LEFT_RIGHT).save('testimage-flipped.bmp')

editorImg = open('testimagemanual.bmp', 'rb').read() # Image flipped in Photoshop
libImg = open('testimage-flipped.bmp', 'rb').read() # Image flipped using library

print("Photoshop v Library Tests:")
print("Flipped images equal? "+(str(editorImg == libImg)))
print("Sizes before trimming: "+str(len(editorImg))+" v "+str(len(libImg)))
editorImg = editorImg[54:-2]
libImg = libImg[54:]
print("Trimmed images equal? "+(str(editorImg == libImg)))
print("Sizes after trimming: "+str(len(editorImg))+" v "+str(len(libImg)))
