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
        # Coba beberapa lokasi file
        possible_paths = ['model.pkl', './model.pkl', 'models/model.pkl']
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"Loading model from: {path}")
                return joblib.load(path)
        
        print("File model.pkl tidak ditemukan di semua lokasi yang dicoba")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

@st.cache_resource 
def load_vectorizer():
    try:
        # Coba beberapa lokasi file
        possible_paths = ['vectorizer.pkl', './vectorizer.pkl', 'models/vectorizer.pkl']
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"Loading vectorizer from: {path}")
                return joblib.load(path)
        
        print("File vectorizer.pkl tidak ditemukan di semua lokasi yang dicoba")
        return None
    except Exception as e:
        print(f"Error loading vectorizer: {e}")
        return None
