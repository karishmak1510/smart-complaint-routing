import pickle

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

# Load vectorizer
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict(text):
    text = text.lower()  # lowercase

    # Convert text → vector
    text_vec = vectorizer.transform([text])

    # Predict department
    result = model.predict(text_vec)[0]

    return result