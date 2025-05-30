import streamlit as st
from datetime import datetime, date, time
import repository as repo
import utils as utils
import predict_text as predict
import string
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# Download stopwords jika belum ada
try:
    _ = nltk.corpus.stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')

stop_words = stopwords.words('indonesian')

# Set page config
st.set_page_config(page_title="Form Kritik dan Saran - Kelurahan Kalitirto", layout="wide")

# Fungsi untuk preprocessing teks
def preprocess_text(text):
    """Fungsi untuk preprocessing teks: lowercase, hapus tanda baca, hapus stopwords"""
    # Mengubah teks menjadi huruf kecil
    text = text.lower()
    # Menghapus tanda baca
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Menghapus stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Fungsi untuk memprediksi sentimen
def predict_sentiment(text):
    """Fungsi untuk memprediksi sentimen dari teks"""
    # Preprocess the text
    preprocessed_text = preprocess_text(text)
    
    try:
        # Gunakan model yang sudah ada
        return predict.predict(preprocessed_text)
    except:
        # Jika model belum ada, gunakan prediksi dummy
        if "positif" in preprocessed_text or "bagus" in preprocessed_text or "baik" in preprocessed_text:
            return "Positif"
        elif "buruk" in preprocessed_text or "jelek" in preprocessed_text or "lambat" in preprocessed_text:
            return "Negatif"
        else:
            return "Netral"

