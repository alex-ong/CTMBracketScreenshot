import pycurl
from io import BytesIO 
import certifi
import PIL
import sys
import os

SPREADSHEET_ID = "1VlI8JQOopeeV2xnqvr7Zy6QB1K6krkJ90L_RbXtzVJo"
SHEET_ID = "0"

OPTS = ("/export?format=pdf&portrait=false" +
       "&size=A4" + 
       "&top_margin=0.00" + 
       "&bottom_margin=0.00" +
       "&left_margin=0.00" +
       "&right_margin=0.00" +
       "&scale=4")
test = "https://docs.google.com/spreadsheets/d/1VlI8JQOopeeV2xnqvr7Zy6QB1K6krkJ90L_RbXtzVJo/export?format=pdf&portrait=false&size=A4&top_margin=0.00&bottom_margin=0.00&left_margin=0.00&right_margin=0.00&scale=4&gid=0"       
def downloadfile(output, spreadsheetID, sheetID=0):
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

        
if __name__ == '__main__':
    name = 'ctmcc.pdf'
    #downloadfile(name, SPREADSHEET_ID,SHEET_ID)
    convertPdf(name, 'CTMCC winners.png', [0.05,0.0,0.9,0.685])
    convertPdf(name, 'CTMCC losers.png', [0.05,0.685,0.75,1.0])