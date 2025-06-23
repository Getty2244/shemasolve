import streamlit as st
import pandas as pd

# Exempeldata (din schemalista)
data = [
    ["Mon", "08:30-09:15", "7a", "bgk1", "SO"],
    ["Tue", "08:30-09:15", "7a", "bgk1", "SO"],
    ["Mon", "09:20-10:05", "8a", "bgk1", "SO"],
    ["Tue", "09:20-10:05", "8a", "bgk1", "SO"],
    ["Mon", "10:10-10:55", "9a", "bgk1", "SO"],
    ["Tue", "10:10-10:55", "9a", "bgk1", "SO"],
    ["Mon", "09:20-10:05", "7a", "bgk2", "MA"],
    ["Tue", "09:20-10:05", "7a", "bgk2", "MA"],
    ["Mon", "08:30-09:15", "8a", "bgk2", "MA"],
    ["Tue", "08:30-09:15", "8a", "bgk2", "MA"],
    ["Mon", "11:00-11:45", "9a", "bgk2", "MA"],
    ["Tue", "11:00-11:45", "9a", "bgk2", "MA"],
]

# Skapa DataFrame
df = pd.DataFrame(data, columns=["Dag", "Tid", "Klass", "Lärare", "Ämne"])

# Visa i Streamlit som tabell
st.write("### Schema")
st.dataframe(df)
