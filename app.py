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
            key=f"farg_{amne}"  # unikt key per ämne
        )
    with col2:
        st.write(st.session_state.temp_farg_val[amne])

if st.button("Spara färger", key="spara_farger_knapp"):
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

# === 4. SKOLDAGENS INSTÄLLNINGAR ===
st.header("4. Inställningar för skoldagen")

with st.form("daginst_form"):
    starttid_str = st.text_input("Skoldagens starttid (HH:MM)", value="08:30")

    sluttider = {}
    for dag in dagar_val:
        sluttid_str = st.text_input(f"Sluttid för {dag} (HH:MM)", value="15:00", key=f"sluttid_{dag}")
        sluttider[dag] = sluttid_str

    lunchmin = st.number_input("Lunchrastens längd (min)", min_value=20, max_value=60, value=40)
    lek_min = st.number_input("Minsta lektionslängd (min)", min_value=30, max_value=60, value=40)
    lek_max = st.number_input("Max lektionslängd (min)", min_value=60, max_value=90, value=60)
    rast_min = st.number_input("Minsta rast (min)", min_value=5, max_value=15, value=5)
    rast_max = st.number_input("Största rast (min)", min_value=10, max_value=30, value=15)

    spara_tid = st.form_submit_button("Spara inställningar")

if spara_tid:
    try:
        starttid = datetime.datetime.strptime(starttid_str, "%H:%M").time()
        sluttider_clean = {dag: datetime.datetime.strptime(tid, "%H:%M").time() for dag, tid in sluttider.items()}

        st.session_state.daginst = {
            "starttid": starttid,
            "sluttider": sluttider_clean,
            "lunch": lunchmin,
            "lek_min": lek_min,
            "lek_max": lek_max,
            "rast_min": rast_min,
            "rast_max": rast_max
        }
        st.success("Skoldagens inställningar sparade!")
    except ValueError:
        st.error("Fel format på tid. Använd HH:MM.")


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

# === REDIGERA LÄRARE ===
st.write("### Inlagda lärare:")
if "redigera_index" not in st.session_state:
    st.session_state.redigera_index = None

for i, larare in enumerate(st.session_state.larare_data):
    if st.session_state.redigera_index == i:
        st.write(f"✏️ Redigerar lärare **{larare['id']}**")
        nytt_id = st.text_input("Lärar-ID", value=larare["id"], key=f"edit_id_{i}")
        nytt_amne = st.selectbox("Ämne", options=amnen, index=amnen.index(larare["ämne"]), key=f"edit_amne_{i}")
        nytt_tid = st.number_input("Undervisningsminuter/vecka", value=larare["minuter_per_vecka"], step=10, key=f"edit_tid_{i}")
        nytt_klasser = st.multiselect("Klasser", options=klasser, default=larare["klasser"], key=f"edit_klass_{i}")
        nytt_dagar = st.multiselect("Arbetsdagar", options=dagar_val, default=larare["dagar"], key=f"edit_dagar_{i}")

        if st.button("💾 Spara ändringar", key=f"spara_{i}"):
            st.session_state.larare_data[i] = {
                "id": nytt_id,
                "ämne": nytt_amne,
                "klasser": nytt_klasser,
                "dagar": nytt_dagar,
                "minuter_per_vecka": nytt_tid
            }
            st.session_state.redigera_index = None
            st.rerun()

        if st.button("❌ Ta bort", key=f"ta_bort_{i}"):
            st.session_state.larare_data.pop(i)
            st.session_state.redigera_index = None
            st.rerun()

        if st.button("Avbryt", key=f"avbryt_{i}"):
            st.session_state.redigera_index = None
            st.rerun()
    else:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"**{larare['id']}** – {larare['ämne']} – klasser: {', '.join(larare['klasser'])} – {larare['minuter_per_vecka']} min")
        with col2:
            if st.button("✏️ Redigera", key=f"redigera_{i}"):
                st.session_state.redigera_index = i
                st.rerun()

# === 3. LÄGG TILL SAL + REDIGERING ===
st.header("3. Lägg till sal")

sal_typ = st.radio("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], horizontal=True)

with st.form("sal_form"):
    sal_namn = st.text_input("Salnamn (t.ex. A101, NO-labb)")
    sal_klass = None
    sal_amne = None

    if sal_typ == "Hemklassrum":
        sal_klass = st.selectbox("Tilldelad klass", options=klasser)
    else:
        sal_amne = st.selectbox("Tilldelat ämne", options=amnen)

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

st.write("### Inlagda salar:")
if "redigera_sal_index" not in st.session_state:
    st.session_state.redigera_sal_index = None

for i, sal in enumerate(st.session_state.sal_data):
    if st.session_state.redigera_sal_index == i:
        st.write(f"✏️ Redigerar sal **{sal['sal']}**")
        nytt_namn = st.text_input("Salnamn", value=sal["sal"], key=f"edit_sal_namn_{i}")
        ny_typ = st.selectbox("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], index=["Hemklassrum", "Ämnesklassrum"].index(sal["typ"]), key=f"edit_sal_typ_{i}")

        ny_klass = None
        ny_amne = None
        if ny_typ == "Hemklassrum":
            ny_klass = st.selectbox("Tilldelad klass", options=klasser, index=klasser.index(sal["klass"]) if sal["klass"] else 0, key=f"edit_klass_{i}")
        else:
            ny_amne = st.selectbox("Tilldelat ämne", options=amnen, index=amnen.index(sal["ämne"]) if sal["ämne"] else 0, key=f"edit_amne_{i}")

        if st.button("💾 Spara sal", key=f"spara_sal_{i}"):
            st.session_state.sal_data[i] = {
                "sal": nytt_namn,
                "typ": ny_typ,
                "klass": ny_klass if ny_typ == "Hemklassrum" else None,
                "ämne": ny_amne if ny_typ == "Ämnesklassrum" else None
            }
            st.session_state.redigera_sal_index = None
            st.rerun()

        if st.button("❌ Ta bort", key=f"ta_bort_sal_{i}"):
            st.session_state.sal_data.pop(i)
            st.session_state.redigera_sal_index = None
            st.rerun()

        if st.button("Avbryt", key=f"avbryt_sal_{i}"):
            st.session_state.redigera_sal_index = None
            st.rerun()
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
                st.rerun()

# === 4. SKOLDAGENS INSTÄLLNINGAR ===
st.header("4. Inställningar för skoldagen")

with st.form("daginst_form"):
    starttid = st.time_input("Skoldagens starttid", value=datetime.time(8, 30))
    sluttid = st.time_input("Skoldagens sluttid", value=datetime.time(15, 0))
    lunchmin = st.number_input("Lunchrastens längd (min)", min_value=20, max_value=60, value=40)
    lek_min = st.number_input("Minsta lektionslängd (min)", min_value=30, max_value=60, value=40)
    lek_max = st.number_input("Max lektionslängd (min)", min_value=60, max_value=90, value=60)
    rast_min = st.number_input("Minsta rast (min)", min_value=5, max_value=15, value=5)
    rast_max = st.number_input("Största rast (min)", min_value=10, max_value=30, value=15)
    
    spara_tid = st.form_submit_button("Spara inställningar")

if spara_tid:
    st.session_state.daginst = {
        "starttid": starttid,
        "sluttid": sluttid,
        "lunch": lunchmin,
        "lek_min": lek_min,
        "lek_max": lek_max,
        "rast_min": rast_min,
        "rast_max": rast_max
    }
    st.success("Skoldagens inställningar sparade!")
