import streamlit as st
import datetime
from streamlit.runtime.scriptrunner.script_runner import RerunException, RerunData

def rerun():
    raise RerunException(RerunData())

# Ämnen och klasser
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

st.title("AI-schemaplanerare för skolan")

# --- INITIERA SESSION_STATE FÖR LÄRARE INPUT ---
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

# --- INITIERA SESSION_STATE FÖR SALAR INPUT ---
if "input_sal_namn" not in st.session_state:
    st.session_state.input_sal_namn = ""
if "input_sal_typ" not in st.session_state:
    st.session_state.input_sal_typ = "Hemklassrum"
if "input_sal_klass" not in st.session_state:
    st.session_state.input_sal_klass = klasser[0]
if "input_sal_amne" not in st.session_state:
    st.session_state.input_sal_amne = amnen[0]

# --- INITIERA LISTOR FÖR DATA ---
if "larare_data" not in st.session_state:
    st.session_state.larare_data = []
if "sal_data" not in st.session_state:
    st.session_state.sal_data = []

# --- RESET FUNKTIONER ---
def reset_larare_inputs():
    st.session_state.input_larar_id = ""
    st.session_state.input_amne = amnen[0]
    st.session_state.input_undervisningstid = 0
    st.session_state.input_larar_klasser = []
    st.session_state.input_arbetsdagar = dagar_val.copy()
    st.session_state.input_onskemal = ""

def reset_sal_inputs():
    st.session_state.input_sal_namn = ""
    st.session_state.input_sal_typ = "Hemklassrum"
    st.session_state.input_sal_klass = klasser[0]
    st.session_state.input_sal_amne = amnen[0]

# --- 1. LÄGG TILL / REDIGERA LÄRARE ---
st.header("2. Lägg till / Redigera lärare")

if "redigera_larare_index" not in st.session_state:
    st.session_state.redigera_larare_index = None

with st.form("larare_form", clear_on_submit=False):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)", key="input_larar_id")
    amne = st.selectbox("Ämne", options=amnen, key="input_amne")
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10, key="input_undervisningstid")
    larar_klasser = st.multiselect("Undervisar i klasser", options=klasser, key="input_larar_klasser")
    arbetsdagar = st.multiselect("Arbetsdagar", options=dagar_val, default=dagar_val, key="input_arbetsdagar")
    onskemal = st.text_area("Extra önskemål (valfritt)", key="input_onskemal")

    skicka = st.form_submit_button("Spara lärare")

if skicka:
    if not larar_id:
        st.error("Lärar-ID måste fyllas i!")
    elif undervisningstid <= 0:
        st.error("Undervisningsminuter måste vara större än 0!")
    elif not larar_klasser:
        st.error("Välj minst en klass!")
    elif not arbetsdagar:
        st.error("Välj minst en arbetsdag!")
    else:
        ny_larare = {
            "id": larar_id,
            "ämne": amne,
            "klasser": larar_klasser,
            "dagar": arbetsdagar,
            "minuter_per_vecka": undervisningstid,
            "önskemål": onskemal or ""
        }
        if st.session_state.redigera_larare_index is not None:
            # Uppdatera existerande
            st.session_state.larare_data[st.session_state.redigera_larare_index] = ny_larare
            st.success(f"Lärare {larar_id} uppdaterad!")
            st.session_state.redigera_larare_index = None
        else:
            # Lägg till ny lärare
            st.session_state.larare_data.append(ny_larare)
            st.success(f"Lärare {larar_id} tillagd!")
        reset_larare_inputs()
        rerun()

# Visa lista + redigera / ta bort knappar
st.subheader("📋 Inlagda lärare")
if not st.session_state.larare_data:
    st.info("Inga lärare inlagda ännu.")
