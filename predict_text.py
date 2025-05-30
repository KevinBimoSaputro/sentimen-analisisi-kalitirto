import string
import connection as conn
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np

try:
    _ = nltk.corpus.stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')

try:
    model = conn.load_model()
    vectorizer = conn.load_vectorizer()
except:
    # Jika model tidak ada, buat model dummy
    # Data dummy untuk training
    data = {
        'text': [
            'pelayanan sangat baik dan cepat',
            'petugas ramah dan membantu',
            'antriannya terlalu lama',
            'ruangan kotor dan tidak terawat',
            'prosedur mudah dimengerti'
        ],
        'sentiment': [
            'Positif', 'Positif', 'Negatif', 'Negatif', 'Positif'
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Preprocessing
    stop_words = stopwords.words('indonesian')
    
    def preprocess_text(text):
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = ' '.join([word for word in text.split() if word not in stop_words])
        return text
    
    df['processed_text'] = df['text'].apply(preprocess_text)
    
    # Vectorize
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['processed_text'])
    
    # Train model
    model = MultinomialNB()
    model.fit(X, df['sentiment'])

stop_words = stopwords.words('indonesian')

def preprocess_text(text):
    """Fungsi untuk preprocessing teks: lowercase, hapus tanda baca, hapus stopwords"""
    # Mengubah teks menjadi huruf kecil
    text = text.lower()
    # Menghapus tanda baca
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Menghapus stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

def predict(text):
    """Fungsi untuk memprediksi sentimen dari teks"""
    # Preprocess the text
    preprocessed_text = preprocess_text(text)
    
    try:
        # Vectorize the text
        vectorized_text = vectorizer.transform([preprocessed_text])
        
        # Predict sentiment
        prediction = model.predict(vectorized_text)
        
        return prediction[0]
    except:
        # Fallback jika ada error
        if "baik" in preprocessed_text or "bagus" in preprocessed_text or "puas" in preprocessed_text:
            return "Positif"
        elif "buruk" in preprocessed_text or "lambat" in preprocessed_text or "kecewa" in preprocessed_text:
            return "Negatif"
        else:
            return "Netral"
