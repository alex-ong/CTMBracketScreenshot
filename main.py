import pycurl
from io import BytesIO 
import certifi
import PIL
import sys
import os
import json

OPTS = ("/export?format=pdf&portrait=false" +
       "&size=A4" + 
       "&top_margin=0.00" + 
       "&bottom_margin=0.00" +
       "&left_margin=0.00" +
       "&right_margin=0.00" +
       "&scale=4")
def downloadFile(output, spreadsheetID, sheetID=0):
    print ("Downloading sheet...")
    url = ("https://docs.google.com/spreadsheets/d/" + spreadsheetID + 
            OPTS + "&gid=" + str(sheetID))    
    
    file = open(output, 'wb')

    crl = pycurl.Curl() 
    crl.setopt(crl.CAINFO,certifi.where())
    # Set URL value
    crl.setopt(crl.URL, url)

    # Write bytes that are utf-8 encoded
    crl.setopt(crl.WRITEDATA, file)

    # Perform a file transfer 
    crl.perform() 

    # End curl session
    crl.close()



from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

#path of pdf, cropRect is percentage of rectangle.
#e.g. [0.1, 0.2, 0.5, 0.7] will crop the left 10%, right 50%, top 20% and bottom 30%
def convertPdf(path, name, cropRect):
    print ("Opening " + path)
    filename = os.path.basename(path)
    images = convert_from_path(path,dpi=400)
    #only get first page!
    image = images[0]
        
    print("Saving " + name)
    width, height = image.size
    x,y,x2,y2 = cropRect
    newRect = [x*width, y*height, x2*width, y2*height]
    newRect = [int(item) for item in newRect]
    image = image.crop(newRect)
    image.save(name)

def processConfig(configName):
    with open(configName) as f:
        data = json.load(f)
    
    for sectionName in data:
        section = data[sectionName]
        spreadsheetID = section['spreadsheet_id']
        sheetID = section['sheet_id']
        pdfName = 'output/' + sectionName+'.pdf'
        downloadFile(pdfName,spreadsheetID,sheetID)
        images = section['images']
        for image in images:
            convertPdf(pdfName, 'output/'+image, images[image])
            
if __name__ == '__main__':
    try:
        os.mkdir('output')
    except:
        pass
    processConfig('config.json')