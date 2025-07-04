import streamlit as st
import pandas as pd
import random
import datetime
import pickle
import base64
from collections import defaultdict
import io

st.set_page_config(page_title="SchemaSolve", layout="wide")

# Initiera session_state
if "larare" not in st.session_state:
    st.session_state.larare = []
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {"SO": "#FFD700", "ENG": "#87CEEB", "MA": "#90EE90"}
if "farg_saved_val" not in st.session_state:
    st.session_state.farg_saved_val = st.session_state.farg_val.copy()
if "timplan" not in st.session_state:
    st.session_state.timplan = {}
if "salar" not in st.session_state:
    st.session_state.salar = []
if "daginst" not in st.session_state:
    st.session_state.daginst = {
        "starttid": datetime.time(8, 0),
        "sluttider": {dag: datetime.time(15, 0) for dag in ["Mon", "Tue", "Wed", "Thu", "Fri"]}
    }

# Globala listor
dagar = ["Mon", "Tue", "Wed", "Thu", "Fri"]
amnen = ["SO", "ENG", "MA"]

# --- Steg 0: Klasser ---
st.header("0. Klasser")
if "klasser" not in st.session_state:
    st.session_state.klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
if "edit_arskurs" not in st.session_state:
    st.session_state.edit_arskurs = None

with st.form("klass_form", clear_on_submit=True):
    ny_klass = st.text_input("Lägg till ny klass")
    if st.form_submit_button("➕ Lägg till klass"):
        if ny_klass and ny_klass not in st.session_state.klasser:
            st.session_state.klasser.append(ny_klass)
            st.rerun()

if st.session_state.klasser:
    st.markdown("**Inlagda klasser (per årskurs):**")
    grupper = {}
    for k in sorted(st.session_state.klasser):
        if k and k[0].isdigit():
            grupper.setdefault(k[0], []).append(k)
        else:
            grupper.setdefault("Övrigt", []).append(k)

    for ar, kl_list in grupper.items():
        st.markdown(f"**Årskurs {ar}:**")
        if st.session_state.edit_arskurs == ar:
            nya_klasser = []
            cols = st.columns(len(kl_list))
            for i, klass in enumerate(kl_list):
                with cols[i]:
                    nya_klass = st.text_input("", value=klass, key=f"edit_{ar}_{i}")
                    nya_klasser.append(nya_klass)
                    if st.button("🗑️", key=f"del_{ar}_{i}"):
                        if klass in st.session_state.klasser:
                            st.session_state.klasser.remove(klass)
                            st.rerun()
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✅ Spara ändringar", key=f"spara_{ar}"):
                    for gammal, ny in zip(kl_list, nya_klasser):
                        if ny != gammal and ny not in st.session_state.klasser:
                            idx = st.session_state.klasser.index(gammal)
                            st.session_state.klasser[idx] = ny
                    st.session_state.edit_arskurs = None
                    st.rerun()
            with col2:
                if st.button("↩️ Avbryt", key=f"avbryt_{ar}"):
                    st.session_state.edit_arskurs = None
                    st.rerun()
        else:
            st.markdown(", ".join(kl_list))
            if st.button(f"✏️ Redigera årskurs {ar}", key=f"edit_knapp_{ar}"):
                st.session_state.edit_arskurs = ar
                st.rerun()

alla_ar = sorted(set(k[0] for k in st.session_state.klasser if k and k[0].isdigit()))
for amne in amnen:
    if amne not in st.session_state.timplan:
        st.session_state.timplan[amne] = {}
    for ar in alla_ar:
        if ar not in st.session_state.timplan[amne]:
            st.session_state.timplan[amne][ar] = 120

# --- Steg 1: Färgval per ämne ---
st.header("1. Färgval per ämne")
with st.form("farg_form"):
    farg_input = {}
    for amne in amnen:
        col1, col2 = st.columns([3, 1])
        with col1:
            farg_input[amne] = st.color_picker(amne, value=st.session_state.farg_val.get(amne, "#FFFFFF"), key=f"farg_{amne}")
        with col2:
            st.markdown(f"`{farg_input[amne]}`")
    if st.form_submit_button("Spara färger"):
        for amne in amnen:
            st.session_state.farg_val[amne] = farg_input[amne]
            st.session_state.farg_saved_val[amne] = farg_input[amne]
        st.success("Färger sparade!")

# --- Steg 2: Lärare ---
st.header("2. Lärare")
if "edit_larare_index" not in st.session_state:
    st.session_state.edit_larare_index = None

