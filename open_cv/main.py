import cv2
import numpy as np 
import face_recognition
import os
from datetime import datetime


path  = "imagesmain"
images  = []
classNames = []
mylist = os.listdir(path)
for i in mylist:
    cimg = cv2.imread(f'{path}/{i}')
    images.append(cimg)
    classNames.append(os.path.splitext(i)[0])


def encodings(images):
    eList = []
    for img in images:
        img =  cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode= face_recognition.face_encodings(img)[0]
        eList.append(encode)

    return eList

def markAttendance(name):
    with open("Attendance.csv","r+")  as f:
        mydatalist = f.readlines()
        namelist = []
        for line in mydatalist:
            entry = line.split(",")
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            tString = now.strftime('%H:%M:%S')
            dString = now.strftime('%d-%m-%Y')
            f.writelines(f'\n{name},{dString},{tString}')  

def logout(name):
    with open("Attendance.csv","r+")  as f:
        mydatalist = f.readlines()
        namelist = []
        for line in mydatalist:
            entry = line.split(",")
            namelist.append(entry[0])
        if name in namelist:
            now = datetime.now()
            logout = now.strftime('%H:%M:%S')
            f.writelines(f',{logout}')

elistknown = encodings(images)
print("Encoding Done")

cap =cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0), None,0.25,0.25)
    imgS =  cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCFrame  = face_recognition.face_locations(imgS)
    encodeCFrame = face_recognition.face_encodings(imgS, facesCFrame)

    for encodeFace,faceLoc in zip(encodeCFrame,facesCFrame):
        matches = face_recognition.compare_faces(elistknown,encodeFace)
        faceDis = face_recognition.face_distance(elistknown,encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,255,255),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,255,255),cv2.FILLED)
            cv2.putText(img, name,(x1+6,y2-6),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,0),2)
            markAttendance(name)
    
          
    logout(markAttendance)        


    cv2.imshow('Webcam',img)
    cv2.waitKey(1)







