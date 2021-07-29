import glob
import os
import csv
fileList = glob.glob("mydz_files/16/*.jpeg")
from PIL import Image
ind=1
ff=[]
for file in fileList:
    img = Image.open(file)  # image extension *.png,*.jpg
    orgimg = img
    new_width = 1
    new_height = 1
    file = file.split('/')
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    # getting colors
    # multiband images (RBG)
    pixelcolor = Image.Image.getcolors(img)
    #r*g*b
    colorval = pixelcolor[0][1][0] * pixelcolor[0][1][1] * pixelcolor[0][1][2]
    minColor=8702980
    maxColor=13765920
    i=False 
    if colorval < maxColor and colorval >= minColor:
        i=True
    ff.append({'sno': str(ind), 'tile': file[-1],'rgb':str(pixelcolor[0][1][0]) +','+str(pixelcolor[0][1][1]) +','+ str(pixelcolor[0][1][2]),'r*g*b':str(colorval),'filtered':str(i)})    
    ind=ind+1
with open('names.csv', 'w', newline='') as csvfile:
        fieldnames = ['sno', 'tile', 'rgb','r*g*b','filtered']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for f in ff:
            writer.writerow(f)