from sklearn.preprocessing import LabelEncoder
import src.face_recognition.facenet as facenet
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle


def train_model():
    # lấy dữ liệu
    EMBEDDED_X, Y = facenet._load_save()
    encoder = LabelEncoder()
    encoder.fit(Y)
    Y = encoder.transform(Y)

    # chuẩn bị dữ liệu cho quá trình huấn luyện
    X_train, X_test, Y_train, Y_test = train_test_split(EMBEDDED_X, Y, shuffle=True, random_state=17)
    model = SVC(kernel='linear', probability=True)
    model.fit(X_train, Y_train)

    # kiểm tra độ chính xác
    print("Kiểm tra độ chính xác...")
    pred_accuracy = model.score(X_test, Y_test)
    print(f"Độ chính xác = {pred_accuracy * 100:.3f} %")

    # lưu dữ liệu đã được huấn luyện
    with open('D:/FaceReg/lib/svm_model_160x160.pkl','wb') as f:
        pickle.dump(model,f)
        
    return True
train_model()