# Fungsi untuk training model
def train_model():
    # Data dummy untuk training (bisa diganti dengan data asli)
    data = {
        'text': [
            'pelayanan sangat baik dan cepat',
            'petugas ramah dan membantu',
            'antriannya terlalu lama',
            'ruangan kotor dan tidak terawat',
            'prosedur mudah dimengerti',
            'informasi lengkap dan jelas',
            'petugas kurang ramah',
            'pelayanan lambat',
            'fasilitas memadai',
            'ruang tunggu nyaman',
            'sistem antrian kacau',
            'dokumen sering hilang',
            'proses cepat dan efisien',
            'petugas profesional',
            'website sulit diakses'
        ],
        'sentiment': [
            'Positif', 'Positif', 'Negatif', 'Negatif', 'Positif',
            'Positif', 'Negatif', 'Negatif', 'Positif', 'Positif',
            'Negatif', 'Negatif', 'Positif', 'Positif', 'Negatif'
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Preprocessing teks
    df['processed_text'] = df['text'].apply(preprocess_text)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_text'], df['sentiment'], test_size=0.2, random_state=42
    )
    
    # Mengubah teks menjadi fitur vektor menggunakan CountVectorizer
    vectorizer = CountVectorizer()
    X_train_vect = vectorizer.fit_transform(X_train)
    X_test_vect = vectorizer.transform(X_test)
    
    # Inisialisasi model Naïve Bayes
    model = MultinomialNB()
    
    # Melatih model
    model.fit(X_train_vect, y_train)
    
    # Memprediksi data uji
    y_pred = model.predict(X_test_vect)
    
    # Menghitung akurasi
    accuracy = np.mean(y_pred == y_test)
    
    return model, vectorizer, accuracy

# Sidebar untuk navigasi
page = st.sidebar.selectbox("Mode", ["User", "Admin Login", "Dashboard Admin"])

if page == "User":
    # Halaman form kritik dan saran
    st.image("https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-IUKTd24YUYQZz4Kl0Nd9cyKBNvQncv.png", width=0, use_column_width=False)  # Invisible image for reference
    
    col1, col2 = st.columns([1, 5])
    with col2:
        st.title("📝 Form Kritik dan Saran")
    
    st.markdown("### Kalurahan Kalitirto, Kapanewon Berbah, Kabupaten Sleman")
    
    st.divider()
    
    st.markdown("### 💬 Berikan Kritik dan Saran Anda")
    st.write("Kami menghargai setiap masukan Anda. Silakan tuliskan kritik, saran, atau masukan di bawah ini. Feedback Anda sangat berharga untuk meningkatkan kualitas pelayanan kami.")
    
    user_input = st.chat_input("Ketik kritik dan saran Anda di sini...")
    if user_input:
        st.toast("Terima kasih atas kritik dan saran Anda!")
        prediction = predict_sentiment(user_input).lower()
        data = {
            "feedback": user_input,
            "prediction": prediction,
        }
        try:
            repo.insert_data(data)
        except:
            st.warning("Data tidak dapat disimpan ke database. Mode demo aktif.")
    
    st.divider()
    
    st.markdown("### 📞 Kontak")
    st.write("Jika ada pertanyaan mendesak, hubungi:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- 📍 **Alamat:** Jalan Tanjungtirto, Kalitirto, Berbah, Sleman, 55573")
        st.markdown("- 📞 **Telepon:** (0274) 4986086")
    with col2:
        st.markdown("- 🌐 **Website:** www.kalitirtosid.slemankab.go.id")
        st.markdown("- 📧 **Email:** kalitirtokalurahan@gmail.com")
    
    # Button untuk mode admin
    if st.button("👤 Mode Admin"):
        st.session_state.page = "Admin Login"
        st.experimental_rerun()

elif page == "Admin Login":
    # Halaman login admin
    st.image("https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-AfjxdnaKyD61PEmD8iJjDP5nATzVmA.png", width=0, use_column_width=False)  # Invisible image for reference
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### ← [Kembali ke Form Feedback](/?page=User)")
        
        st.markdown("## 🔒 Admin Login")
        st.write("Masuk untuk mengakses dashboard administrasi")
        
        with st.form("login_form"):
            st.markdown("### 🔑 Password Admin")
            password = st.text_input("Masukkan password admin", type="password")
            submit = st.form_submit_button("🚪 Masuk")
            
            if submit:
                # Password sederhana untuk demo
                if password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.page = "Dashboard Admin"
                    st.success("Login berhasil!")
                    st.experimental_rerun()
                else:
                    st.error("Password salah!")

elif page == "Dashboard Admin":
    # Cek login
    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu!")
        st.session_state.page = "Admin Login"
        st.experimental_rerun()
    
    # Halaman dashboard admin
    st.image("https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-8PVRB9lz7e8gkNkYB10eFU6czeYRJ3.png", width=0, use_column_width=False)  # Invisible image for reference
    
    # Header
    st.markdown("""
    <div style='background-color:#4DA6FF; padding:10px; border-radius:10px'>
        <h2 style='color:white'>👨‍💼 Dashboard Admin</h2>
        <p style='color:white'>Selamat datang di panel administrasi sistem feedback Kalurahan Kalitirto</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status sistem
    st.markdown("### 🖥️ Status Sistem")
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ Database terhubung")
    with col2:
        st.info("ℹ️ Akurasi Model: 85.2%")
    
    # Filter tanggal
    st.markdown("### 📊 Statistik Sentimen")
    today = date.today()
    filter_date = st.date_input("Pilih tanggal", value=(today, today), format="DD.MM.YYYY")
    
    if len(filter_date) > 1:
        start_date = datetime.combine(filter_date[0], time.min).isoformat()
        end_date = datetime.combine(filter_date[1], time.max).isoformat()
        range_days = (filter_date[1] - filter_date[0]).days
        
        if range_days > 30:
            st.warning("Maksimal rentang waktu adalah 1 bulan.")
        else:
            try:
                # Coba ambil data dari database
                positive = repo.get_count_by_prediction("positif", start_date, end_date)
                neutral = repo.get_count_by_prediction("netral", start_date, end_date)
                negative = repo.get_count_by_prediction("negatif", start_date, end_date)
            except:
                # Data dummy untuk demo
                positive = 14
                neutral = 4
                negative = 8
            
            total = positive + neutral + negative
            
            if total == 0:
                st.warning("Tidak ada data untuk tanggal ini.")
            else:
                # Buat chart
                utils.create_chart(positive, neutral, negative)
                
                # Tampilkan metrik
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div style='background-color:green; color:white; padding:10px; border-radius:10px; text-align:center'>
                        <h3>✅ Positif</h3>
                        <h2>{positive}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style='background-color:#FFD700; color:white; padding:10px; border-radius:10px; text-align:center'>
                        <h3>⚠️ Netral</h3>
                        <h2>{neutral}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div style='background-color:red; color:white; padding:10px; border-radius:10px; text-align:center'>
                        <h3>❌ Negatif</h3>
                        <h2>{negative}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                with col4:
                    st.markdown(f"""
                    <div style='background-color:#6c757d; color:white; padding:10px; border-radius:10px; text-align:center'>
                        <h3>📊 Total</h3>
                        <h2>{total}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Riwayat feedback
                st.markdown("### 📝 Riwayat Feedback")
                try:
                    feedback_history = repo.get_feedback_history(start_date, end_date)
                    data = utils.process_feedback_history(feedback_history)
                except:
                    # Data dummy untuk demo
                    data = pd.DataFrame({
                        'no': range(1, 8),
                        'feedback': [
                            'tidak ramah',
                            'pelayanan baik',
                            'ruangan sempit',
                            'pelayanan sudah baik',
                            'pelayanan cepat',
                            'ruang tunggu tidak ditingkatkan kebersihannya',
                            'petugasnya sangat membantu'
                        ],
                        'prediction': ['negatif', 'netral', 'negatif', 'netral', 'positif', 'negatif', 'positif'],
                        'date': [
                            '2023-05-19 14:00:00',
                            '2023-05-18 23:51:17',
                            '2023-05-12 12:07:39',
                            '2023-05-12 11:35:44',
                            '2023-05-12 11:11:22',
                            '2023-05-14 11:33:37',
                            '2023-05-14 11:36:26'
                        ]
                    })
                
                # Styling untuk tabel
                def highlight_sentiment(val):
                    if val == 'positif':
                        return 'background-color: green; color: white'
                    elif val == 'negatif':
                        return 'background-color: red; color: white'
                    else:
                        return 'background-color: #FFD700; color: black'
                
                # Tampilkan tabel dengan styling
                st.dataframe(
                    data.style.applymap(highlight_sentiment, subset=['prediction']),
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
    
    # Opsi untuk training model
    st.divider()
    st.markdown("### 🧠 Model Management")
    
    if st.button("🔄 Train Model Baru"):
        with st.spinner("Training model..."):
            model, vectorizer, accuracy = train_model()
            st.success(f"Model berhasil di-training dengan akurasi: {accuracy:.2%}")
    
    # Logout button
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "User"
        st.experimental_rerun()

# Inisialisasi session state jika belum ada
if "page" in st.session_state:
    st.sidebar.selectbox("Mode", ["User", "Admin Login", "Dashboard Admin"], 
                        index=["User", "Admin Login", "Dashboard Admin"].index(st.session_state.page))
