from PIL import Image
import PIL
import os
import glob

image_path = "./products"
##icon_path = "./icons"
image_files = glob.glob(image_path + '/*')
##icon_files = glob.glob(icon_path + '/*')

for fl in image_files:
    im = Image.open(fl)
    im.save(fl, optimize=True, quality=30)
##for fl in icon_files:
##    im = Image.open(fl)
##    im.save(fl, optimize=True, quality=30)
