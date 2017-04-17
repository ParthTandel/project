from time import time
from process import preprocess
features_train_vect,features_train, features_test, labels_train, labels_test = preprocess()

from sklearn.svm import SVC
clf = SVC(C=10000.0,kernel="linear")
t0 = time()
clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"
import collections

t0 = time()
pred = clf.predict(features_test)
print "prediction time:", round(time()-t0, 3), "s"
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(pred , labels_test)
print accuracy
