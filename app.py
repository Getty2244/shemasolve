import streamlit as st

# === ÄMNEN OCH KLASSER ===
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

st.title("AI-schemaplanerare för skolan")

# === 1. FÄRGVAL ===
if "temp_farg_val" not in st.session_state:
    st.session_state.temp_farg_val = {amne: "#FFFFFF" for amne in amnen}

if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}

st.header("1. Färgval för ämnen")

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

# Initiera session_state-variabler en gång tidigt
if "input_larar_id" not in st.session_state:
    st.session_state.input_larar_id = ""
if "input_amne" not in st.session_state:
    st.session_state.input_amne = amnen[0]
if "input_undervisningstid" not in st.session_state:
    st.session_state.input_undervisningstid = 0
if "input_larar_klasser" not in st.session_state:
    st.session_state.input_larar_klasser = []
if "input_arbetsdagar" not in st.session_state:
    st.session_state.input_arbetsdagar = dagar_val
if "input_onskemal" not in st.session_state:
    st.session_state.input_onskemal = ""

with st.form("larare_form"):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)", key="input_larar_id")
    amne = st.selectbox("Ämne", options=amnen, index=amnen.index(st.session_state.input_amne), key="input_amne")
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10, key="input_undervisningstid")
    larar_klasser = st.multiselect("Undervisar i klasser", options=klasser, default=st.session_state.input_larar_klasser, key="input_larar_klasser")
    arbetsdagar = st.multiselect("Arbetsdagar", options=dagar_val, default=st.session_state.input_arbetsdagar, key="input_arbetsdagar")
    onskemal = st.text_area("Extra önskemål (valfritt)", value=st.session_state.input_onskemal, key="input_onskemal")

    with st.expander("ℹ️ Se exempel på vanliga önskemål"):
        st.markdown("""
        **Exempel på extra önskemål:**
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

        # Rensa inputfält (förbered nästa inmatning)
        st.session_state.input_larar_id = ""
        st.session_state.input_amne = amnen[0]
        st.session_state.input_undervisningstid = 0
        st.session_state.input_larar_klasser = []
        st.session_state.input_arbetsdagar = dagar_val
        st.session_state.input_onskemal = ""

# === Visa inlagda lärare ===
st.subheader("📋 Inlagda lärare")
if "larare_data" not in st.session_state or not st.session_state.larare_data:
    st.info("Inga lärare inlagda ännu.")
else:
    for larare in st.session_state.larare_data:
        st.markdown(f"""
        - **{larare['id']}** ({larare['ämne']})  
          Klasser: {', '.join(larare['klasser'])}  
          Dagar: {', '.join(larare['dagar'])}  
          Minuter/vecka: {larare['minuter_per_vecka']}  
          Önskemål: _{larare.get('önskemål', '')}_
        """)

