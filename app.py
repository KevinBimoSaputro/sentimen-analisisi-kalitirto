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
import auth
import time as time_module

# Inisialisasi session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_admin_login" not in st.session_state:
    st.session_state.show_admin_login = False
if "show_notification" not in st.session_state:
    st.session_state.show_notification = False
if "notification_message" not in st.session_state:
    st.session_state.notification_message = ""
if "notification_type" not in st.session_state:
    st.session_state.notification_type = "success"

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
        width: 100%;
        margin-left: 0;
        margin-right: 0;
        padding: 0;
        text-align: left;
    }
    
    .header-section .support-text {
        font-size: 1rem;
        color: #6c757d;
        line-height: 1.6;
        width: 100%;
        margin: 0;
        padding: 0;
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
    
    /* Custom notification styles */
    .custom-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        animation: slideIn 0.3s ease-out, fadeOut 0.3s ease-out 5.7s forwards;
        max-width: 400px;
        word-wrap: break-word;
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
    
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
    
    /* Uniform admin buttons */
    .stButton > button {
        background: white !important;
        color: #6c757d !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        background: #f8f9fa !important;
        border-color: #6c757d !important;
        color: #495057 !important;
    }
    
    /* Clean metric boxes without borders */
    .metric-box-positif {
        background: #28a745 !important;
        border: none !important;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    }
    .metric-box-positif:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
    }

    .metric-box-netral {
        background: #ffc107 !important;
        border: none !important;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    }
    .metric-box-netral:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 193, 7, 0.4);
    }

    .metric-box-negatif {
        background: #dc3545 !important;
        border: none !important;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    }
    .metric-box-negatif:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4);
    }

    .metric-box-total {
        background: #6c757d !important;
        border: none !important;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    }
    .metric-box-total:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(108, 117, 125, 0.4);
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
    
    /* Hide default streamlit notifications */
    .stAlert {
        display: none !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-section {
            padding: 0.3rem 0;
        }
        
        .header-section h1 {
            font-size: 2rem;
            margin-bottom: 0.2rem;
        }
        
        .header-section h2 {
            font-size: 1.5rem;
            margin-bottom: 0.8rem;
        }
        
        .header-section hr {
            margin: 1rem auto;
        }
        
        .header-section h3 {
            font-size: 1.4rem;
            text-align: left;
            margin-bottom: 0.6rem;
        }
        
        .header-section .support-text {
            font-size: 0.95rem;
            text-align: center;
            margin-bottom: 0.8rem;
        }
        
        .metric-value {
            font-size: 2rem !important;
        }
        
        .metric-label {
            font-size: 1rem !important;
        }
        
        .custom-notification {
            top: 10px;
            right: 10px;
            left: 10px;
            max-width: none;
        }
    }
