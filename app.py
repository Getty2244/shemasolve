import streamlit as st

# === ÄMNEN OCH KLASSER ===
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# --- Funktion för att tvinga omstart av appen ---
from streamlit.runtime.scriptrunner.script_runner import RerunException, RerunData
def rerun():
    raise RerunException(RerunData())

# --- Reset inputfält om flagga satt ---
if "reset_larare_input" in st.session_state and st.session_state.reset_larare_input:
    st.session_state.input_larar_id = ""
    st.session_state.input_amne = amnen[0]
    st.session_state.input_undervisningstid = 0
    st.session_state.input_larar_klasser = []
    st.session_state.input_arbetsdagar = dagar_val
    st.session_state.input_onskemal = ""
    st.session_state.reset_larare_input = False

# --- Initiera session_state-variabler vid start ---
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

if "larare_data" not in st.session_state:
    st.session_state.larare_data = []

st.title("AI-schemaplanerare för skolan")

# === 1. Färgval för ämnen (exempel, kan utvecklas) ===
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

# === 2. Lägg till lärare ===
st.header("2. Lägg till lärare")

with st.form("larare_form"):
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
        st.session_state.larare_data.append(ny_larare)
        st.success(f"Lärare {larar_id} tillagd!")

        # Sätt flaggan för reset av inputfält vid nästa rerun
        st.session_state.reset_larare_input = True
        rerun()

# === Visa inlagda lärare ===
st.subheader("📋 Inlagda lärare")
if not st.session_state.larare_data:
    st.info("Inga lärare inlagda ännu.")
else:
    for larare in st.session_state.larare_data:
        st.markdown(f"- **{larare['id']}** ({larare['ämne']}) — Klasser: {', '.join(larare['klasser'])}, Dagar: {', '.join(larare['dagar'])}, Minuter/vecka: {larare['minuter_per_vecka']}")
# === 3. LÄGG TILL SAL ===
st.header("3. Lägg till sal")

if "input_sal_namn" not in st.session_state:
    st.session_state.input_sal_namn = ""
if "input_sal_typ" not in st.session_state:
    st.session_state.input_sal_typ = "Hemklassrum"
if "input_sal_klass" not in st.session_state:
    st.session_state.input_sal_klass = klasser[0]
if "input_sal_amne" not in st.session_state:
    st.session_state.input_sal_amne = amnen[0]

with st.form("sal_form"):
    sal_typ = st.radio("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], horizontal=True, key="input_sal_typ")
    sal_namn = st.text_input("Salnamn (t.ex. A101, NO-labb)", value=st.session_state.input_sal_namn, key="input_sal_namn")
    sal_klass = None
    sal_amne = None

    if sal_typ == "Hemklassrum":
        sal_klass = st.selectbox("Tilldelad klass", options=klasser, index=klasser.index(st.session_state.input_sal_klass), key="input_sal_klass")
    else:
        sal_amne = st.selectbox("Tilldelat ämne", options=amnen, index=amnen.index(st.session_state.input_sal_amne), key="input_sal_amne")

    sal_submit = st.form_submit_button("Lägg till sal")

if "sal_data" not in st.session_state:
    st.session_state.sal_data = []

def rerun():
    raise RerunException(RerunData())

if sal_submit and sal_namn:
    ny_sal = {
        "sal": sal_namn,
        "typ": sal_typ,
        "klass": sal_klass if sal_typ == "Hemklassrum" else None,
        "ämne": sal_amne if sal_typ == "Ämnesklassrum" else None
    }
    st.session_state.sal_data.append(ny_sal)
    st.success(f"Sal {sal_namn} tillagd!")

    # Rensa inputfält
    st.session_state.input_sal_namn = ""
    st.session_state.input_sal_typ = "Hemklassrum"
    st.session_state.input_sal_klass = klasser[0]
    st.session_state.input_sal_amne = amnen[0]

    rerun()

# Visa och redigera salar
st.subheader("📋 Inlagda salar")
if not st.session_state.sal_data:
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
                                       index=klasser.index(sal["klass"]) if sal["klass"] else 0, key=f"edit_klass_{i}")
            else:
                ny_amne = st.selectbox("Tilldelat ämne", options=amnen,
                                      index=amnen.index(sal["ämne"]) if sal["ämne"] else 0, key=f"edit_amne_{i}")

            if st.button("💾 Spara sal", key=f"spara_sal_{i}"):
                st.session_state.sal_data[i] = {
                    "sal": nytt_namn,
                    "typ": ny_typ,
                    "klass": ny_klass if ny_typ == "Hemklassrum" else None,
                    "ämne": ny_amne if ny_typ == "Ämnesklassrum" else None
                }
                st.session_state.redigera_sal_index = None
                rerun()

            if st.button("❌ Ta bort", key=f"ta_bort_sal_{i}"):
                st.session_state.sal_data.pop(i)
                st.session_state.redigera_sal_index = None
                rerun()

            if st.button("Avbryt", key=f"avbryt_sal_{i}"):
                st.session_state.redigera_sal_index = None
                rerun()
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
                    rerun()

