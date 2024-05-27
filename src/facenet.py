from keras_facenet import FaceNet
import numpy as np
import tensorflow as tf
import loading_face
import matplotlib.pyplot as plt  # Correctly import pyplot from matplotlib
# Initialize the FaceNet embedder
embedder = FaceNet()

# Initialize the face loading class with the path to the datase
    
def get_embedding(face_img):
    face_img = face_img.astype('float32')  # 3D (160x160x3)   
    face_img = np.expand_dims(face_img, axis=0)
    yhat = embedder.embeddings(face_img)
    return yhat[0]

def _load_save():
    faceloading = loading_face.FACELOADING("D:\\FaceReg\\datasets\\dataTraining")
    X, Y = faceloading.load_classes() 
    
    EMBEDDED_X = []
    for img in X:
        EMBEDDED_X.append(get_embedding(img))
    EMBEDDED_X = np.asarray(EMBEDDED_X)
    
    # Save model
    np.savez_compressed('faces_embeddings_done_4classes.npz', EMBEDDED_X, Y)
    return EMBEDDED_X, Y
