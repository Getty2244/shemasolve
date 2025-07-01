import streamlit as st

# Initiera session_state för inputfält EN gång i början
if "input_larar_id" not in st.session_state:
    st.session_state.input_larar_id = ""
if "input_amne" not in st.session_state:
    st.session_state.input_amne = "SO"
if "input_undervisningstid" not in st.session_state:
    st.session_state.input_undervisningstid = 0
if "input_larar_klasser" not in st.session_state:
    st.session_state.input_larar_klasser = []
if "input_arbetsdagar" not in st.session_state:
    st.session_state.input_arbetsdagar = ["Mon", "Tue", "Wed", "Thu", "Fri"]
if "input_onskemal" not in st.session_state:
    st.session_state.input_onskemal = ""

# Formulär
with st.form("larare_form"):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)", value=st.session_state.input_larar_id, key="input_larar_id")
    amne = st.selectbox("Ämne", options=["SO", "MA", "NO", "SV"], index=["SO", "MA", "NO", "SV"].index(st.session_state.input_amne), key="input_amne")
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10, value=st.session_state.input_undervisningstid, key="input_undervisningstid")
    larar_klasser = st.multiselect("Undervisar i klasser", options=["7a", "7b", "8a"], default=st.session_state.input_larar_klasser, key="input_larar_klasser")
    arbetsdagar = st.multiselect("Arbetsdagar", options=["Mon", "Tue", "Wed", "Thu", "Fri"], default=st.session_state.input_arbetsdagar, key="input_arbetsdagar")
    onskemal = st.text_area("Extra önskemål (valfritt)", value=st.session_state.input_onskemal, key="input_onskemal")

    submitted = st.form_submit_button("Lägg till lärare")

if submitted:
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

        # Återställ session_state INNAN rerun (för att undvika konflikt)
        st.session_state.input_larar_id = ""
        st.session_state.input_amne = "SO"
        st.session_state.input_undervisningstid = 0
        st.session_state.input_larar_klasser = []
        st.session_state.input_arbetsdagar = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        st.session_state.input_onskemal = ""

        st.experimental_rerun()  # Startar om appen så inputfält töms ordentligt
