import streamlit as st
import pandas as pd
import datetime
from streamlit.runtime.scriptrunner.script_runner import RerunException, RerunData

def rerun():
    raise RerunException(RerunData())

# ÄMNEN OCH KLASSER
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

st.title("AI-schemaplanerare för skolan")

# Initiera session_state för input-fält OM de inte finns
if "input_larar_id" not in st.session_state:
    st.session_state.input_larar_id = ""
if "input_amne" not in st.session_state:
    st.session_state.input_amne = amnen[0]
if "input_undervisningstid" not in st.session_state:
    st.session_state.input_undervisningstid = 0
if "input_larar_klasser" not in st.session_state:
    st.session_state.input_larar_klasser = []
if "input_arbetsdagar" not in st.session_state:
    st.session_state.input_arbetsdagar = dagar_val.copy()
if "input_onskemal" not in st.session_state:
    st.session_state.input_onskemal = ""

# Färgval
if "temp_farg_val" not in st.session_state:
    st.session_state.temp_farg_val = {amne: "#FFFFFF" for amne in amnen}
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}

st.header("1. Färgval för ämnen")
for amne in amnen:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state.temp_farg_val[amne] = st.color_picker(
            f"{amne}", st.session_state.temp_farg_val[amne], key=f"farg_{amne}"
        )
    with col2:
        st.write(st.session_state.temp_farg_val[amne])

if st.button("Spara färger"):
    st.session_state.farg_val = st.session_state.temp_farg_val.copy()
    st.success("Färger sparade!")

# Funktion för att rensa lärarformulär inputs
def reset_larar_inputs():
    st.session_state.input_larar_id = ""
    st.session_state.input_amne = amnen[0]
    st.session_state.input_undervisningstid = 0
    st.session_state.input_larar_klasser = []
    st.session_state.input_arbetsdagar = dagar_val.copy()
    st.session_state.input_onskemal = ""

# Lägg till lärare
st.header("2. Lägg till lärare")

with st.form("larare_form"):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)", key="input_larar_id")
    amne = st.selectbox("Ämne", options=amnen, key="input_amne")
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10, key="input_undervisningstid")
    larar_klasser = st.multiselect("Undervisar i klasser", options=klasser, key="input_larar_klasser")
    arbetsdagar = st.multiselect("Arbetsdagar", options=dagar_val, default=dagar_val, key="input_arbetsdagar")
    onskemal = st.text_area("Extra önskemål (valfritt)", key="input_onskemal")

    with st.expander("ℹ️ Exempel på vanliga önskemål"):
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
    if (st.session_state.input_larar_id.strip() != "" and
        st.session_state.input_amne and
        st.session_state.input_larar_klasser and
        st.session_state.input_arbetsdagar and
        st.session_state.input_undervisningstid > 0):

        ny_larare = {
            "id": st.session_state.input_larar_id.strip(),
            "ämne": st.session_state.input_amne,
            "klasser": st.session_state.input_larar_klasser,
            "dagar": st.session_state.input_arbetsdagar,
            "minuter_per_vecka": st.session_state.input_undervisningstid,
            "önskemål": st.session_state.input_onskemal or ""
        }
        if "larare_data" not in st.session_state:
            st.session_state.larare_data = []
        st.session_state.larare_data.append(ny_larare)
        st.success(f"Lärare {ny_larare['id']} tillagd!")

        reset_larar_inputs()
        rerun()

# Visa och redigera lärare
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
                    "id": nytt_id.strip(),
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
