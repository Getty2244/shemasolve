import streamlit as st
import pandas as pd
import datetime
from streamlit.runtime.scriptrunner.script_runner import RerunException, RerunData

def rerun():
    raise RerunException(RerunData())

# === ÄMNEN OCH KLASSER ===
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Initiera session_state variabler för formulärinputs om de saknas
defaults = {
    "input_larar_id": "",
    "input_amne": amnen[0],
    "input_undervisningstid": 0,
    "input_larar_klasser": [],
    "input_arbetsdagar": dagar_val,
    "input_onskemal": "",
    "input_sal_namn": "",
    "input_sal_klass": klasser[0],
    "input_sal_amne": amnen[0],
    "input_starttid": "08:30",
    "input_lunchmin": 40,
    "input_lek_min": 40,
    "input_lek_max": 60,
    "input_rast_min": 5,
    "input_rast_max": 15,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

st.title("AI-schemaplanerare för skolan")

# === 1. FÄRGVAL ===
if "temp_farg_val" not in st.session_state:
    st.session_state.temp_farg_val = {amne: "#FFFFFF" for amne in amnen}

if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}

st.header("1. Färgval för ämnen")
for amne in amnen:
    col1, col2 = st.columns([3,1])
    with col1:
        st.session_state.temp_farg_val[amne] = st.color_picker(
            f"{amne}",
            st.session_state.temp_farg_val[amne],
            key=f"farg_{amne}"
        )
    with col2:
        st.write(st.session_state.temp_farg_val[amne])

if st.button("Spara färger"):
    st.session_state.farg_val = st.session_state.temp_farg_val.copy()
    st.success("Färger sparade!")

# === 2. LÄGG TILL LÄRARE ===
st.header("2. Lägg till lärare")

with st.form("larare_form"):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)", key="input_larar_id")
    amne = st.selectbox("Ämne", options=amnen, key="input_amne")
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10, key="input_undervisningstid")
    larar_klasser = st.multiselect("Undervisar i klasser", options=klasser, key="input_larar_klasser")
    arbetsdagar = st.multiselect("Arbetsdagar", options=dagar_val, default=dagar_val, key="input_arbetsdagar")
    onskemal = st.text_area("Extra önskemål (valfritt)", key="input_onskemal")

    with st.expander("ℹ️ Exempel på önskemål"):
        st.markdown("""
        - Undvik SO på måndagar  
        - Idrott helst efter lunch  
        - NO bör ej ligga första lektionen  
        - Engelska i följd om möjligt  
        - Fredagar helst undervisningsfri  
        - Matte inte alla dagar i rad  
        - Slöjd ska ej vara efter idrott  
        - Mentorstid varje tisdag 10:00
        """)

    skicka = st.form_submit_button("Lägg till lärare")

    if skicka:
        if larar_id and amne and larar_klasser and arbetsdagar and undervisningstid > 0:
            ny_larare = {
                "id": larar_id,
                "ämne": amne,
                "klasser": larar_klasser,
                "dagar": arbetsdagar,
                "minuter_per_vecka": undervisningstid,
                "önskemål": onskemal or ""
            }
            if "larare_data" not in st.session_state:
                st.session_state.larare_data = []
            st.session_state.larare_data.append(ny_larare)
            st.success(f"Lärare {larar_id} tillagd!")

            # Rensa inputfält - viktigt att detta sker här, INUTI if skicka:
            st.session_state.input_larar_id = ""
            st.session_state.input_amne = amnen[0]
            st.session_state.input_undervisningstid = 0
            st.session_state.input_larar_klasser = []
            st.session_state.input_arbetsdagar = dagar_val
            st.session_state.input_onskemal = ""

            rerun()

# Visa/redigera lärare
st.subheader("📋 Inlagda lärare")
if "larare_data" not in st.session_state or not st.session_state.larare_data:
    st.info("Inga lärare inlagda ännu.")
else:
    if "redigera_larare_index" not in st.session_state:
        st.session_state.redigera_larare_index = None

    for i, larare in enumerate(st.session_state.larare_data):
        if st.session_state.redigera_larare_index == i:
            st.write(f"✏️ Redigerar lärare **{larare['id']}**")
            nytt_id = st.text_input("Lärar-ID", value=larare["id"], key=f"edit_id_{i}")
            nytt_amne = st.selectbox("Ämne", options=amnen, index=amnen.index(larare["ämne"]), key=f"edit_amne_{i}")
            nya_klasser = st.multiselect("Klasser", options=klasser, default=larare["klasser"], key=f"edit_klass_{i}")
            nya_dagar = st.multiselect("Arbetsdagar", options=dagar_val, default=larare["dagar"], key=f"edit_dagar_{i}")
            nya_minuter = st.number_input("Undervisningsminuter/vecka", value=larare["minuter_per_vecka"], min_value=0, step=10, key=f"edit_min_{i}")
            nya_onskemal = st.text_area("Extra önskemål", value=larare.get("önskemål", ""), key=f"edit_onskemal_{i}")

            if st.button("💾 Spara", key=f"spara_larare_{i}"):
                st.session_state.larare_data[i] = {
                    "id": nytt_id,
                    "ämne": nytt_amne,
                    "klasser": nya_klasser,
                    "dagar": nya_dagar,
                    "minuter_per_vecka": nya_minuter,
                    "önskemål": nya_onskemal
                }
                st.session_state.redigera_larare_index = None
                rerun()

            if st.button("❌ Ta bort", key=f"ta_bort_larare_{i}"):
                st.session_state.larare_data.pop(i)
                st.session_state.redigera_larare_index = None
                rerun()

            if st.button("Avbryt", key=f"avbryt_larare_{i}"):
                st.session_state.redigera_larare_index = None
                rerun()
        else:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"""
                - **{larare['id']}** ({larare['ämne']})  
                  Klasser: {', '.join(larare['klasser'])}  
                  Dagar: {', '.join(larare['dagar'])}  
                  Minuter/vecka: {larare['minuter_per_vecka']}  
                  Önskemål: _{larare.get('önskemål', '')}_  
                """)
            with col2:
                if st.button("✏️ Redigera", key=f"redigera_larare_{i}"):
                    st.session_state.redigera_larare_index = i
                    rerun()

# Du kan bygga vidare på salar, inställningar och schemagenerering på samma sätt,
# med samma princip: ändringar av session_state som rensar inputs görs inuti callback/submit-block!

# Om du vill kan jag skicka hela koden för hela appen med samma struktur, säg bara till!
