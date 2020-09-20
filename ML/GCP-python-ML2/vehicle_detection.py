import cv2
print(cv2.__version__)

cascade_src = 'cars.xml'
video_src = 'dataset/video2.avi'

cap = cv2.VideoCapture(video_src)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
car_cascade = cv2.CascadeClassifier(cascade_src)
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
while True:
    ret, img = cap.read()
    if (type(img) == type(None)):
        break
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    for (x,y,w,h) in cars:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)  
    out.write(img)    
    
    cv2.imshow('video', img)
    
    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()
