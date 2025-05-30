import string
import connection as conn
import nltk
from nltk.corpus import stopwords

try:
    _ = nltk.corpus.stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')

model = conn.load_model()
vectorizer = conn.load_vectorizer()
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
    
    # Vectorize the text
    vectorized_text = vectorizer.transform([preprocessed_text])
    
    # Predict sentiment (dummy prediction for illustration)
    prediction = model.predict(vectorized_text)
    
    return prediction[0]
