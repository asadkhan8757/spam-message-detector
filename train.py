import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Dataset load
df = pd.read_csv("dataset/spam.csv", encoding="latin-1")
# spam.csv me pehle 2 column kaam ke hain
df = df[['v1', 'v2']]
df.columns = ['label', 'message']
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

X = df['message']
y = df['label']

# Vectorizer + Model
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

# Save - Sahi tarike se
with open("spam_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model Ban Gaya! Accuracy:", model.score(X_vec, y))