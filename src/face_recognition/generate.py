import cv2
import os
from unidecode import unidecode

_pathData = "D:/FaceReg/datasets/face_training"
face_detector = cv2.CascadeClassifier("D:/FaceReg/lib/haarcascade_frontalface_default.xml")

# kiểm tra đường dẫn trước khi tạo file
def _checkDir(mdd, name, dvct):
    key = unidecode(f"{mdd}_{name}_{dvct}".replace(" ", "").lower()) # Sử dụng f-string để tạo chuỗi
    new_fol = os.path.join(_pathData, key)  # Sử dụng os.path.join để tạo đường dẫn
    if not os.path.exists(new_fol):
        os.makedirs(new_fol)       
    return new_fol


def process_frame(frame, new_fol, count):
    faces = face_detector.detectMultiScale(frame, 1.3, 5)
    
    for (x, y, w, h) in faces:
        new_img = cv2.resize(frame[y+3: y+h-3, x+3: x+w-3], (160, 160))
        cv2.imwrite(f'{new_fol}/train_{count}.png', new_img)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # tạo hình chữ nhật
        count += 1   
        
    return frame, count

def gen(video_path, mdd, name, dvct):
    cam = cv2.VideoCapture(video_path)
    count = 0
    new_fol = _checkDir(mdd, name, dvct)
    
    while cam.isOpened():
        success, frame = cam.read()
        if not success:
            break
        
        # Xử lý frame và trả về frame đã nhận diện khuôn mặt
        frame, count = process_frame(frame, new_fol, count)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        if count == 200:
            break
    else:
        return
    
    cam.release()
    
    
    