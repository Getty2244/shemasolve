import streamlit as st

amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Init färger
if "temp_farg_val" not in st.session_state:
    st.session_state.temp_farg_val = {amne: "#FFFFFF" for amne in amnen}
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}

# Init input värden (om ej finns)
for key, default in {
    "input_larar_id": "",
    "input_amne": amnen[0],
    "input_undervisningstid": 0,
    "input_larar_klasser": [],
    "input_arbetsdagar": dagar_val,
    "input_onskemal": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.title("AI-schemaplanerare för skolan")

# Färgval
st.header("1. Färgval för ämnen")
for amne in amnen:
    col1, col2 = st.columns([3,1])
    with col1:
        st.session_state.temp_farg_val[amne] = st.color_picker(amne, st.session_state.temp_farg_val[amne], key=f"farg_{amne}")
    with col2:
        st.write(st.session_state.temp_farg_val[amne])

if st.button("Spara färger"):
    st.session_state.farg_val = st.session_state.temp_farg_val.copy()
    st.success("Färger sparade!")

# Lägg till lärare
st.header("2. Lägg till lärare")
with st.form("larare_form"):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)", key="input_larar_id")
    amne = st.selectbox("Ämne", amnen, key="input_amne")
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10, key="input_undervisningstid")
    larar_klasser = st.multiselect("Undervisar i klasser", klasser, key="input_larar_klasser")
    arbetsdagar = st.multiselect("Arbetsdagar", dagar_val, default=dagar_val, key="input_arbetsdagar")
    onskemal = st.text_area("Extra önskemål (valfritt)", key="input_onskemal")

    submitted = st.form_submit_button("Lägg till lärare")

if submitted:
    if not larar_id:
        st.error("Ange Lärar-ID.")
    elif undervisningstid <= 0:
        st.error("Undervisningsminuter måste vara större än 0.")
    elif not larar_klasser:
        st.error("Välj minst en klass.")
    elif not arbetsdagar:
        st.error("Välj minst en arbetsdag.")
    else:
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

        # Rensa input *inne i submit-blocket*
        st.session_state.input_larar_id = ""
        st.session_state.input_amne = amnen[0]
        st.session_state.input_undervisningstid = 0
        st.session_state.input_larar_klasser = []
        st.session_state.input_arbetsdagar = dagar_val
        st.session_state.input_onskemal = ""

        st.experimental_rerun()

# Visa inlagda lärare
st.subheader("Inlagda lärare")
if "larare_data" in st.session_state and st.session_state.larare_data:
    for larare in st.session_state.larare_data:
        st.write(f"- **{larare['id']}** ({larare['ämne']}) — Klasser: {', '.join(larare['klasser'])} — Dagar: {', '.join(larare['dagar'])}")
else:
    st.info("Inga lärare inlagda ännu.")
