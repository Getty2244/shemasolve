import streamlit as st
import pandas as pd
import datetime

# === ÄMNEN OCH KLASSER ===
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

st.title("AI-schemaplanerare för skolan")

# Initiera session_state för formulär keys (för reset)
if "larare_form_key" not in st.session_state:
    st.session_state.larare_form_key = 0
if "sal_form_key" not in st.session_state:
    st.session_state.sal_form_key = 0

def reset_larare_form():
    st.session_state.larare_form_key += 1

def reset_sal_form():
    st.session_state.sal_form_key += 1

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

with st.form(key=f"larare_form_{st.session_state.larare_form_key}"):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)", key="input_larar_id")
    amne = st.selectbox("Ämne", options=amnen, key="input_amne")
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10, key="input_undervisningstid")
    larar_klasser = st.multiselect("Undervisar i klasser", options=klasser, key="input_larar_klasser")
    arbetsdagar = st.multiselect("Arbetsdagar", options=dagar_val, default=dagar_val, key="input_arbetsdagar")
    onskemal = st.text_area("Extra önskemål (valfritt)", key="input_onskemal")

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
        reset_larare_form()

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
                st.experimental_rerun()

            if st.button("❌ Ta bort", key=f"ta_bort_larare_{i}"):
                st.session_state.larare_data.pop(i)
                st.session_state.redigera_larare_index = None
                st.experimental_rerun()

            if st.button("Avbryt", key=f"avbryt_larare_{i}"):
                st.session_state.redigera_larare_index = None
                st.experimental_rerun()
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
                    st.experimental_rerun()

# === 3. LÄGG TILL SAL ===
st.header("3. Lägg till sal")

with st.form(key=f"sal_form_{st.session_state.sal_form_key}"):
    sal_typ = st.radio("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], horizontal=True, key="sal_typ")
    sal_namn = st.text_input("Salnamn (t.ex. A101, NO-labb)", key="input_sal_namn")
    sal_klass = None
    sal_amne = None

    if sal_typ == "Hemklassrum":
        sal_klass = st.selectbox("Tilldelad klass", options=klasser, key="input_sal_klass")
    else:
        sal_amne = st.selectbox("Tilldelat ämne", options=amnen, key="input_sal_amne")

    sal_submit = st.form_submit_button("Lägg till sal")

if sal_submit:
    if st.session_state.input_sal_namn:
        ny_sal = {
            "sal": st.session_state.input_sal_namn,
            "typ": st.session_state.sal_typ,
            "klass": st.session_state.input_sal_klass if st.session_state.sal_typ == "Hemklassrum" else None,
            "ämne": st.session_state.input_sal_amne if st.session_state.sal_typ == "Ämnesklassrum" else None
        }
        if "sal_data" not in st.session_state:
            st.session_state.sal_data = []
        st.session_state.sal_data.append(ny_sal)
        st.success(f"Sal {st.session_state.input_sal_namn} tillagd!")
        reset_sal_form()

# Visa/redigera salar
st.subheader("📋 Inlagda salar")
if "sal_data" not in st.session_state or not st.session_state.sal_data:
    st.info("Inga salar inlagda ännu.")
else:
    if "redigera_sal_index" not in st.session_state:
        st.session_state.redigera_sal_index = None

    for i, sal in enumerate(st.session_state.sal_data):
        if st.session_state.redigera_sal_index == i:
            st.write(f"✏️ Redigerar sal **{sal['sal']}**")
            nytt_namn = st.text_input("Salnamn", value=sal["sal"], key=f"edit_sal_namn_{i}")
            ny_typ = st.selectbox("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"],
                                  index=["Hemklassrum", "Ämnesklassrum"].index(sal["typ"]), key=f"edit_sal_typ_{i}")

            ny_klass = None
            ny_amne = None
            if ny_typ == "Hemklassrum":
                ny_klass = st.selectbox("Tilldelad klass", options=klasser,
                                       index=klasser.index(sal["klass"]) if sal["klass"] else 0,
                                       key=f"edit_klass_{i}")
            else:
                ny_amne = st.selectbox("Tilldelat ämne", options=amnen,
                                      index=amnen.index(sal["ämne"]) if sal["ämne"] else 0,
                                      key=f"edit_amne_{i}")

            if st.button("💾 Spara sal", key=f"spara_sal_{i}"):
                st.session_state.sal_data[i] = {
                    "sal": nytt_namn,
                    "typ": ny_typ,
                    "klass": ny_klass if ny_typ == "Hemklassrum" else None,
                    "ämne": ny_amne if ny_typ == "Ämnesklassrum" else None
                }
                st.session_state.redigera_sal_index = None
                st.experimental_rerun()

            if st.button("❌ Ta bort", key=f"ta_bort_sal_{i}"):
                st.session_state.sal_data.pop(i)
                st.session_state.redigera_sal_index = None
                st.experimental_rerun()

            if st.button("Avbryt", key=f"avbryt_sal_{i}"):
                st.session_state.redigera_sal_index = None
                st.experimental_rerun()
        else:
            col1, col2 = st.columns([5, 1])
            with col1:
                info = f"{sal['sal']} – {sal['typ']}"
                if sal["klass"]:
                    info += f", klass: {sal['klass']}"
                if sal["ämne"]:
                    info += f", ämne: {sal['ämne']}"
                st.write(info)
            with col2:
                if st.button("✏️ Redigera", key=f"redigera_sal_{i}"):
                    st.session_state.redigera_sal_index = i
                    st.experimental_rerun()

# ... Du kan fortsätta med skoldagsinställningar och schemaläggning nedan ...
