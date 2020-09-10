import joblib, json, pandas as pd
from sklearn import metrics
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

tweets_data = []

for line in open('Streamed-Data.txt', "r"):
    try: tweets_data.append(json.loads(line))
    except: continue
    
sent = pd.read_excel('Polarity-Sentiment.xlsx')

x, y = [], []

for i in range(len(tweets_data)):
    if tweets_data[i]['id'] == sent['id'][i]: x.append(tweets_data[i]['text']); y.append(sent['sentiment'][i])

vectorizer = CountVectorizer(stop_words='english')

X_train, X_test, y_train, y_test = train_test_split(vectorizer.fit_transform(x).toarray(), 
                                                    [int(r) for r in y], test_size=0.33, random_state=42)

svc = LinearSVC(); svc.fit(X_train, y_train)
predictions = svc.predict(X_test)

acc = metrics.accuracy_score(y_test, predictions)
print("Validation Accuracy: {0}".format(acc))
fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions, pos_label=1)
print("Area Under the Curve: {0}".format(metrics.auc(fpr, tpr)))

joblib.dump(svc, 'LinearSVC_Model.joblib')

print("\n-----------------------\n")

data, x = [], []
for line in open('Streamed-Data.txt', "r"):
    try: data.append(json.loads(line))
    except: continue
sent = pd.read_excel('Polarity-Sentiment.xlsx')
for i in range(len(data)):
    if data[i]['id'] == sent['id'][i]: x.append(data[i]['text']);
vectorizer = CountVectorizer(stop_words='english')
vectorizer.fit_transform(x)

svc = joblib.load('LinearSVC_Model.joblib')

print(svc.predict(vectorizer.transform(["I want to die depression sucks!"]))[0])

