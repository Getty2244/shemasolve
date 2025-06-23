import streamlit as st
import pandas as pd

amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]

st.title("Färgval för ämnen")

# Initiera färgval i session_state om det inte finns
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}

# Visa color pickers och uppdatera session_state
for amne in amnen:
    st.session_state.farg_val[amne] = st.color_picker(f"Välj färg för {amne}", st.session_state.farg_val[amne])

data = {
    "Tid": ["08:30-09:15", "09:20-10:05", "10:10-10:55", "11:00-11:45"],
    "Ämne": ["SO", "MA", "SO", "MA"],
    "Klass": ["7a", "8a", "9a", "9a"]
}

df = pd.DataFrame(data)

def color_amne(val):
    return f"background-color: {st.session_state.farg_val.get(val, '#FFFFFF')};"

st.write("### Schema med färgade ämnen")

styled_df = df.style.applymap(color_amne, subset=["Ämne"])

# Visa som HTML, unsafe_allow_html=True krävs för färger
st.write(styled_df.to_html(), unsafe_allow_html=True)