else:
    for i, larare in enumerate(st.session_state.larare_data):
        if st.session_state.redigera_larare_index == i:
            st.info(f"Redigerar lärare: {larare['id']}")
        else:
            col1, col2 = st.columns([7,1])
            with col1:
                st.markdown(f"**{larare['id']}** — {larare['ämne']}, klasser: {', '.join(larare['klasser'])}, dagar: {', '.join(larare['dagar'])}, min/vecka: {larare['minuter_per_vecka']}")
            with col2:
                if st.button("✏️ Redigera", key=f"redigera_larare_{i}"):
                    st.session_state.redigera_larare_index = i
                    # Sätt inputfälten till denna lärares värden
                    st.session_state.input_larar_id = larare["id"]
                    st.session_state.input_amne = larare["ämne"]
                    st.session_state.input_undervisningstid = larare["minuter_per_vecka"]
                    st.session_state.input_larar_klasser = larare["klasser"]
                    st.session_state.input_arbetsdagar = larare["dagar"]
                    st.session_state.input_onskemal = larare.get("önskemål", "")
                    rerun()
                if st.button("🗑 Ta bort", key=f"ta_bort_larare_{i}"):
                    st.session_state.larare_data.pop(i)
                    # Om man redigerar just nu, avbryt redigering
                    if st.session_state.redigera_larare_index == i:
                        st.session_state.redigera_larare_index = None
                    rerun()

# --- 2. LÄGG TILL / REDIGERA SALAR ---
st.header("3. Lägg till / Redigera sal")

if "redigera_sal_index" not in st.session_state:
    st.session_state.redigera_sal_index = None

with st.form("sal_form", clear_on_submit=False):
    sal_typ = st.radio("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], key="input_sal_typ", horizontal=True)
    sal_namn = st.text_input("Salnamn (t.ex. A101, NO-labb)", key="input_sal_namn")

    if sal_typ == "Hemklassrum":
        sal_klass = st.selectbox("Tilldelad klass", options=klasser, key="input_sal_klass")
    else:
        sal_amne = st.selectbox("Tilldelat ämne", options=amnen, key="input_sal_amne")

    sal_submit = st.form_submit_button("Spara sal")

if sal_submit:
    if not st.session_state.input_sal_namn:
        st.error("Salnamn måste fyllas i!")
    else:
        ny_sal = {
            "sal": st.session_state.input_sal_namn,
            "typ": st.session_state.input_sal_typ,
            "klass": st.session_state.input_sal_klass if st.session_state.input_sal_typ == "Hemklassrum" else None,
            "ämne": st.session_state.input_sal_amne if st.session_state.input_sal_typ == "Ämnesklassrum" else None
        }
        if st.session_state.redigera_sal_index is not None:
            st.session_state.sal_data[st.session_state.redigera_sal_index] = ny_sal
            st.success(f"Sal {st.session_state.input_sal_namn} uppdaterad!")
            st.session_state.redigera_sal_index = None
        else:
            st.session_state.sal_data.append(ny_sal)
            st.success(f"Sal {st.session_state.input_sal_namn} tillagd!")
        reset_sal_inputs()
        rerun()

# Visa lista + redigera / ta bort sal
st.subheader("📋 Inlagda salar")
if not st.session_state.sal_data:
    st.info("Inga salar inlagda ännu.")
else:
    for i, sal in enumerate(st.session_state.sal_data):
        if st.session_state.redigera_sal_index == i:
            st.info(f"Redigerar sal: {sal['sal']}")
        else:
            col1, col2 = st.columns([7,1])
            with col1:
                info = f"{sal['sal']} — {sal['typ']}"
                if sal["klass"]:
                    info += f", klass: {sal['klass']}"
                if sal["ämne"]:
                    info += f", ämne: {sal['ämne']}"
                st.write(info)
            with col2:
                if st.button("✏️ Redigera", key=f"redigera_sal_{i}"):
                    st.session_state.redigera_sal_index = i
                    # Sätt inputfälten för salen som redigeras
                    st.session_state.input_sal_namn = sal["sal"]
                    st.session_state.input_sal_typ = sal["typ"]
                    if sal["typ"] == "Hemklassrum":
                        st.session_state.input_sal_klass = sal["klass"] or klasser[0]
                    else:
                        st.session_state.input_sal_amne = sal["ämne"] or amnen[0]
                    rerun()
                if st.button("🗑 Ta bort", key=f"ta_bort_sal_{i}"):
                    st.session_state.sal_data.pop(i)
                    if st.session_state.redigera_sal_index == i:
                        st.session_state.redigera_sal_index = None
                    rerun()
