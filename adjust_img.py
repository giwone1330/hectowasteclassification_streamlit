import streamlit as st
from PIL import Image, ImageOps
import time
import random
import colorsys
import re
import glob

def adjust_height(image, set_aspect=0.85):
    if set_aspect == None:
        return image
    width, height = image.size
    pad = int((height/set_aspect-width)/2)
    image = image.convert('RGBA')
    new_image = ImageOps.expand(image, border=(pad,0,pad,10), fill=(0,0,0,0) )
    return new_image

for f in glob.glob("scinarios/**"):
    image = ImageOps.exif_transpose(Image.open(f))
    new_image = adjust_height(image)
    save_dir = f.replace("scinarios", "new_scinarios").split('.')[0] + ".png"
    new_image.save(save_dir,"PNG")


