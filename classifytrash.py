from lib2to3.pgen2.tokenize import generate_tokens
from pyexpat import features
from string import capwords
import cv2
import os
import sys, getopt
import signal
import time
import numpy as np
from edge_impulse_linux.image import ImageImpulseRunner
from datetime import datetime
import notecard
from notecard import hub, note, card
from periphery import I2C
import keys

debug = False #set to true to save images of trash

port = I2C("/dev/i2c-1")

card = notecard.OpenI2C(port, 0, 0)

#hub.set(card,product=keys.productUID,mode="continous",outbound=30,inbound=720)
req = {"req": "hub.set"}
req["product"] = keys.productUID
req["mode"]="periodic"
req["outbound"] = 30
req["inbound"] = 720
rsp = card.Transaction(req)

req = {"req": "hub.sync"}
rsp = card.Transaction(req)

#Set gps to continous mode
req = {"req": "card.location.mode"}
req["mode"] = "continuous"
card.Transaction(req)

runner = None

def now():
    return round(time.time() * 1000)

def get_webcams():
    port_ids = []
    for port in range(5):
        print("Looking for a camera in port %s:" %port)
        camera = cv2.VideoCapture(port)
        if camera.isOpened():
            ret = camera.read()[0]
            if ret:
                backendName =camera.getBackendName()
                w = camera.get(3)
                h = camera.get(4)
                print("Camera %s (%s x %s) found in port %s " %(backendName,h,w, port))
                port_ids.append(port)
            camera.release()
    return port_ids

def sigint_handler(sig, frame):
    print('Interrupted')
    if (runner):
        runner.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


def generate_features(img):
    features = []
    pixels = np.array(img).flatten().tolist()

    for ix in range(0, len(pixels), 3):
        b = pixels[ix + 0]
        g = pixels[ix + 1]
        r = pixels[ix + 2]
        features.append((r << 16) + (g << 8) + b)

    return features

def gpsActive():
    req = {"req": "card.location"}
    rsp = card.Transaction(req)
    print(rsp)
    if "{gps-active}" in rsp["status"] and "lat" in rsp and "lon" in rsp:
        return True
    else:
        return False
    
def main():
    
    model = "model.eim"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    print('MODEL: ' + modelfile)

    with ImageImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')
            labels = model_info['model_parameters']['labels']
            #if len(args)>= 2:
                #videoCaptureDeviceId = int(args[1])
            #else:
            port_ids = get_webcams()
            if len(port_ids) == 0:
                raise Exception('Cannot find any webcams')
            if len(port_ids)> 1:
                raise Exception("Multiple cameras found. Add the camera port ID as a second argument to use to this script")
            videoCaptureDeviceId = int(port_ids[0])

            camera = cv2.VideoCapture(videoCaptureDeviceId)
            ret = camera.read()[0]
            if ret:
                backendName = camera.getBackendName()
                w = camera.get(3)
                h = camera.get(4)
                print("Camera %s (%s x %s) in port %s selected." %(backendName,h,w, videoCaptureDeviceId))
                camera.release()
            else:
                raise Exception("Couldn't initialize selected camera.")

            next_frame = 0 
            
            for img in runner.get_frames(videoCaptureDeviceId):
                if (next_frame > now()):
                    time.sleep((next_frame - now()) / 1000)
                
                features = generate_features(cv2.resize(img, (160,160), interpolation=cv2.INTER_AREA))  

                res = runner.classify(features)
                
                if "classification" in res["result"].keys():
                        score = res['result']['classification']['trash']
                        if score > 0.6:
                            print("trash: " + str(score))
                            #get gps location
                            req = {"req": "card.location"}
                            rsp = card.Transaction(req)
                            
                            #send the trash classification using the Notecard API
                            note.add(card,
                                    file="trash.qo",
                                    body={"trash": score, "lat": rsp["lat"], "lon": rsp["lon"]}) 
                            
                            if debug:
                                outfile = '%s/%s.jpg' % ("debug", "trash"  + str(datetime.now())) #save the image of trash
                                cv2.imwrite(outfile,  cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
                next_frame = now()

        finally:
            if (runner):
                runner.stop()


while not gpsActive(): #wait for gps to be active before starting the script
    print("waiting for gps")
    time.sleep(30)
    
print("starting")   
main()