import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('spam.tsv', sep='\t')

hamDf = df[df['label'] == "ham"]
spamDf = df[df['label'] == "spam"]

hamDf = hamDf.sample(spamDf.shape[0])

finalDf = pd.concat([hamDf, spamDf], ignore_index=True)

X_train, X_test, Y_train, Y_test = train_test_split(finalDf['message'], finalDf['label'], test_size=0.2, random_state=0, shuffle=True, stratify=finalDf['label'])

model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('svc', SVC(C=1000, gamma='auto'))
])

model.fit(X_train, Y_train)

Y_predict = model.predict(X_test)

accuracy = accuracy_score(Y_test, Y_predict)
report = classification_report(Y_test, Y_predict)

print("Accuracy:", accuracy)
print("Classification Report:")
print(report)

sample_messages = [
    "Congratulations you have won a lottery",
    "Buy our exclusive products at discount prices",
    "Get rich quick with our amazing scheme",
    "Hello, how are you today?",
    "Check out our new website",
    "Claim your prize now"
]

predictions = model.predict(sample_messages)

print("Sample Message Predictions:")
for message, prediction in zip(sample_messages, predictions):
    print(f"Message: {message} | Prediction: {prediction}")

# Save the trained model
#joblib.dump(model, "mySVCModel.pkl")