import string
import connection as conn
import nltk
from nltk.corpus import stopwords
import os

try:
    _ = nltk.corpus.stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')

# Load model dan vectorizer dari file pkl
try:
    model = conn.load_model()
    vectorizer = conn.load_vectorizer()
    model_loaded = True
except Exception as e:
    print(f"Error loading model: {e}")
    model_loaded = False

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
    
    if model_loaded:
        try:
            # Vectorize the text
            vectorized_text = vectorizer.transform([preprocessed_text])
            
            # Predict sentiment
            prediction = model.predict(vectorized_text)
            
            return prediction[0]
        except Exception as e:
            print(f"Error during prediction: {e}")
            # Fallback jika ada error
            return fallback_prediction(preprocessed_text)
    else:
        # Jika model tidak berhasil dimuat, gunakan fallback
        return fallback_prediction(preprocessed_text)

def fallback_prediction(text):
    """Fungsi prediksi fallback sederhana jika model tidak tersedia"""
    if "baik" in text or "bagus" in text or "puas" in text or "senang" in text or "cepat" in text:
        return "Positif"
    elif "buruk" in text or "lambat" in text or "kecewa" in text or "lama" in text or "kotor" in text:
        return "Negatif"
    else:
        return "Netral"

def check_models_available():
    """Check if model files are available"""
    return os.path.exists('model.pkl') and os.path.exists('vectorizer.pkl')

def get_model_accuracy():
    """Get model accuracy (dummy implementation)"""
    try:
        # In real implementation, this would calculate actual accuracy
        return "85.2"
    except:
        return None
