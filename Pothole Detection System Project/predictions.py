import cv2
from ultralytics import YOLO

global yolo
yolo = YOLO('best.pt')


def detection(frame):
    pred = yolo.predict(frame)
    objs = list(pred[0].boxes.xyxy)
    conf = list(pred[0].boxes.conf)
    co_ords = []
    for i,j in zip(objs,conf):
        co_ords.append([(int(i[0]),int(i[1])),(int(i[2]),int(i[3])),float(j)])
    return co_ords

def cal_area(co_ordinates):
    height = co_ordinates[1][0] - co_ordinates[0][0]
    width = co_ordinates[1][1] - co_ordinates[0][1]
    area = (height/10) * (width/10)
    return int(area)

def draw_bounding_boxes(co_ords,img_new):
    for i in co_ords:
        if len(i) !=0 and i[-1] > 0.3:
            area = cal_area(i)
            text = 'pothole approx area : ' + str(area) + 'sq.cm'
            cv2.rectangle(img_new,i[0],i[1],(100,255,0),3)
            cv2.putText(img_new,text,(i[0][0],i[0][1]-5),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)
    return img_new
