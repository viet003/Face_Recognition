import cv2
import numpy as np
import os
import time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import pickle
from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder
import actions.action_data as actions
import actions.sql_connect as sql_connect

# Tải các mô hình và dữ liệu cần thiết
facenet = FaceNet()
faces_embedding = np.load("D:/FaceReg/lib/faces_embeddings_done_4classes.npz")
Y = faces_embedding['arr_1']
encoder = LabelEncoder()
encoder.fit(Y)
haarcascade = cv2.CascadeClassifier("D:/FaceReg/lib/haarcascade_frontalface_default.xml")
model = pickle.load(open('D:/FaceReg/lib/svm_model_160x160.pkl', 'rb'))

cnt = 0
pause_cnt = 0
justscanned = False

def process_frame(frame):
    rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = haarcascade.detectMultiScale(gray_img, 1.3, 5)

    global justscanned
    global pause_cnt
 
    pause_cnt += 1
    
    per = {
        'label': '',
        'confidence': 0
    }
    
    for x, y, w, h in faces:
        img = rgb_img[y:y+h, x:x+w]
        img = cv2.resize(img, (160, 160))
        img = np.expand_dims(img, axis=0)
        ypred = facenet.embeddings(img)
        
        # Dự đoán tên khuôn mặt và tính toán độ chính xác
        face_name = model.predict(ypred)
        probabilities = model.predict_proba(ypred)
        confidence = np.max(probabilities)
        
        # So sánh độ chính xác với ngưỡng 0.8
        if confidence > 0.8 and not justscanned:
            global cnt
            cnt += 1
            n = (100 / 30) * cnt
            w_filled = (cnt / 30) * w
            
            #name
            label = encoder.inverse_transform(face_name)[0]
            
            #kiểm tra và lấy ra nhãn chính xác nhất
            if(per['confidence'] < confidence):
                per['confidence'] = confidence
                per['label'] = label
                
            # thêm title và kẻ khung      
            cv2.putText(frame, label, (x + 20, y + h + 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 10)
            cv2.rectangle(frame, (x, y + h + 40), (x + int(w_filled), y + h + 50), (153, 255, 255), cv2.FILLED)


            if int(cnt) == 30:
                cnt = 0
                per_arr = per['label'].split('_')
                user_key = per_arr[0]
                
                if(actions.check_scan_today(sql_connect.connect_mysql(), user_key)):
                    cv2.putText(frame, 'Đã hoàn thành!', (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)
                else:
                    actions.insert_attendance(sql_connect.connect_mysql(), user_key)
                
                cv2.putText(frame, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)
                time.sleep(1)
                
                justscanned = True
                pause_cnt = 0
 
        else:
            if not justscanned:
                # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 10)
                cv2.putText(frame, str('unknown'), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 10)
            else:
                # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 10)
                cv2.putText(frame, str(''), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

            if pause_cnt > 80:
                justscanned = False
        
    
    print(per['confidence'],' ', per['label'])
    
    return frame


def _run(video_path):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        # Xử lý frame và trả về frame đã nhận diện khuôn mặt
        frame = process_frame(frame)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
    cap.release()
  