from time import time
from process import preprocess
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif


features_train_vect,features_train, features_test, labels_train, labels_test = preprocess()

from sklearn.neighbors import KNeighborsClassifier
t0 = time()
neigh = KNeighborsClassifier(n_neighbors = 5)
neigh.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"


pred = neigh.predict(features_test)
print "prediction time:", round(time()-t0, 3), "s"
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(pred , labels_test)
print accuracy


from bs4 import BeautifulSoup
from newspaper import Article

urls = ['http://www.newsmax.com/Politics/putin-tv-trump-dangerous/2017/04/17/id/784706/',
        'http://www.hollywoodreporter.com/heat-vision/star-wars-rare-archival-footage-shown-at-celebration-had-funny-new-hope-f-bomb-994552?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+thr%2Ffilm+%28The+Hollywood+Reporter+-+Movies%29&utm_content=FeedBurner',
        'http://www.espn.com/sports/endurance/story/_/id/19177433/boston-marathon-2017-devin-wang-another-year-brings-closure-tragedy']

prediction_data = []
for url in urls:

    article = Article(url)
    article.download()
    article.parse()
    soupText = BeautifulSoup(article.text);
    prediction_data.append(soupText.get_text());


vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
features_train_transformed = vectorizer.fit_transform(features_train_vect)
features_test_transformed  = vectorizer.transform(prediction_data)
selector = SelectPercentile(f_classif, percentile=1)
selector.fit(features_train_transformed, labels_train)
features_test_transformed  = selector.transform(features_test_transformed).toarray()


pred = neigh.predict(features_test_transformed)

print pred
