import cv2
import os

_pathData = "./datasets/dataTraining"
img_path = 'imgs'
face_detector = cv2.CascadeClassifier("D:/FaceReg/lib/haarcascade_frontalface_default.xml")

def _checkDir(_pathData):
    name_fold = input('Nhap ten: ')
    new_folder = _pathData + '/' + name_fold
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)       
    return new_folder


def _postDataTrain(_pathData):
    cam = cv2.VideoCapture(0) #Su dung camera mac dinh
    count = 0
    new_fol = _checkDir(_pathData)
    while True :
        OK, frame = cam.read()
        faces = face_detector.detectMultiScale(frame, 1.3 , 5)
        for (x,y,w,h) in faces:
            new_img = cv2.resize(frame[y+3: y+h-3, x+3: x+w-3], (160,160))
            cv2.imwrite(new_fol + '/train_{}.png'.format(count), new_img)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2) # tao hinh chu nhat
            count+=1

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if(count == 10) :
            break
           
    cam.release()
    cv2.destroyAllWindows()

_postDataTrain(_pathData)