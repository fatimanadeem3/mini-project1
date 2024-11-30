from collections import deque  #from this there will be stack in which we can add element from both side and also remove it from both side 
import cv2
import numpy as np

def values(x):
    pass

cv2.namedWindow("color detectors")#the following is perdefine perameter for a plot to detect colour
cv2.createTrackbar("upper hue","color detectors",153,180,values)
cv2.createTrackbar("upper saturation","color detectors",255,255,values)
cv2.createTrackbar("upper value","color detectors",255,255,values)
cv2.createTrackbar("lower hue","color detectors",64,180,values)
cv2.createTrackbar("lower saturation","color detectors",72,255,values)
cv2.createTrackbar("lower value","color detectors",49,255,values)
 
#as we use deque to store elements,now making array to handle colour
blue_points=[deque(maxlen=1024)]
green_points=[deque(maxlen=1024)]
red_points=[deque(maxlen=1024)]
yellow_points=[deque(maxlen=1024)]

#index points for colour
blue_index=0
green_index=0
red_index=0
yellow_index=0

#to use kernel ,small matrix for blurring, sharpening, embossing, edge detection.
kernel=np.ones((5,5),np.uint8)

colors=[(255,0,0),(0, 255, 0), (0, 0, 255), (0, 255, 255)]

color_index=0

#to start canvas

paintWindow=np.zeros((471,636,3)) +255
paintWindow=cv2.rectangle(paintWindow,(40,1),(140,65),(0,0,0),2)
paintWindow=cv2.rectangle(paintWindow,(160,1),(255,65),colors[0],-1)
paintWindow=cv2.rectangle(paintWindow,(275,1),(370,65),colors[1],-1)
paintWindow=cv2.rectangle(paintWindow,(390,1),(485,65),colors[2],-1)
paintWindow=cv2.rectangle(paintWindow,(505,1),(600,65),colors[3],-1)

cv2.putText(paintWindow,"erase all",(49,33),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
cv2.putText(paintWindow,"blue",(185,33),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
cv2.putText(paintWindow,"green",(298,33),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
cv2.putText(paintWindow,"red",(420,33),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
cv2.putText(paintWindow,"yellow",(520,33),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
cv2.namedWindow("paint",cv2.WINDOW_AUTOSIZE)

#connect to camera 

cap=cv2.VideoCapture(0)

#making the loop for camaer to work untill user finished his/her work
while True:
    ret , frame= cap.read()
    frame=cv2.flip(frame,1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    u_hue=cv2.getTrackbarPos("upper hue","color detectors")
    u_saturation=cv2.getTrackbarPos("upper saturation","color detectors")
    u_value = cv2.getTrackbarPos("upper value", "color detectors")
    l_hue = cv2.getTrackbarPos("lower hue", "color detectors")
    l_saturation = cv2.getTrackbarPos("lower saturation", "color detectors")
    l_value = cv2.getTrackbarPos("lower value", "color detectors")

    
    upper_hsv=np.array([u_hue,u_saturation,u_value])
    lower_hsv=np.array([l_hue,l_saturation,l_value])


    #to add button on screen 

    frame=cv2.rectangle(frame,(40,1),(140,65),(122,122,122),-1)
    frame=cv2.rectangle(frame,(160,1),(255,65),colors[0],-1)
    frame=cv2.rectangle(frame,(275,1),(370,65),colors[1],-1)
    frame=cv2.rectangle(frame,(390,1),(485,65),colors[2],-1)
    frame=cv2.rectangle(frame,(505,1),(600,65),colors[3],-1)

    cv2.putText(frame,"erase all",(49,33),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(frame,"blue",(185,33),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(frame,"green",(298,33),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(frame,"red",(420,33),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(frame,"yellow",(520,33),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),2,cv2.LINE_AA)

    #making a mask mean black mask layer to identifying the pointer
    Mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    cnts,_=cv2.findContours(Mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center=None

    if len(cnts)>0:
        cnt=sorted(cnts,key=cv2.contourArea,reverse=True)[0]
        ((x,y),radius)=cv2.minEnclosingCircle(cnt)
        cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
        M=cv2.moments(cnt)
        center=(int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))

        #to detect the button option
        if center[1]<=65:
            if 40<=center[0] <=140:#to clear 
                blue_points=[deque(maxlen=512)]
                green_points=[deque(maxlen=512)]
                red_points=[deque(maxlen=512)]
                yellow_points=[deque(maxlen=512)]
                blue_index=0
                green_index=0
                red_index=0
                yellow_index=0
                paintWindow[67:,:,:]=255
            elif 160 <= center[0] <=255:
                color_index=0
            elif 275 <= center[0] <=370:
                color_index=1
            elif 390 <= center[0] <=485:
                color_index=2
            elif 505 <= center[0] <=600:
                color_index=3

        else:
            if color_index ==0:
                blue_points[blue_index].appendleft(center)
            elif color_index==1:
                green_points[green_index].appendleft(center)
            elif color_index==2:
                red_points[red_index].appendleft(center)
            elif color_index==3:
                yellow_points[yellow_index].appendleft(center)
    else:
        blue_points.append(deque(maxlen=512))
        blue_index +=1
        green_points.append(deque(maxlen=512))
        green_index +=1
        red_points.append(deque(maxlen=512))
        red_index +=1
        yellow_points.append(deque(maxlen=512))
        yellow_index +=1


        #now to draw anything 
    points=[blue_points,green_points,red_points,yellow_points]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1,len(points[i][j])):
                if points [i][j][k-1] is None or points[i][j][k]is None:
                    continue
                cv2.line(frame,points[i][j][k-1],points[i][j][k],colors[i],2)            
                cv2.line(paintWindow,points[i][j][k-1],points[i][j][k],colors[i],2)
    cv2.imshow("frame",frame)
    cv2.imshow("paint window",paintWindow)
    cv2.imshow("mask",Mask)
    if cv2.waitKey(1 ) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()                  
