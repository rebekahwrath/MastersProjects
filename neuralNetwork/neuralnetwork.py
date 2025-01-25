# -*- coding: utf-8 -*-
"""neuralNetwork.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UAWFD8fOm_1Wfj67Ga45OosVQ-HNmRLV
"""

import tensorflow as tf

import pandas as pd

from google.colab import files
uploaded_files = files.upload()

import pandas as pd
import io

byte_data = uploaded_files['data.csv']

# Convert byte data to a file-like object using BytesIO
file_like = io.BytesIO(byte_data)

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(file_like, encoding='utf-8-sig')

# Display the first few rows of the DataFrame
df.head()

from sklearn.preprocessing import LabelEncoder

# Encode labels: 'ham' -> 0, 'spam' -> 1, from ChatGPT
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['label'])
df.head()

### NEURAL NETWORK

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

# Encode labels: 'ham' -> 0, 'spam' -> 1, allows the classifier to make a binary prediction
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['label'])

# Split data into train and test sets
X = df['message']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the text data using TF-IDF (Term Frequency-Inverse Document Frequency), converting text into numbers so the model can process it
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"Shape of training data: {X_train_tfidf.shape}")

# Convert sparse matrices to dense numpy arrays to avoid errors (neural network expects dense matrix)
X_train_tfidf = X_train_tfidf.toarray()  # Convert to dense array
X_test_tfidf = X_test_tfidf.toarray()    # Convert to dense array

# Check the shape to ensure conversion
print(f"Shape of training data: {X_train_tfidf.shape}")
print(f"Shape of test data: {X_test_tfidf.shape}")

# Build and compile the model, simplest model - add and build layers one by one
model = Sequential()

# Input layer + first hidden layer
model.add(Dense(512, input_dim=X_train_tfidf.shape[1], activation='relu'))
model.add(Dropout(0.2))  # Dropout to prevent overfitting

# Second hidden layer, receives data from the input layer
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))

# Output layer (binary classification: spam (1) or ham (0))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])

# Show the model summary
model.summary()

# Train the model
history = model.fit(X_train_tfidf, y_train, epochs=5, batch_size=64, validation_data=(X_test_tfidf, y_test))

# Save the trained model
model.save('spam_ham_classifier.keras')

# Evaluate the model on the test data
loss, accuracy = model.evaluate(X_test_tfidf, y_test)
print(f"Test accuracy: {accuracy:.4f}")

# Predict on the test data
y_pred = (model.predict(X_test_tfidf) > 0.5).astype(int)

# Evaluate performance
from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

def predict_message(message):
    message_tfidf = vectorizer.transform([message])  # Convert the message to TF-IDF format
    prediction = model.predict(message_tfidf)  # Predict using the trained model
    label = 'ham' if prediction < 0.5 else 'spam'
    return label

# Test the prediction function
test_message1 = "Congratulations, you've won a free iPhone! Click here to claim."
print(f"Prediction: {predict_message(test_message1)}")

test_message2 = "Hey! What are you up to this weekend? let's grab coffee"
print(f"Prediction: {predict_message(test_message2)}")

test_message3 = "dinner 2night? miss u m8"
print(f"Prediction: {predict_message(test_message3)}")