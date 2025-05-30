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
import predict_text as predict

# Inisialisasi session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_admin_login" not in st.session_state:
    st.session_state.show_admin_login = False

# Password admin sederhana
ADMIN_PASSWORD = "admin123"

# CSS untuk styling
st.markdown("""
<style>
    .main-content {
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .header-section {
        padding: 0.5rem 0;
        margin-bottom: 1.5rem;
        color: #2c3e50;
        text-align: center;
    }
    
    .header-section h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #2c3e50;
    }
    
    .header-section h2 {
        font-size: 1.8rem;
        font-weight: 500;
        margin-bottom: 1rem;
        color: #34495e;
    }
    
    .header-section hr {
        border: none;
        height: 1px;
        background: #dee2e6;
        margin: 1.5rem auto;
        width: 60%;
    }
    
    .header-section h3 {
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #2c3e50;
        text-align: left;
    }
    
    .header-section .support-text {
        font-size: 1rem;
        color: #6c757d;
        line-height: 1.6;
        text-align: justify;
        margin-bottom: 1rem;
    }
    
    .admin-panel {
        background: #4facfe;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.3);
    }
    
    .status-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        animation: slideIn 0.3s ease-out;
        max-width: 400px;
    }
    
    .notification-success {
        background: linear-gradient(135deg, #28a745, #20c997);
    }
    
    .notification-error {
        background: linear-gradient(135deg, #dc3545, #e74c3c);
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
    
    .metric-box-positif {
        background: #28a745 !important;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        margin-bottom: 1rem;
    }

    .metric-box-netral {
        background: #ffc107 !important;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
        margin-bottom: 1rem;
    }

    .metric-box-negatif {
        background: #dc3545 !important;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
        margin-bottom: 1rem;
    }

    .metric-box-total {
        background: #6c757d !important;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
        margin-bottom: 1rem;
    }

    .metric-label {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: white !important;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white !important;
        margin: 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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

# Simple admin login function
def admin_login_form():
    # Container untuk judul yang lebih rapi
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 3rem 0;">
        <h1 style="font-size: 2.5rem; color: #2c3e50; margin-bottom: 0.5rem; font-weight: 700;">🔒 Admin Login</h1>
        <p style="font-size: 1.1rem; color: #6c757d; margin: 0;">Masuk untuk mengakses dashboard administrasi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form dalam container yang terpisah
    with st.container():
        with st.form("admin_login_form", clear_on_submit=True):
            st.markdown("### 🔑 Password Admin")
            password = st.text_input("Masukkan password admin", type="password", placeholder="Password...")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button("🚪 Masuk", use_container_width=True)
            
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
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Kembali ke Form Feedback", key="back_to_user", use_container_width=True):
            st.session_state.show_admin_login = False
            st.rerun()
    
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    admin_login_form()

elif st.session_state.admin_logged_in:
    # Dashboard Admin
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header admin dengan tombol logout di kiri
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🚪 Logout", key="admin_logout_btn"):
            st.session_state.admin_logged_in = False
            st.success("✅ Logout berhasil!")
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="admin-panel">
            <h1>👨‍💼 Dashboard Admin</h1>
            <p>Selamat datang di panel administrasi sistem feedback Kelurahan Kalitirto</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Status Connection
    st.markdown("""
    <div class="status-card">
        <strong>📊 Status Sistem</strong><br>
        ✅ Database terhubung | 🎯 Akurasi Model: 85.2%
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
        <h3>💬 Berikan Kritik dan Saran Anda</h3>
        <p class="support-text">
            Kami menghargai setiap masukan Anda. Silakan tuliskan kritik, saran, atau masukan di bawah ini. 
            Feedback Anda sangat berharga untuk meningkatkan kualitas pelayanan kami.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form feedback dengan text area dan tombol submit
    with st.form("feedback_form", clear_on_submit=True):
        user_input = st.text_area("Ketik kritik dan saran Anda di sini...", height=150, placeholder="Ketik kritik dan saran Anda di sini...")
        
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
