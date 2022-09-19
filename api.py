from crypt import methods

import requests
from flask import Flask, request, redirect, url_for
from flask import render_template
import json
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = Flask(__name__)


@app.route('/qrbarcode')
def code():
    url = request.args['url']
    url = str(url)

    # perform request ..... sample url : 'https://i.stack.imgur.com/Mspmr.png'
    response =  requests.get(url).content
    # convert to array of ints
    nparr = np.frombuffer(response, np.uint8)
    # convert to image array
    img = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED)
    
    # img = cv2.imread('/home/hadi/Projects/QRBarcodeAPI/QrBarcodeAPI/QrCodeBarCode/Images/Vitamin.png')
    
    # cap = cv2.VideoCapture(0)
    # cap.set(3,640)
    # cap.set(4,480)

    # success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        # print(myData)

        # if myData in myDataList:
        #     myOutput = 'Authorized'
        #     myColor = (0,255,0)
        # else:
        #     myOutput = 'Un-Authorized'
        #     myColor = (0, 0, 255)

        # pts = np.array([barcode.polygon],np.int32)
        # pts = pts.reshape((-1,1,2))
        # cv2.polylines(img,[pts],True,myColor,5)
        # pts2 = barcode.rect
        # cv2.putText(img,myOutput,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
        #             0.9,myColor,2)
        
    return myData
    # cv2.imshow('Result',img)
    # cv2.waitKey(1)


@app.route('/imgresize')
def resize():
    
    # extract url
    url = request.args['url']
    url = str(url)
    
    target = request.args['target']
    target = str(target)
    
    size = request.args['size']
    size = size.split('*')
    length = int(size[0])
    width = int (size[1])
    

    # extract image name
    n = url.split('/')
    n = str(n[-1])
    n2 = n.split('.')
    name = n2[1] 

    response =  requests.get(url).content
    # convert to array of ints
    nparr = np.frombuffer(response, np.uint8)
    # convert to image array
    img = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED)

    # resize func: (lenght,hight)
    imgResize = cv2.resize(img,(length,width))

    cv2.imwrite("/home/mehrehsan/public_html/"+target+"/"+name+"-resized.jpeg",imgResize)

    return "done"


@app.route('/imrotate')
def rotate():
    
    # image address url
    url = request.args['url']
    url = str(url)

    # extract image name from url
    n = url.split("/")
    na = str(n[-1])
    nam = na.split('.')
    name = str(nam[0])

    # desired store location
    target = request.args['target']
    target = str(target)

    # angle should be according to right-turn
    angle = request.args['angle'] 
    angle = int(angle)

    # load image
    response =  requests.get(url).content
    # convert to array of ints
    nparr = np.frombuffer(response, np.uint8)
    # convert to image array
    img = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED)
    
    # rotation
    width, length, rgb= img.shape

    matrix = cv2.getRotationMatrix2D((length/2,width/2),angle,1)    
    new_img = cv2.warpAffine(img,matrix,(length,width))
    
    # store new image in target directory
    cv2.imwrite("/home/ehsaniran/public_html/"+target+"/"+name+"-rot"+str(angle)+".jpg",new_img)
    
    return "done"