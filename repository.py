import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Inisialisasi database
try:
    import connection as conn
    db = conn.load_database()
except:
    db = None

def insert_data(data):
    if db:
        try:
            db.insert(data).execute()
            get_count_by_prediction.clear()
            get_feedback_history.clear()
            return True
        except Exception as e:
            print(f"Database insert error: {e}")
            # Fallback ke session state
            save_to_session_state(data)
            return True
    else:
        # Simpan ke session state sebagai fallback
        save_to_session_state(data)
        return True

def save_to_session_state(data):
    """Simpan data ke session state sebagai fallback"""
    if 'feedback_data' not in st.session_state:
        st.session_state.feedback_data = []
    
    # Tambahkan timestamp
    data['created_at'] = datetime.now().isoformat()
    st.session_state.feedback_data.append(data)

@st.cache_data
def get_count_by_prediction(prediction, start_date, end_date):
    if db:
        try:
            data = db.select("*", count="exact") \
                .eq("prediction", prediction) \
                .gte("created_at", start_date) \
                .lte("created_at", end_date) \
                .limit(1) \
                .execute()
            return data.count
        except Exception as e:
            print(f"Database query error: {e}")
            return get_count_from_session_state(prediction, start_date, end_date)
    else:
        return get_count_from_session_state(prediction, start_date, end_date)

def get_count_from_session_state(prediction, start_date, end_date):
    """Hitung data dari session state"""
    if 'feedback_data' not in st.session_state:
        return 0
    
    count = 0
    for item in st.session_state.feedback_data:
        if item['prediction'] == prediction and start_date <= item['created_at'] <= end_date:
            count += 1
    return count

@st.cache_data
def get_feedback_history(start_date, end_date):
    if db:
        try:
            data = db.select("feedback, prediction, created_at") \
                .gte("created_at", start_date) \
                .lte("created_at", end_date) \
                .order("created_at", desc=False) \
                .execute()
            return data.data
        except Exception as e:
            print(f"Database query error: {e}")
            return get_history_from_session_state(start_date, end_date)
    else:
        return get_history_from_session_state(start_date, end_date)

def get_history_from_session_state(start_date, end_date):
    """Ambil history dari session state"""
    if 'feedback_data' not in st.session_state:
        # Data dummy untuk demo
        dummy_data = [
            {"feedback": "pelayanan sangat baik", "prediction": "positif", "created_at": (datetime.now() - timedelta(days=1)).isoformat()},
            {"feedback": "antriannya terlalu lama", "prediction": "negatif", "created_at": (datetime.now() - timedelta(days=2)).isoformat()},
            {"feedback": "petugas cukup membantu", "prediction": "netral", "created_at": (datetime.now() - timedelta(days=3)).isoformat()}
        ]
        return dummy_data
    
    # Filter berdasarkan tanggal
    filtered_data = []
    for item in st.session_state.feedback_data:
        if start_date <= item['created_at'] <= end_date:
            filtered_data.append(item)
    
    return filtered_data

def get_connection_status():
    """Check database connection status"""
    try:
        if db:
            # Try a simple query to test connection
            test_query = db.select("*").limit(1).execute()
            return True
        return False
    except:
        return False