</style>
""", unsafe_allow_html=True)

# Check if models are available
try:
    model_available = predict.check_models_available()
except:
    model_available = False

if not model_available:
    # Enhanced model generation page
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h1>🤖 Setup Model Machine Learning</h1>
        <p style="font-size: 1.2rem; color: #666; margin: 2rem 0;">
            Sistem memerlukan model AI untuk analisis sentimen feedback.<br>
            Klik tombol di bawah untuk membuat model secara otomatis.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔧 Generate Models", key="generate_models", help="Klik untuk membuat model ML"):
            with st.spinner("🔄 Sedang membuat model ML... Mohon tunggu..."):
                try:
                    import create_models
                    success = create_models.create_dummy_models()
                    if success:
                        st.success("✅ Model berhasil dibuat! Aplikasi akan dimuat ulang...")
                        # Clear cache and rerun
                        st.cache_resource.clear()
                        st.rerun()
                    else:
                        st.error("❌ Gagal membuat model. Silakan coba lagi.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    st.markdown("""
    ---
    ### ℹ️ Informasi
    - **Proses ini hanya dilakukan sekali** saat pertama kali setup
    - **Model akan tersimpan otomatis** untuk penggunaan selanjutnya  
    - **Waktu proses**: sekitar 10-30 detik
    - **Tidak memerlukan internet** - semua proses lokal
    """)
    st.stop()

# Function to show custom notification
def show_notification(message, notification_type="success"):
    st.session_state.show_notification = True
    st.session_state.notification_message = message
    st.session_state.notification_type = notification_type
    
    # JavaScript to hide notification after 2 seconds
    notification_class = f"notification-{notification_type}"
    st.markdown(f"""
    <div class="custom-notification {notification_class}" id="customNotification">
        {message}
    </div>
    <script>
        setTimeout(function() {{
            var notification = document.getElementById('customNotification');
            if (notification) {{
                notification.style.display = 'none';
            }}
        }}, 6000);
    </script>
    """, unsafe_allow_html=True)

# Logika tampilan berdasarkan status
if st.session_state.show_admin_login and not auth.is_admin_logged_in():
    # Tombol kembali di tengah atas dengan spacing yang lebih baik
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Kembali ke Form Feedback", key="back_to_user", use_container_width=True):
            st.session_state.show_admin_login = False
            st.rerun()
    
    # Spacing antara tombol dan form
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    
    # Form login admin tanpa column wrapper - langsung ke kiri
    auth.admin_login_form()

elif auth.is_admin_logged_in():
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
            auth.admin_logout()
        if st.button("👤 Mode User", key="back_to_user_mode"):
            st.session_state.show_admin_login = False
            st.session_state.admin_logged_in = False
            st.rerun()
    
    # Status Connection (Simple) - Hapus total feedback
    connection_status = repo.get_connection_status()
    model_accuracy = predict.get_model_accuracy()

    if connection_status:
        accuracy_text = f" | 🎯 Akurasi Model: {model_accuracy}%" if model_accuracy else ""
        st.markdown(f"""
        <div class="status-card">
            <strong>📊 Status Sistem</strong><br>
            ✅ Database terhubung{accuracy_text}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Database tidak terhubung. Periksa konfigurasi.")
    
    # Konten admin - Statistik dan Analytics
    markdown = utils.set_markdown()
    
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
                    
                    # Separator using Streamlit divider
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

                    # PDF Download button - moved to bottom
                    st.container(height=20, border=False)
                    col_pdf1, col_pdf2, col_pdf3 = st.columns([1, 1, 1])
                    with col_pdf2:
                        if st.button("📄 Download PDF", key="download_pdf", use_container_width=True):
                            try:
                                # Pass the selected date range to PDF generator
                                pdf_data = utils.generate_pdf_report(
                                    start_date=start_date, 
                                    end_date=end_date,
                                    positive=positive,
                                    neutral=neutral,
                                    negative=negative
                                )
                                if pdf_data:
                                    # Format date for filename
                                    start_str = filter_date[0].strftime('%Y%m%d')
                                    end_str = filter_date[1].strftime('%Y%m%d')
                                    filename = f"laporan_feedback_{start_str}_to_{end_str}.pdf"
                                    
                                    st.download_button(
                                        label="📥 Download Laporan PDF",
                                        data=pdf_data,
                                        file_name=filename,
                                        mime="application/pdf",
                                        key="download_pdf_btn",
                                        use_container_width=True
                                    )
                                    st.success("✅ PDF siap didownload!")
                                else:
                                    st.error("❌ Gagal membuat PDF")
                            except Exception as e:
                                st.error(f"❌ Error generating PDF: {e}")

            except Exception as e:
                st.error(f"❌ Error loading statistics: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Tampilan User Biasa - Form Feedback
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header tanpa kotak background
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
    
    with st.container():
        user_input = st.chat_input("💭 Ketik kritik dan saran Anda di sini...")
        if user_input:
            try:
                prediction = predict.predict(user_input).lower()
                data = {
                    "feedback": user_input,
                    "prediction": prediction,
                }
                success = repo.insert_data(data)
                if success:
                    show_notification("🎉 Terima kasih! Feedback Anda telah tersimpan.", "success")
                else:
                    show_notification("❌ Gagal menyimpan feedback. Silakan coba lagi.", "error")
            except Exception as e:
                show_notification("❌ Terjadi kesalahan. Silakan coba lagi.", "error")
    
    # Kontak saja yang tersisa
    st.markdown("""
---
### 📞 Kontak
Jika ada pertanyaan mendesak, hubungi:
- **📍 Alamat**: Jalan Tanjungtirto, Kalitirto, Berbah, Sleman, 55573
- **📞 Telepon**: (0274) 4986086
- **🌐 Website**: www.kalitirtosid.slemankab.go.id
- **✉️ Email**: kalitirtokalurahan@gmail.com
""")
    
    # Tombol admin di pojok kanan bawah
    if st.button("👨‍💼 Mode Admin", key="admin_toggle", help="Klik untuk masuk ke dashboard admin"):
        st.session_state.show_admin_login = True
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
