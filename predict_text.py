import string
import connection as conn
import nltk
from nltk.corpus import stopwords

try:
    _ = nltk.corpus.stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')

# Load model dan vectorizer dengan error handling
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
    # Cek apakah model dan vectorizer berhasil dimuat
    if model is None or vectorizer is None:
        # Fallback prediction berdasarkan kata kunci sederhana
        return predict_fallback(text)
    
    try:
        # Preprocess the text
        preprocessed_text = preprocess_text(text)
        
        # Vectorize the text
        vectorized_text = vectorizer.transform([preprocessed_text])
        
        # Predict sentiment
        prediction = model.predict(vectorized_text)
        
        return prediction[0]
    except Exception as e:
        print(f"Error in prediction: {e}")
        # Fallback ke prediksi sederhana
        return predict_fallback(text)

def predict_fallback(text):
    """Prediksi sederhana berdasarkan kata kunci jika model tidak tersedia"""
    text_lower = text.lower()
    
    # Kata-kata positif
    positive_words = ['baik', 'bagus', 'senang', 'puas', 'terima kasih', 'memuaskan', 
                     'ramah', 'cepat', 'profesional', 'membantu', 'lancar']
    
    # Kata-kata negatif  
    negative_words = ['buruk', 'jelek', 'lambat', 'lama', 'kecewa', 'marah', 
                     'tidak puas', 'mengecewakan', 'sulit', 'rumit', 'kotor']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return 'positif'
    elif negative_count > positive_count:
        return 'negatif'
    else:
        return 'netral'
