import streamlit as st
import pandas as pd

amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]

st.title("Färgval för ämnen")

farg_val = {}
for amne in amnen:
    farg_val[amne] = st.color_picker(f"Välj färg för {amne}", "#FFFFFF")

data = {
    "Tid": ["08:30-09:15", "09:20-10:05", "10:10-10:55", "11:00-11:45"],
    "Ämne": ["SO", "MA", "SO", "MA"],
    "Klass": ["7a", "8a", "9a", "9a"]
}

df = pd.DataFrame(data)

def color_amne(val):
    color = farg_val.get(val, "#FFFFFF")
    return f"background-color: {color};"

st.write("### Schema med färgade ämnen")

# Här konverterar vi till HTML och visar med unsafe_allow_html=True
styled_df = df.style.applymap(color_amne, subset=["Ämne"]).render()
st.markdown(styled_df, unsafe_allow_html=True)
