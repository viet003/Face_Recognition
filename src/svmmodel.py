from sklearn.preprocessing import LabelEncoder
import facenet
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle


EMBEDDED_X, Y = facenet._load_save()

encoder = LabelEncoder()
encoder.fit(Y)
Y = encoder.transform(Y)

X_train, X_test, Y_train, Y_test = train_test_split(EMBEDDED_X, Y, shuffle=True, random_state=17)
model = SVC(kernel='linear', probability=True)
model.fit(X_train, Y_train)

ypreds_train = model.predict(X_train)
ypreds_test = model.predict(X_test)

accuracy_score(Y_train, ypreds_train)
accuracy_score(Y_test,ypreds_test)

# save the model
with open('svm_model_160x160.pkl','wb') as f:
    pickle.dump(model,f)