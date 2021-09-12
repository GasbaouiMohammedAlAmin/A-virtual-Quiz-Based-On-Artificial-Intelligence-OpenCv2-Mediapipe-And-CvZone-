# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 10:25:11 2021

@author: amine gasa
"""
import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
class Question:
    def __init__(self,data):
        self.question=data[0]
        self.choice1=data[1];
        self.choice2=data[2];
        self.choice3=data[3];
        self.choice4=data[4];
        self.answer=int(data[5])
        self.userAnswer=None
    def update(self,cursor,bboxs):
       for x ,bbox in enumerate(bboxs):
           x1,y1,x2,y2=bbox
           if(x1<cursor[0]<x2 and y1<cursor[1]<y2):
               self.userAnswer=x+1
               cv2.rectangle(img,(x1,y1), (x2,y2), (0,255,0),cv2.FILLED)
        

detector=HandDetector(detectionCon=0.8)
cap=cv2.VideoCapture(0);
cap.set(3,1280)
cap.set(4,1024)
#import csv file
path="quiz.csv";
with open(path,newline="\n")as f :
    reader=csv.reader( f)
    dataAll=list(reader)[1:]
questionList=[]    
for q in dataAll:
    questionList.append(Question(q))
print("___ "+str(len(questionList)))    
questNumber=0
totalQuest=len(dataAll)   
    
while True:
    success , img=cap.read();
    img= cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    Qesut=questionList[0];
    if(questNumber<totalQuest):
        
        Qesut=questionList[questNumber];
        img,bbox=cvzone.putTextRect(img, Qesut.question, [20,20],1,2,offset=20,border=2)
        img,bbox1=cvzone.putTextRect(img, Qesut.choice1, [150,100],1,2,offset=20,border=2)
        img,bbox2=cvzone.putTextRect(img, Qesut.choice2, [400,100],1,2,offset=20,border=2)
        img,bbox3=cvzone.putTextRect(img, Qesut.choice3, [150,300],1,2,offset=20,border=2)
        img,bbox4=cvzone.putTextRect(img, Qesut.choice4, [400,300],1,2,offset=20,border=2)
        if hands:
            lmList=hands[0]['lmList']
            cursor=lmList[8]
            length,info=detector.findDistance(lmList[8], lmList[12])
            print(length)
            if(length<60):
                Qesut.update(cursor, [bbox1,bbox2,bbox3,bbox4])
                print(Qesut.userAnswer)
                if(Qesut.userAnswer is not None):
                    time.sleep(0.4)
                    questNumber+=1
    else :
        score=0
        for mcq in questionList:
            if(mcq.userAnswer==mcq.answer):
               score+=1
        score=round((score/totalQuest)*100,2) 
        img,_=cvzone.putTextRect(img,"Quiz completed " , [150,200],1,2,offset=15)
        img,_=cvzone.putTextRect(img,"your score "+str(score)+"%" , [150,300],1,2,offset=15)
    #draw progress bar
    barValue= 120+(330//totalQuest)*questNumber               
    cv2.rectangle(img,(120,400),(barValue,450),(0,255,0),cv2.FILLED)
    cv2.rectangle(img,(120,400),(450,450),(255,0,255),2)  
    img,_=cvzone.putTextRect(img, f'{round((questNumber/totalQuest)*100)}%', [500,430],1,2,offset=15)         
    cv2.imshow("img", img)
    cv2.waitKey(1);