import cv2
from ultralytics import YOLO
import pandas as pd
import cvzone
from tracker import Tracker

model = YOLO("yolov10s.pt")  

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap=cv2.VideoCapture('cctv.mp4')
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

tracker=Tracker()
cy1=364
offset=10

peoplecount=[]
count=0
while True:
    ret,frame = cap.read()
    count += 1
    if count % 5 != 0:
        continue
    if not ret:
       break
    frame = cv2.resize(frame, (1020, 600))

    results = model(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    list=[]
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        
        d = int(row[5])
        c = class_list[d]
        if 'person' in c: #creates condition to append the coord as a list format in tracker by updating
           list.append([x1,y1,x2,y2])
    bbox_idx=tracker.update(list)
    for bbox in bbox_idx:
        x3,y3,x4,y4,id=bbox #assigns new coords + uq id
        cx=int(x3+x4)//2 #need center point
        cy=int(y3+y4)//2
#        cv2.circle(frame,(cx,cy),4,(255,0,0),-1)
#        cvzone.putTextRect(frame,f'{id}',(x3,y3),1,1)
#        cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)

        if cy1<(cy+offset) and cy1>(cy-offset):
           cvzone.putTextRect(frame,f'{id}',(x3,y3),1,1)
           cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
           if peoplecount.count(id)==0: #doesn't repeat id
              peoplecount.append(id)

              
                 
                 
    cv2.line(frame,(3,364),(1018,364),(255,255,255),1)


    people=len(peoplecount)
   
    

    cvzone.putTextRect(frame,f'People:-{people}',(50,60),2,2)
    
    
    cv2.imshow("RGB", frame)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()


