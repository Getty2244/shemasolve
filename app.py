import streamlit as st
import pandas as pd
import datetime

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
        st.session_state.temp_farg_val[amne] = st.color_picker(
            f"{amne}",
            st.session_state.temp_farg_val[amne],
            key=f"farg_{amne}"
        )
    with col2:
        st.write(st.session_state.temp_farg_val[amne])

if st.button("Spara färger", key="spara_farger_knapp"):
    st.session_state.farg_val = st.session_state.temp_farg_val.copy()
    st.success("Färger sparade!")

# === 2. LÄGG TILL LÄRARE ===
st.header("2. Lägg till lärare")

with st.form("larare_form"):
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

# === 3. INSTÄLLNINGAR FÖR SKOLDAGEN ===
st.header("3. Inställningar för skoldagen")

with st.form("form_skoldag_tider"):
    starttid_str = st.text_input("Skoldagens starttid (HH:MM)", value="08:30")
    sluttider = {}
    for dag in dagar_val:
        sluttider[dag] = st.text_input(f"Sluttid för {dag} (HH:MM)", value="15:00")
    lunchmin = st.number_input("Lunchrastens längd (min)", min_value=20, max_value=60, value=40)
    lek_min = st.number_input("Minsta lektionslängd (min)", min_value=30, max_value=60, value=40)
    lek_max = st.number_input("Max lektionslängd (min)", min_value=60, max_value=90, value=60)
    rast_min = st.number_input("Minsta rast (min)", min_value=5, max_value=15, value=5)
    rast_max = st.number_input("Största rast (min)", min_value=10, max_value=30, value=15)

    spara_tid = st.form_submit_button("Spara inställningar")

if spara_tid:
    try:
        starttid = datetime.datetime.strptime(starttid_str, "%H:%M").time()
        sluttider_obj = {dag: datetime.datetime.strptime(tid, "%H:%M").time() for dag, tid in sluttider.items()}
        st.session_state.daginst = {
            "starttid": starttid,
            "sluttider": sluttider_obj,
            "lunch": lunchmin,
            "lek_min": lek_min,
            "lek_max": lek_max,
            "rast_min": rast_min,
            "rast_max": rast_max
        }
        st.success("Skoldagens inställningar sparade!")
    except ValueError:
        st.error("Felaktigt tidsformat. Använd HH:MM")
