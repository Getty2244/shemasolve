import streamlit as st

# Konstanter
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Initiera session_state för färger, lärare och salar
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}

if "larare_data" not in st.session_state:
    st.session_state.larare_data = []

if "sal_data" not in st.session_state:
    st.session_state.sal_data = []

if "redigera_larare_index" not in st.session_state:
    st.session_state.redigera_larare_index = None

if "redigera_sal_index" not in st.session_state:
    st.session_state.redigera_sal_index = None

# Funktioner för att rensa formulärinmatningar
def reset_larare_inputs():
    st.session_state.input_larar_id = ""
    st.session_state.input_amne = amnen[0]
    st.session_state.input_undervisningstid = 0
    st.session_state.input_larar_klasser = []
    st.session_state.input_arbetsdagar = dagar_val
    st.session_state.input_onskemal = ""

def reset_sal_inputs():
    st.session_state.input_sal_namn = ""
    st.session_state.input_sal_typ = "Hemklassrum"
    st.session_state.input_sal_klass = klasser[0]
    st.session_state.input_sal_amne = amnen[0]

# Initiera inmatningsfält för lärare
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

# Initiera inmatningsfält för sal
for key, default in {
    "input_sal_namn": "",
    "input_sal_typ": "Hemklassrum",
    "input_sal_klass": klasser[0],
    "input_sal_amne": amnen[0]
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.title("AI-schemaplanerare")

# --- 1. Färgval ---
st.header("1. Färgval för ämnen")
for amne in amnen:
    st.session_state.farg_val[amne] = st.color_picker(
        amne, st.session_state.farg_val[amne], key=f"farg_{amne}"
    )
if st.button("Spara färger"):
    st.success("Färger sparade!")

# --- 2. Lägg till / redigera lärare ---
st.header("2. Lägg till lärare")

with st.form("larare_form", clear_on_submit=False):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)", key="input_larar_id")
    amne = st.selectbox("Ämne", amnen, index=amnen.index(st.session_state.input_amne), key="input_amne")
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10, key="input_undervisningstid")
    larar_klasser = st.multiselect("Undervisar i klasser", klasser, default=st.session_state.input_larar_klasser, key="input_larar_klasser")
    arbetsdagar = st.multiselect("Arbetsdagar", dagar_val, default=st.session_state.input_arbetsdagar, key="input_arbetsdagar")
    onskemal = st.text_area("Extra önskemål (valfritt)", key="input_onskemal")
    skicka = st.form_submit_button("Spara")

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
        if st.session_state.redigera_larare_index is not None:
            st.session_state.larare_data[st.session_state.redigera_larare_index] = ny_larare
            st.session_state.redigera_larare_index = None
            st.success(f"Lärare {larar_id} uppdaterad!")
        else:
            st.session_state.larare_data.append(ny_larare)
            st.success(f"Lärare {larar_id} tillagd!")

        reset_larare_inputs()
        st.experimental_rerun()
    else:
        st.error("Fyll i alla obligatoriska fält!")

# Visa/redigera lärare
st.subheader("📋 Inlagda lärare")

if not st.session_state.larare_data:
    st.info("Inga lärare inlagda ännu.")
else:
    for i, larare in enumerate(st.session_state.larare_data):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"- **{larare['id']}** ({larare['ämne']}), Klasser: {', '.join(larare['klasser'])}, Dagar: {', '.join(larare['dagar'])}, Minuter/vecka: {larare['minuter_per_vecka']}")
        with col2:
            if st.button("✏️ Redigera", key=f"redigera_larare_{i}"):
                st.session_state.redigera_larare_index = i
                lar = st.session_state.larare_data[i]
                st.session_state.input_larar_id = lar['id']
                st.session_state.input_amne = lar['ämne']
                st.session_state.input_undervisningstid = lar['minuter_per_vecka']
                st.session_state.input_larar_klasser = lar['klasser']
                st.session_state.input_arbetsdagar = lar['dagar']
                st.session_state.input_onskemal = lar.get('önskemål', '')
                st.experimental_rerun()
            if st.button("❌ Ta bort", key=f"ta_bort_larare_{i}"):
                st.session_state.larare_data.pop(i)
                st.experimental_rerun()

# --- 3. Lägg till / redigera sal ---
st.header("3. Lägg till sal")

with st.form("sal_form", clear_on_submit=False):
    sal_typ = st.radio("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], index=["Hemklassrum", "Ämnesklassrum"].index(st.session_state.input_sal_typ), key="input_sal_typ")

    sal_namn = st.text_input("Salnamn (ex: A101, NO-labb)", key="input_sal_namn")

    if sal_typ == "Hemklassrum":
        sal_klass = st.selectbox("Tilldelad klass", klasser, index=klasser.index(st.session_state.input_sal_klass), key="input_sal_klass")
        sal_amne = None
    else:
        sal_amne = st.selectbox("Tilldelat ämne", amnen, index=amnen.index(st.session_state.input_sal_amne), key="input_sal_amne")
        sal_klass = None

    sal_submit = st.form_submit_button("Spara sal")

if sal_submit:
    if sal_namn and ((sal_typ == "Hemklassrum" and sal_klass) or (sal_typ == "Ämnesklassrum" and sal_amne)):
        ny_sal = {
            "sal": sal_namn,
            "typ": sal_typ,
            "klass": sal_klass,
            "ämne": sal_amne
        }
        if st.session_state.redigera_sal_index is not None:
            st.session_state.sal_data[st.session_state.redigera_sal_index] = ny_sal
            st.session_state.redigera_sal_index = None
            st.success(f"Sal {sal_namn} uppdaterad!")
        else:
            st.session_state.sal_data.append(ny_sal)
            st.success(f"Sal {sal_namn} tillagd!")

        reset_sal_inputs()
        st.experimental_rerun()
    else:
        st.error("Fyll i alla obligatoriska fält för sal!")

# Visa/redigera salar
st.subheader("📋 Inlagda salar")

if not st.session_state.sal_data:
    st.info("Inga salar inlagda ännu.")
else:
    for i, sal in enumerate(st.session_state.sal_data):
        col1, col2 = st.columns([5,1])
        with col1:
            text = f"{sal['sal']} ({sal['typ']})"
            if sal['typ'] == "Hemklassrum" and sal['klass']:
                text += f", klass: {sal['klass']}"
            if sal['typ'] == "Ämnesklassrum" and sal['ämne']:
                text += f", ämne: {sal['ämne']}"
            st.write(text)
        with col2:
            if st.button("✏️ Redigera", key=f"redigera_sal_{i}"):
                st.session_state.redigera_sal_index = i
                s = st.session_state.sal_data[i]
                st.session_state.input_sal_namn = s['sal']
                st.session_state.input_sal_typ = s['typ']
                st.session_state.input_sal_klass = s.get('klass', klasser[0])
                st.session_state.input_sal_amne = s.get('ämne', amnen[0])
                st.experimental_rerun()
            if st.button("❌ Ta bort", key=f"ta_bort_sal_{i}"):
                st.session_state.sal_data.pop(i)
                st.experimental_rerun()
