#execute this file first to detect moving objects and store the times the object enters and exits the frame
#press q to turn off webcam
import cv2, time, pandas
from datetime import datetime

first_frame = None #captures 1st frame (static bg img)
status_list=[None,None] #empty list to track status
times=[] #empty list to track times of motion
df=pandas.DataFrame(columns=["start","end"]) #empty df

video = cv2.VideoCapture(0,cv2.CAP_DSHOW)

while True:
    check, frame = video.read()
    status=0

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0) #blur grey img
    #assign initial bg img
    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame,None, iterations=2)

    #finding contours in current frame and filter based on area
    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contours in cnts:
        if cv2.contourArea(contours) <10000:
            continue
        status=1
        (x,y,w,h) = cv2.boundingRect(contours)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),5)

    #append each status for each frame
    status_list.append(status)

    #improve memory by only keep last 2 elements
    status_list=status_list[-2:]
    #recording when status changes
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key=cv2.waitKey(1)

    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break

print(status_list) #prints status list of last 2 elements
print(times)

#append times values to df
for i in range(0,len(times),2):
    df=df.append({"start":times[i],"end":times[i+1]}, ignore_index=True)

df.to_csv("MotionTimes.csv")

video.release()
cv2.destroyAllWindows