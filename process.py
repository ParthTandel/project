from pymongo import MongoClient
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.model_selection import train_test_split


def preprocess():

    client = MongoClient()
    db = client.clusters
    cursor = db.articles.find()

    articleType = []
    articles = []

    for data in  cursor:
        if data['text'] != '' or data["summary"] != '' :

            if data['text'] != '' or data['text'] != 'Your browser does not support JavaScript.':
                articles.append(data['text'])
            else :
                articles.append(data['summary'])

            articleType.append(data['type'])

    features_train, features_test, labels_train, labels_test = train_test_split(articles, articleType, test_size=0.1, random_state=42)


    features_train_vect = features_train
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                 stop_words='english')
    features_train_transformed = vectorizer.fit_transform(features_train)
    features_test_transformed  = vectorizer.transform(features_test)


    selector = SelectPercentile(f_classif, percentile=1)
    selector.fit(features_train_transformed, labels_train)
    features_train_transformed = selector.transform(features_train_transformed).toarray()
    features_test_transformed  = selector.transform(features_test_transformed).toarray()
    return features_train_vect , features_train_transformed, features_test_transformed, labels_train, labels_test
