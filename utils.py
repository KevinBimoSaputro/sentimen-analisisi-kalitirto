import pandas as pd
import streamlit as st
import pytz
import plotly.express as px

def process_feedback_history(data):
    df = pd.DataFrame(data)

    try:
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        df['date'] = pd.to_datetime(df['created_at']).dt.tz_convert(jakarta_tz).dt.strftime('%Y-%m-%d %H:%M:%S')
        df.drop(columns=['created_at'], inplace=True)
    except:
        # Jika tidak ada kolom created_at atau error lainnya
        if 'date' not in df.columns:
            df['date'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

    if 'no' not in df.columns:
        df.insert(0, 'no', range(1, len(df) + 1))
    
    return df

def set_markdown():
    return st.markdown("""
    <style>
        .stMetricValue-positif {
            background-color: green;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricValue-negatif {
            background-color: red;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricValue-netral {
            background-color: yellow;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricLabel {
            font-size: 16px;
            font-weight: bold;
        }
        
        /* Tambahan styling untuk UI yang lebih baik */
        .stButton>button {
            background-color: #4DA6FF;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #3A7FBF;
        }
        
        /* Styling untuk header */
        h1, h2, h3 {
            color: #1E3A8A;
        }
        
        /* Styling untuk container */
        .stContainer {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

def create_chart(positive, neutral, negative):
    labels = ['Positif', 'Netral', 'Negatif']
    values = [positive, neutral, negative]
    
    # Hitung persentase
    total = sum(values)
    percentages = [round(val/total*100, 1) for val in values]
    
    # Buat label dengan persentase
    custom_labels = [f"{labels[i]}\n{percentages[i]}%" for i in range(len(labels))]

    fig = px.pie(
        names=labels,
        values=values,
        color=labels,
        color_discrete_map={
            'Positif': 'green',
            'Netral': '#FFD700',
            'Negatif': 'red'
        }
    )

    fig.update_traces(
        textinfo='label+percent',
        insidetextorientation='auto',
        hoverinfo='label+value', 
        textfont_size=14,
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    
    fig.update_layout(
        title="Distribusi Sentimen Feedback",
        legend_title="Sentimen",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
