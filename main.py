import zipfile
import PIL
from PIL import Image
from PIL import ImageDraw
import pytesseract
import cv2 as cv
import numpy as np
from zipfile import ZipFile


#print('starting program')
# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
infoDict = {}
with ZipFile('readonly/images.zip') as myZip:
        myZip.extractall()
        for newspaper in myZip.infolist():
            #print('Starting first for loop')
            #display(newspaper)
            #display(newspaper[0])
            #newspaper = myZip.infolist()
            #display(newspaper.filename)
            currentNewspaper = newspaper.filename
            #display(newspaper)
            with myZip.open(newspaper.filename) as myFile:
                picture = Image.open(myFile)  
                #print('newspaper name')
                display(newspaper.filename)
                #print('Image to string conversion')
                article = pytesseract.image_to_string(picture)
                #print('Completed')
                #currentNewspaper = newspaper.namelist()
                #print('printing current newspaper')
                #print(currentNewspaper)
                img = cv.imread(currentNewspaper)
                #display(img)
                #display(img)
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                #display(image)
                #print('detecting faces')
                faces = face_cascade.detectMultiScale(img, 1.35)
                #print('completed')
                #display(faces)
                #display(faces)
                image = Image.fromarray(gray, "L")
                drawing=ImageDraw.Draw(image)
                boundingBoxes = []
                for x,y,w,h in faces:
                    #outline= drawing.rectangle((x,y,x+w,y+h), outline='white')
                    innerList = [x,y,w,h]
                    boundingBoxes.append(innerList)
                #print('Printing list bounding boxes')
                #print(boundingBoxes)
                #display(image)
                #rec=faces.tolist()[3]
                #drawing.rectangle(rec, outline='red')
                #display(image)
                faceImages = []
                for box in boundingBoxes:
                    #print('Starting for loop boundingBoxes')
                    #display(image.crop((2510, 211, 2659, 360)))
                    #print('Printing first param of box')
                    #print(box[0])
                    croppedImage = image.crop((box[0], box[1], box[0]+box[2], box[1]+box[3]))
                    faceImages.append(croppedImage)
                    #display(croppedImage)
                    #print('end of for loop')
                infoDict[currentNewspaper] = {'faceImages' : faceImages, 'text': article, 'boundingBoxes':boundingBoxes}
                print('end of loop')
                #print('Printing infoDict')
                #display(infoDict)
def getFaces():
    print('starting fucntion')
    userInput = input('Enter search ')
    print(userInput)
    #print(userInput)
    #for dictionary in infoDict:
    #contact_sheet = 0
    #lengthFM = len(faceImages)
    #print(lengthFM)
    for newspaper in myZip.infolist():
        #print('in for loop')
        cn = newspaper.filename
        #print("filename "+cn)
        first_image = None
        contact_sheet = None 
        faceImages = infoDict[cn]['faceImages']
        #print(len(faceImages))
        if len(faceImages) > 0:
            first_image=infoDict[cn]['faceImages'][0]
            contact_sheet=PIL.Image.new(first_image.mode, (1653,348))
        x=0
        y=0
        print(first_image)
        if userInput in infoDict[cn]['text']:
            #print('You are in the if statement')
            #faceImages = infoDict[cn]['faceImages']
            for face in faceImages:
                contact_sheet.paste(face, (x, y) )
                if x+face.width >= contact_sheet.width:
                    x=0
                    y=y+face.height
                else:
                    x=x+face.width
            #print('Printing contact sheet ver 1')
            #display(contact_sheet)
            #print('Printing width')
            #display(contact_sheet.width)
            #print('printing height')
            #display(contact_sheet.height)
            print('Results found in file ' + cn)
            if len(faceImages)==0:
                print('But there were no faces in that file!')
            else:
                #'About to resize contact sheet'
                contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
                display(contact_sheet)


getFaces()
