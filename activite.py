import cv2
import pyttsx3 as ps



def r_f():

    _, prev = cap.read()
    prev = cv2.flip(prev, 1)

	_, new = cap.read()
    new = cv2.flip(new, 1)
    thres = 0.45 
    
    # Threshold to detect object
    #img = cv2.imread('lena.png') 
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    cap.set(10,70)
    
    classNames= []
    classFile = 'vovo.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')
    
    configPath = 'ssd.pbtxt'
    weightsPath = 'ref.pb'
        
    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    
    while True:
        success,img = cap.read()
        classIds, confs, bbox = net.detect(img,confThreshold=thres)
        print(classIds,bbox)
    
        if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                cv2.rectangle(img,box,color=(255,255,0),thickness=1)
                cv2.putText(img,classNames[classId-1].upper(),(box[0]+5,box[1]+15),
                            cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1)
                #cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                #cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    
        cv2.imshow("vue",img)
        cv2.waitKey(1)

    

r_f()