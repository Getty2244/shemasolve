import streamlit as st
import pandas as pd

# === ÄMNEN OCH KLASSER ===
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

st.title("AI-schemaplanerare för skolan")

# === 1. FÄRGVAL ===
st.header("1. Färgval för ämnen")

if "temp_farg_val" not in st.session_state:
    st.session_state.temp_farg_val = {amne: "#FFFFFF" for amne in amnen}

if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}

for amne in amnen:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state.temp_farg_val[amne] = st.color_picker(f"{amne}", st.session_state.temp_farg_val[amne], key=amne)
    with col2:
        st.write(st.session_state.temp_farg_val[amne])

if st.button("Spara färger"):
    st.session_state.farg_val = st.session_state.temp_farg_val.copy()
    st.success("Färger sparade!")

# === 2. LÄGG TILL LÄRARE ===
st.header("2. Lägg till lärare")

with st.form("lärare_form"):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)")
    amne = st.selectbox("Ämne", options=amnen)
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10)
    larar_klasser = st.multiselect("Undervisar i klasser", options=klasser)
    arbetsdagar = st.multiselect("Arbetsdagar", options=dagar_val, default=dagar_val)
    skicka = st.form_submit_button("Lägg till lärare")

if "larare_data" not in st.session_state:
    st.session_state.larare_data = []

if skicka and larar_id and amne and larar_klasser and arbetsdagar and undervisningstid > 0:
    ny_larare = {
        "id": larar_id,
        "ämne": amne,
        "klasser": larar_klasser,
        "dagar": arbetsdagar,
        "minuter_per_vecka": undervisningstid
    }
    st.session_state.larare_data.append(ny_larare)
    st.success(f"Lärare {larar_id} tillagd!")

if st.session_state.larare_data:
    st.write("### Inlagda lärare:")
    st.table(st.session_state.larare_data)

# === 3. LÄGG TILL SAL ===
st.header("3. Lägg till sal")

with st.form("sal_form"):
    sal_namn = st.text_input("Salnamn (t.ex. A101, NO-labb)")
    sal_typ = st.selectbox("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"])

    sal_klass = None
    sal_amne = None

    if sal_typ == "Hemklassrum":
        sal_klass = st.selectbox("Tilldelad klass", options=klasser, key="klass_val")
    else:
        sal_amne = st.selectbox("Tilldelat ämne", options=amnen, key="amne_val")

    sal_submit = st.form_submit_button("Lägg till sal")

if "sal_data" not in st.session_state:
    st.session_state.sal_data = []

if sal_submit and sal_namn:
    ny_sal = {
        "sal": sal_namn,
        "typ": sal_typ,
        "klass": sal_klass if sal_typ == "Hemklassrum" else None,
        "ämne": sal_amne if sal_typ == "Ämnesklassrum" else None
    }
    st.session_state.sal_data.append(ny_sal)
    st.success(f"Sal {sal_namn} tillagd!")

if st.session_state.sal_data:
    st.write("### Inlagda salar:")
    st.table(st.session_state.sal_data)

# === 4. EXEMPELSCHEMA ===
st.header("4. Exempelschema med färgade ämnen")

data = {
    "Tid": ["08:30-09:15", "09:20-10:05", "10:10-10:55", "11:00-11:45"],
    "Ämne": ["SO", "MA", "SO", "MA"],
    "Klass": ["7a", "8a", "9a", "9a"]
}
df = pd.DataFrame(data)

def color_amne(val):
    return f"background-color: {st.session_state.farg_val.get(val, '#FFFFFF')};"

styled_df = df.style.applymap(color_amne, subset=["Ämne"])
st.write(styled_df.to_html(), unsafe_allow_html=True)
