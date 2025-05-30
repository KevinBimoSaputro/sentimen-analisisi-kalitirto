import connection as conn
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

try:
    db = conn.load_database()
except:
    # Jika database tidak terhubung, gunakan dummy data
    db = None

def insert_data(data):
    if db:
        db.insert(data).execute()
        get_count_by_prediction.clear()
        get_feedback_history.clear()
    else:
        # Simpan ke session state sebagai fallback
        if 'feedback_data' not in st.session_state:
            st.session_state.feedback_data = []
        
        # Tambahkan timestamp
        data['created_at'] = datetime.now().isoformat()
        st.session_state.feedback_data.append(data)

@st.cache_data
def get_count_by_prediction(prediction, start_date, end_date):
    if db:
        data = db.select("*", count="exact") \
            .eq("prediction", prediction) \
            .gte("created_at", start_date) \
            .lte("created_at", end_date) \
            .limit(1) \
            .execute()
        return data.count
    else:
        # Gunakan data dari session state
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
        data = db.select("feedback, prediction, created_at") \
            .gte("created_at", start_date) \
            .lte("created_at", end_date) \
            .order("created_at", desc=False) \
            .execute()
        return data.data
    else:
        # Gunakan data dari session state
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
