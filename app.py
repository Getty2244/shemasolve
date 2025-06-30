import streamlit as st

# --- Grunddata ---
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# --- Init session_state-variabler ---
if "temp_farg_val" not in st.session_state:
    st.session_state.temp_farg_val = {amne: "#FFFFFF" for amne in amnen}
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}
if "larare_data" not in st.session_state:
    st.session_state.larare_data = []
if "redigera_larare_index" not in st.session_state:
    st.session_state.redigera_larare_index = None

st.title("AI-schemaplanerare för skolan")

# --- 1. Färgval ---
st.header("1. Färgval för ämnen")
for amne in amnen:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state.temp_farg_val[amne] = st.color_picker(amne, st.session_state.temp_farg_val[amne], key=f"farg_{amne}")
    with col2:
        st.write(st.session_state.temp_farg_val[amne])

if st.button("Spara färger"):
    st.session_state.farg_val = st.session_state.temp_farg_val.copy()
    st.success("Färger sparade!")

# --- 2. Lägg till lärare ---
st.header("2. Lägg till lärare")

with st.form("larare_form", clear_on_submit=True):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)")
    amne = st.selectbox("Ämne", amnen)
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10)
    larar_klasser = st.multiselect("Undervisar i klasser", klasser)
    arbetsdagar = st.multiselect("Arbetsdagar", dagar_val, default=dagar_val)
    onskemal = st.text_area("Extra önskemål (valfritt)")

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
        st.session_state.larare_data.append(ny_larare)
        st.success(f"Lärare {larar_id} tillagd!")

# --- 3. Visa och redigera lärare ---
st.subheader("📋 Inlagda lärare")

if st.session_state.larare_data:
    for i, larare in enumerate(st.session_state.larare_data):
        if st.session_state.redigera_larare_index == i:
            # Redigeringsformulär för vald lärare
            nytt_id = st.text_input("Lärar-ID", value=larare["id"], key=f"edit_id_{i}")
            nytt_amne = st.selectbox("Ämne", amnen, index=amnen.index(larare["ämne"]), key=f"edit_amne_{i}")
            nya_klasser = st.multiselect("Klasser", klasser, default=larare["klasser"], key=f"edit_klass_{i}")
            nya_dagar = st.multiselect("Arbetsdagar", dagar_val, default=larare["dagar"], key=f"edit_dagar_{i}")
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
                st.experimental_rerun()

            if st.button("❌ Ta bort", key=f"ta_bort_larare_{i}"):
                st.session_state.larare_data.pop(i)
                st.session_state.redigera_larare_index = None
                st.experimental_rerun()

            if st.button("Avbryt", key=f"avbryt_larare_{i}"):
                st.session_state.redigera_larare_index = None
                st.experimental_rerun()

        else:
            # Visa lärarinfo och redigeraknapp
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"**{larare['id']}** ({larare['ämne']}) — Klasser: {', '.join(larare['klasser'])} — Dagar: {', '.join(larare['dagar'])}")
            with col2:
                if st.button("✏️ Redigera", key=f"redigera_larare_{i}"):
                    st.session_state.redigera_larare_index = i
                    st.experimental_rerun()
else:
    st.info("Inga lärare inlagda ännu.")
