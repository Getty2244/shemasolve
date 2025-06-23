import streamlit as st
import pandas as pd

# === Färgval för ämnen ===
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]

st.title("AI-schemaplanerare för skolan")

st.header("1. Färgval för ämnen")

# Initiera färger i session_state
if "temp_farg_val" not in st.session_state:
    st.session_state.temp_farg_val = {amne: "#FFFFFF" for amne in amnen}

if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}

st.write("Välj färg för varje ämne och klicka på 'Spara färger'.")

for amne in amnen:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state.temp_farg_val[amne] = st.color_picker(f"{amne}", st.session_state.temp_farg_val[amne], key=amne)
    with col2:
        st.write(st.session_state.temp_farg_val[amne])

if st.button("Spara färger"):
    st.session_state.farg_val = st.session_state.temp_farg_val.copy()
    st.success("Färger sparade!")

# === Lägg till lärare ===
st.header("2. Lägg till lärare")

with st.form("lärare_form"):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)")
    amne = st.selectbox("Ämne", options=amnen)
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10)
    klasser = st.multiselect("Undervisar i klasser", options=["7a", "7b", "8a", "8b", "9a", "9b"])
    dagar = st.multiselect("Arbetsdagar", options=["Mon", "Tue", "Wed", "Thu", "Fri"])
    skicka = st.form_submit_button("Lägg till lärare")

if "larare_data" not in st.session_state:
    st.session_state.larare_data = []

if skicka and larar_id and amne and klasser and dagar and undervisningstid > 0:
    ny_larare = {
        "id": larar_id,
        "ämne": amne,
        "klasser": klasser,
        "dagar": dagar,
        "minuter_per_vecka": undervisningstid
    }
    st.session_state.larare_data.append(ny_larare)
    st.success(f"Lärare {larar_id} tillagd!")

# Visa inlagda lärare
if st.session_state.larare_data:
    st.write("### Inlagda lärare:")
    st.table(st.session_state.larare_data)

# === Testschema att visa med färger ===
st.header("3. Exempelschema med färgade ämnen")

data = {
    "Tid": ["08:30-09:15", "09:20-10:05", "10:10-10:55", "11:00-11:45"],
    "Ämne": ["SO", "MA", "SO", "MA"],
    "Klass": ["7a", "8a", "9a", "9a"]
}
df = pd.DataFrame(data)

# Färglägg ämnesceller
def color_amne(val):
    return f"background-color: {st.session_state.farg_val.get(val, '#FFFFFF')};"

styled_df = df.style.applymap(color_amne, subset=["Ämne"])
st.write(styled_df.to_html(), unsafe_allow_html=True)
