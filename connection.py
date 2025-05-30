import streamlit as st
import joblib
import os

@st.cache_resource 
def load_database():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        from supabase import create_client
        client = create_client(url, key)
        table = st.secrets["supabase"]["table"]
        return client.table(table)
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@st.cache_resource 
def load_model():
    try:
        if os.path.exists('model.pkl'):
            return joblib.load('model.pkl')
        else:
            print("File model.pkl tidak ditemukan")
            return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

@st.cache_resource 
def load_vectorizer():
    try:
        if os.path.exists('vectorizer.pkl'):
            return joblib.load('vectorizer.pkl')
        else:
            print("File vectorizer.pkl tidak ditemukan")
            return None
    except Exception as e:
        print(f"Error loading vectorizer: {e}")
        return None
