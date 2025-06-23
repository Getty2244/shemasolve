import streamlit as st
import pandas as pd

# Lista med ämnen
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]

st.title("Färgval för ämnen")

# Låt användaren välja färg för varje ämne
farg_val = {}
for amne in amnen:
    farg_val[amne] = st.color_picker(f"Välj färg för {amne}", "#FFFFFF")

st.write("---")

# Exempeldata för schema, varje rad är en lektion med ämne
data = {
    "Tid": ["08:30-09:15", "09:20-10:05", "10:10-10:55", "11:00-11:45"],
    "Ämne": ["SO", "MA", "SO", "MA"],
    "Klass": ["7a", "8a", "9a", "9a"]
}

df = pd.DataFrame(data)

# Funktion för att färgsätta ämnesceller med vald färg
def color_amne(val):
    color = farg_val.get(val, "#FFFFFF")
    return f"background-color: {color};"

# Visa tabellen med färgerade ämnesceller
st.write("### Schema med färgade ämnen")
st.dataframe(df.style.applymap(color_amne, subset=["Ämne"]))
