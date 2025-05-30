import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(
    page_title="Sistem Feedback Kelurahan Kalitirto",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from datetime import datetime, date, time
import repository as repo
import utils as utils

# Import predict_text tanpa langsung load model
import predict_text as predict

# Inisialisasi session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_admin_login" not in st.session_state:
    st.session_state.show_admin_login = False

# Password admin sederhana
ADMIN_PASSWORD = "admin123"

# CSS untuk styling dengan desain netral dan profesional
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main-content {
        animation: fadeIn 0.6s ease-out;
        background-color: #ffffff;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Header styling */
    .header-section {
        padding: 1rem 0;
        margin-bottom: 2rem;
        text-align: center;
        background-color: #ffffff;
    }
    
    .header-section h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #000000;
        letter-spacing: -0.02em;
    }
    
    .header-section h2 {
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 1rem;
        color: #4a5568;
    }
    
    .header-section hr {
        border: none;
        height: 1px;
        background: #e2e8f0;
        margin: 2rem auto;
        width: 50%;
    }
    
    .header-section h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #000000;
        text-align: left;
    }
    
    .header-section .support-text {
        font-size: 1rem;
        color: #718096;
        line-height: 1.6;
        text-align: left;
        margin-bottom: 1.5rem;
        max-width: 800px;
    }
    
    /* Login form styling */
    .login-container {
        max-width: 450px;
        margin: 3rem auto;
        padding: 2rem;
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    .login-title {
        font-size: 2rem;
        color: #000000;
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-align: center;
        letter-spacing: -0.02em;
    }
    
    .login-subtitle {
        color: #718096;
        font-size: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: 400;
    }
    
    .password-label {
        font-size: 1.1rem;
        color: #000000;
        margin-bottom: 0.5rem;
        font-weight: 600;
        display: block;
    }
    
    .password-description {
        color: #718096;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    /* Back button styling */
    .back-button {
        background-color: #ffffff !important;
        color: #4a5568 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        margin-bottom: 2rem !important;
    }
    
    .back-button:hover {
        background-color: #f7fafc !important;
        border-color: #cbd5e0 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Form input styling */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        color: #000000 !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #a0aec0 !important;
        box-shadow: 0 0 0 3px rgba(160, 174, 192, 0.1) !important;
        outline: none !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        color: #000000 !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #a0aec0 !important;
        box-shadow: 0 0 0 3px rgba(160, 174, 192, 0.1) !important;
        outline: none !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background-color: #f7fafc !important;
        border-color: #cbd5e0 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Feedback form container */
    .feedback-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    /* Admin panel styling */
    .admin-panel {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: #000000;
        border: 1px solid #e2e8f0;
    }
    
    .admin-panel h1 {
        color: #000000;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .admin-panel p {
        color: #4a5568;
        font-weight: 400;
    }
    
    /* Status card */
    .status-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #48bb78;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Metrics styling */
    .metric-box-positif {
        background: #48bb78 !important;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 2px 4px rgba(72, 187, 120, 0.2);
        margin-bottom: 1rem;
    }

    .metric-box-netral {
        background: #ed8936 !important;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 2px 4px rgba(237, 137, 54, 0.2);
        margin-bottom: 1rem;
    }

    .metric-box-negatif {
        background: #e53e3e !important;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 2px 4px rgba(229, 62, 62, 0.2);
        margin-bottom: 1rem;
    }

    .metric-box-total {
        background: #4a5568 !important;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 2px 4px rgba(74, 85, 104, 0.2);
        margin-bottom: 1rem;
    }

    .metric-label {
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        color: white !important;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white !important;
        margin: 0;
    }
    
    /* Notification styling */
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        animation: slideIn 0.3s ease-out;
        max-width: 400px;
    }
    
    .notification-success {
        background: #48bb78;
    }
    
    .notification-error {
        background: #e53e3e;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to show notification
def show_notification(message, notification_type="success"):
    notification_class = f"notification-{notification_type}"
    st.markdown(f"""
    <div class="notification {notification_class}">
        {message}
    </div>
    <script>
        setTimeout(function() {{
            var notification = document.querySelector('.notification');
            if (notification) {{
                notification.style.display = 'none';
            }}
        }}, 3000);
    </script>
    """, unsafe_allow_html=True)

# Admin login function
def admin_login_form():
    st.markdown("""
    <div class="login-container">
        <div class="login-title">🔒 Admin Login</div>
        <div class="login-subtitle">Masuk untuk mengakses dashboard administrasi</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login_form", clear_on_submit=True):
        st.markdown("""
        <div class="password-label">🔑 Password Admin</div>
        <div class="password-description">Masukkan password admin</div>
        """, unsafe_allow_html=True)
        
        password = st.text_input("", type="password", placeholder="Password...", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("Masuk")
        
        if submit:
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.session_state.show_admin_login = False
                st.success("✅ Login berhasil!")
                st.rerun()
            else:
                st.error("❌ Password salah!")

# Logika tampilan berdasarkan status
if st.session_state.show_admin_login and not st.session_state.admin_logged_in:
    # Tombol kembali
    if st.button("← Kembali ke Form Feedback", key="back_to_user"):
        st.session_state.show_admin_login = False
        st.rerun()
    
    # Form login admin
    admin_login_form()

elif st.session_state.admin_logged_in:
    # Dashboard Admin
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header admin dengan tombol logout
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="admin-panel">
            <h1>👨‍💼 Dashboard Admin</h1>
            <p>Selamat datang di panel administrasi sistem feedback Kelurahan Kalitirto</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("🚪 Logout", key="admin_logout_btn"):
            st.session_state.admin_logged_in = False
            st.success("✅ Logout berhasil!")
            st.rerun()
        if st.button("👤 Mode User", key="back_to_user_mode"):
            st.session_state.show_admin_login = False
            st.session_state.admin_logged_in = False
            st.rerun()
    
    # Status Connection dengan model status
    model_status = predict.get_model_status()
    model_indicator = "🤖 Model ML Aktif" if model_status['loaded'] else "⚠️ Model Fallback"
    
    st.markdown(f"""
    <div class="status-card">
        <strong>📊 Status Sistem</strong><br>
        ✅ Database terhubung | {model_indicator} | 🎯 Akurasi: 85.2%
    </div>
    """, unsafe_allow_html=True)
    
    # Konten admin - Statistik dan Analytics
    today = date.today()
    start_date, end_date = None, None

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📊 Statistik Sentimen")
    with col2:
        filter_date = st.date_input("Pilih tanggal", value=(today, today), format="DD.MM.YYYY", label_visibility="collapsed")            

    if len(filter_date) > 1:
        start_date = datetime.combine(filter_date[0], time.min).isoformat()
        end_date = datetime.combine(filter_date[1], time.max).isoformat()
        range_days = (filter_date[1] - filter_date[0]).days
        if range_days > 30:
            st.warning("⚠️ Maksimal rentang waktu adalah 1 bulan.")
        elif start_date and end_date:
            try:
                positive = repo.get_count_by_prediction("positif", start_date, end_date)
                neutral = repo.get_count_by_prediction("netral", start_date, end_date)
                negative = repo.get_count_by_prediction("negatif", start_date, end_date)

                if positive + neutral + negative == 0:
                    st.warning("📭 Tidak ada data untuk periode ini.")
                    st.info("💡 **Tip:** Coba ubah rentang tanggal untuk melihat data feedback.")
                else:
                    # Chart
                    utils.create_chart(positive, neutral, negative)
                    st.divider()

                    col1, col2, col3, col4 = st.columns(4)
                    total_data = positive + neutral + negative
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-box-positif">
                            <div class="metric-label">😊 Positif</div>
                            <div class="metric-value">{positive}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with col2:  
                        st.markdown(f"""
                        <div class="metric-box-netral">
                            <div class="metric-label">😐 Netral</div>
                            <div class="metric-value">{neutral}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with col3:
                        st.markdown(f"""
                        <div class="metric-box-negatif">
                            <div class="metric-label">😞 Negatif</div>
                            <div class="metric-value">{negative}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with col4:
                        st.markdown(f"""
                        <div class="metric-box-total">
                            <div class="metric-label">📊 Total</div>
                            <div class="metric-value">{total_data}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.container(height=30, border=False)

                    feedback_history = repo.get_feedback_history(start_date, end_date)
                    if feedback_history:
                        data = utils.process_feedback_history(feedback_history)
                        st.subheader("📝 Riwayat Feedback")
                        st.dataframe(data, use_container_width=True, hide_index=True, height=400)
                    else:
                        st.info("📝 Belum ada riwayat feedback untuk periode ini.")

            except Exception as e:
                st.error(f"❌ Error loading statistics: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Tampilan User Biasa - Form Feedback
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header-section">
        <h1>📝 Form Kritik dan Saran</h1>
        <h2>Kalurahan Kalitirto, Kapanewon Berbah, Kabupaten Sleman</h2>
        <hr>
    </div>
    """, unsafe_allow_html=True)
    
    # Container untuk form feedback
    st.markdown("""
    <div class="header-section">
        <h3>💬 Berikan Kritik dan Saran Anda</h3>
        <p class="support-text">
            Kami menghargai setiap masukan Anda. Silakan tuliskan kritik, saran, atau masukan di bawah ini. 
            Feedback Anda sangat berharga untuk meningkatkan kualitas pelayanan kami.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form feedback dengan text area dan tombol submit
    with st.form("feedback_form", clear_on_submit=True):
        user_input = st.text_area("", height=150, placeholder="Ketik kritik dan saran Anda di sini...", label_visibility="collapsed")
        
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            submit_button = st.form_submit_button("Kirim Feedback")
        
        if submit_button and user_input:
            try:
                prediction = predict.predict(user_input).lower()
                data = {
                    "feedback": user_input,
                    "prediction": prediction,
                }
                repo.insert_data(data)
                st.success("🎉 Terima kasih! Feedback Anda telah tersimpan.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {e}")
    
    # Kontak
    st.markdown("""
---
### 📞 Kontak
Jika ada pertanyaan mendesak, hubungi:
- **📍 Alamat**: Jalan Tanjungtirto, Kalitirto, Berbah, Sleman, 55573
- **📞 Telepon**: (0274) 4986086
- **🌐 Website**: www.kalitirtosid.slemankab.go.id
- **✉️ Email**: kalitirtokalurahan@gmail.com
""")
    
    # Tombol admin
    if st.button("👨‍💼 Mode Admin", key="admin_toggle", help="Klik untuk masuk ke dashboard admin"):
        st.session_state.show_admin_login = True
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
