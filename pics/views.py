from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import traceback
import numpy as np
# import imutils
# from imutils import contours
# from imutils.perspective import four_point_transform
import matplotlib.pyplot as plt
import pandas as pd
#from PIL import Image
import pytesseract
import base64
from base64 import decodestring
from django.core.files.storage import default_storage


# Create your views here.
@csrf_exempt
def home(request):
    return HttpResponse("Go to extract_date")

@csrf_exempt
def extract_date(request):
    if request.method == 'POST':
        base64_string =request.POST.get("base_64_image_content")
        print(type(base64_string))
        file_name="image.jpeg"
        fh = open(file_name, "wb")
        fh.write(base64.b64decode(base64_string))
        file_url = default_storage.url(file_name)
        img=plt.imread(file_url)
        print(img)
        
        #tesseract from program files
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        print("44444")
        
        # fetching text from the image and storing it into a text file
        file_text = pytesseract.image_to_string(img)
        #print(file_text)
        #import datefinder
        import dateutil.parser as dparser
        l = []
        for i in file_text.splitlines():
            try:
                #matches = list(datefinder.find_dates(i))
                matches=dparser.parse(i,fuzzy=True)
                matches=matches.strftime('%Y-%m-%d')
                l.append(matches)
            except Exception as e:
                pass
        l2=[]
        for l1 in l:
            if '20' in l1:
                l2.append(l1)
        
        if len(l2)>0:
            d=l2[0]
            date=("date:",d)
        else:
            date=("date:null")
        print(date)
        fh.close()
        default_storage.delete(file_name)
        return HttpResponse(date)

