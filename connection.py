import streamlit as st
import joblib
from supabase import create_client

@st.cache_resource 
def load_database():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    client = create_client(url, key)
    table = st.secrets["supabase"]["table"]
    return client.table(table)

@st.cache_resource 
def load_model():
    return joblib.load('model.pkl')

@st.cache_resource 
def load_vectorizer():
    return joblib.load('vectorizer.pkl')
