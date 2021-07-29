import cherrypy
import cherrypy_cors
import cv2 as cv
import numpy as np
from PIL import Image
import io
import glob
import os
import csv
import simplejson

class HelloWorld(object):


    @cherrypy.expose
    def index(self,min,max):
        pil_image = Image.open("/home/rochans/Documents/Work/filter-tiles/mydz_files/8/0_0.jpeg")
        image = cv.cvtColor(np.array(pil_image), cv.COLOR_RGB2BGR)
        min=min.split(',')
        max=max.split(',')
        lowercolor = np.array([int(min[0]), int(min[1]), int(min[2])])
        highercolor = np.array([int(max[0]), int(max[1]), int(max[2])])
        mask = cv.inRange(image, lowercolor, highercolor)
        image[mask == 0] = (0, 0, 0)
        # encode
        is_success, buffer = cv.imencode(".jpg", image)
        io_buf = io.BytesIO(buffer)
        pil_image = Image.open(io_buf)
        pil_image.save("filtered.jpeg")

        return cherrypy.lib.static.serve_file("/home/rochans/Documents/Work/filter-tiles/filtered.jpeg", content_type='image/jpeg')

    @cherrypy.expose
    def filter(self,min,max):

        fileList = glob.glob("mydz_files/16/*.jpeg")
        ind=1
        ff=[]
        min = min.split(",")
        max = max.split(",")
        min = int(min[0])*int(min[1])*int(min[2])
        max = int(max[0])*int(max[1])*int(max[2])
        print(min,max)
        
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
            minColor=min
            maxColor=max
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
        return cherrypy.lib.static.serve_file("/home/rochans/Documents/Work/filter-tiles/images.jpeg", content_type='image/jpeg')
cherrypy.quickstart(HelloWorld())

