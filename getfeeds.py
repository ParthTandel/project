from pymongo import MongoClient
from pprint import pprint
import spacy
client = MongoClient()
db = client.clusters
cursor = db.articles.find();

countInd = {};
count = 0;
for data in  cursor:
    if data['text'] != '' or data["summary"] != '' :
        if not countInd.has_key(data['type']):
            countInd[data['type']] = 0
        countInd[data['type']] = countInd[data['type']]  + 1;
        # count = count + 1
        print "*****************************";
        print data['text']
        # print str(countInd[data['type']]) +"  "+data['type']+" "+ data['title']
        print "*****************************";
# pprint(countInd);