if st.session_state.edit_larare_index is not None:
    i = st.session_state.edit_larare_index
    lar = st.session_state.larare[i]
    st.subheader(f"✏️ Redigerar lärare: {lar['id']}")
    with st.form("edit_larare_form"):
        lid = st.text_input("Lärar-ID", value=lar["id"])
        amne = st.selectbox("Ämne", amnen, index=amnen.index(lar["ämne"]))
        minuter = st.number_input("Minuter/vecka", min_value=10, step=10, value=lar["minuter"])
        kl = st.multiselect("Klasser", st.session_state.klasser, default=lar["klasser"])
        dag = st.multiselect("Arbetsdagar", dagar, default=lar["dagar"])
        onske = st.text_area("Önskemål (valfritt)", value=lar["önskemål"])
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.form_submit_button("💾 Spara ändringar"):
                st.session_state.larare[i] = {
                    "id": lid,
                    "ämne": amne,
                    "minuter": minuter,
                    "klasser": kl,
                    "dagar": dag,
                    "önskemål": onske.strip()
                }
                st.session_state.edit_larare_index = None
                st.success("Ändringar sparade.")
                st.rerun()
        with col2:
            if st.form_submit_button("↩️ Avbryt"):
                st.session_state.edit_larare_index = None
                st.info("Redigering avbröts.")
else:
    with st.form("add_larare", clear_on_submit=True):
        lid = st.text_input("Lärar-ID")
        amne = st.selectbox("Ämne", amnen)
        minuter = st.number_input("Minuter/vecka", min_value=10, step=10)
        kl = st.multiselect("Klasser", st.session_state.klasser)
        dag = st.multiselect("Arbetsdagar", dagar, default=dagar)
        onske = st.text_area("Önskemål (valfritt)")
        if st.form_submit_button("Lägg till lärare"):
            if lid and kl and minuter > 0:
                st.session_state.larare.append({
                    "id": lid,
                    "ämne": amne,
                    "minuter": minuter,
                    "klasser": kl,
                    "dagar": dag,
                    "önskemål": onske.strip()
                })
                st.success(f"Lärare {lid} tillagd!")

st.subheader("📋 Inlagda lärare")
if st.session_state.larare:
    for i, lar in enumerate(st.session_state.larare):
        with st.expander(f"{lar['id']} ({lar['ämne']})", expanded=False):
            st.markdown(f"- **Ämne:** {lar['ämne']}")
            st.markdown(f"- **Minuter/vecka:** {lar['minuter']}")
            st.markdown(f"- **Klasser:** {', '.join(lar['klasser'])}")
            st.markdown(f"- **Arbetsdagar:** {', '.join(lar['dagar'])}")
            if lar['önskemål']:
                st.markdown(f"- **Önskemål:** {lar['önskemål']}")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✏️ Redigera", key=f"edit_larare_{i}"):
                    st.session_state.edit_larare_index = i
                    st.rerun()
            with col2:
                if st.button("🗑️ Ta bort", key=f"delete_larare_{i}"):
                    st.session_state.larare.pop(i)
                    st.success("Lärare borttagen.")
                    st.rerun()
else:
    st.info("Inga lärare inlagda ännu.")

# --- Spara och ladda data med profilnamn ---
st.header("💾 Spara / Ladda schema")

keys_to_save = [
    "klasser", "larare", "farg_val", "farg_saved_val", "timplan",
    "salar", "daginst", "generated_schema"
]

profilnamn = st.text_input("Ange ett profilnamn (t.ex. skolans namn eller initialer)", value="min_skola")
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("💾 Spara konfiguration"):
        if profilnamn.strip():
            filnamn = f"{profilnamn.strip()}_schema.pkl"
            data_to_save = {k: st.session_state.get(k) for k in keys_to_save}
            with open(filnamn, "wb") as f:
                pickle.dump(data_to_save, f)
            with open(filnamn, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:file/pkl;base64,{b64}" download="{filnamn}">⬇️ Klicka här för att ladda ner \"{filnamn}\"</a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning("Vänligen ange ett profilnamn innan du sparar.")

with col2:
    uploaded_file = st.file_uploader("📁 Ladda in en tidigare sparad fil", type=["pkl"])
    if uploaded_file is not None:
        try:
            loaded_data = pickle.load(uploaded_file)
            for k in keys_to_save:
                if k in loaded_data:
                    st.session_state[k] = loaded_data[k]
            st.success("✅ Data inläst! Ladda om sidan för att se uppdateringarna.")
        except Exception as e:
            st.error(f"Fel vid inläsning: {e}")
