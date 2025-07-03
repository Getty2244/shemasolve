import streamlit as st
from streamlit.runtime.scriptrunner import RerunException, RerunData
import datetime
import pandas as pd
import random

def rerun():
    raise RerunException(RerunData())

# --- Initiera data ---
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# --- Session state init ---
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}
if "farg_saved_val" not in st.session_state:
    st.session_state.farg_saved_val = {amne: None for amne in amnen}
if "farg_changed" not in st.session_state:
    st.session_state.farg_changed = {amne: False for amne in amnen}
if "larare" not in st.session_state:
    st.session_state.larare = []
if "red_larare" not in st.session_state:
    st.session_state.red_larare = None
if "timplan" not in st.session_state:
    st.session_state.timplan = {
        amne: {"7": 120, "8": 120, "9": 120} for amne in amnen
    }
if "salar" not in st.session_state:
    st.session_state.salar = []
if "red_salar" not in st.session_state:
    st.session_state.red_salar = None
if "saltyp" not in st.session_state:
    st.session_state.saltyp = "Hemklassrum"
if "daginst" not in st.session_state:
    default_start = datetime.time(8, 30)
    default_end = {dag: datetime.time(15, 0) for dag in dagar}
    st.session_state.daginst = {
        "starttid": default_start,
        "sluttider": default_end,
        "lunch": 40,
        "lek_min": 40,
        "lek_max": 60,
        "rast_min": 5,
        "rast_max": 15
    }

st.title("Skolplanerare")

# --- Steg 1: Färgval ---
st.header("1. Färgval per ämne")
with st.form("farg_form"):
    farg_input = {}
    for amne in amnen:
        col1, col2 = st.columns([3, 1])
        with col1:
            farg_input[amne] = st.color_picker(amne, value=st.session_state.farg_val[amne], key=f"farg_{amne}")
        with col2:
            hexkod = farg_input[amne]
            if st.session_state.farg_changed.get(amne, False):
                st.markdown(f"`{hexkod}` ✔️")
            else:
                st.markdown(f"`{hexkod}`")
    if st.form_submit_button("🗓 Spara färger"):
        for amne in amnen:
            old = st.session_state.farg_val[amne]
            new = farg_input[amne]
            st.session_state.farg_changed[amne] = old != new
            st.session_state.farg_val[amne] = new
            st.session_state.farg_saved_val[amne] = new
        st.success("Färger sparade!")

# --- Steg 2: Lärare ---
st.header("2. Lärare")
# [Koden för lärare här... Samma som tidigare du använder]

# --- Steg 3: Timplan ---
st.header("3. Lokal timplan (minuter/vecka per ämne och årskurs)")
# [Timplaninput som tidigare...]

# --- Steg 4: Salar ---
st.header("4. Salar")
# [Salinput och redigering som tidigare...]

# --- Steg 5: Skoldagens inställningar ---
st.header("5. Inställningar för skoldagen")
# [Daginstinput som tidigare...]

# --- Steg 5.5: Generera schema ---
st.header("5.5 Generera schema")
if st.button("🗓 Generera schema"):
    lektioner = []
    schemat = {}
    max_per_dag = 5
    dagraeknare = {}

    for lar in st.session_state.larare:
        minuter = lar["minuter"]
        antal = minuter // 40
        dagraeknare[lar["id"]] = {dag: 0 for dag in dagar}
        schema_klass_amne = {dag: set() for dag in dagar}

        tider = list(range(8, st.session_state.daginst["sluttider"][dagar[0]].hour))
        random.shuffle(tider)
        dag_tid = [(d, t) for d in lar["dagar"] for t in tider]
        random.shuffle(dag_tid)

        placerade = 0
        for dag, tid in dag_tid:
            if placerade >= antal:
                break
            if dagraeknare[lar["id"]][dag] >= max_per_dag:
                continue
            klass = random.choice(lar["klasser"])
            if lar["ämne"] in schema_klass_amne[dag]:
                continue

            sal = next((s["sal"] for s in st.session_state.salar
                        if (s["typ"] == "Hemklassrum" and s["klass"] == klass) or
                        (s["typ"] == "Ämnesklassrum" and s["ämne"] == lar["ämne"])), "Saknas")

            key = f"{dag}_{tid}"
            if key not in schemat:
                schemat[key] = {"klass": set(), "sal": set(), "larare": set()}
            if klass in schemat[key]["klass"] or sal in schemat[key]["sal"] or lar["id"] in schemat[key]["larare"]:
                continue

            schemat[key]["klass"].add(klass)
            schemat[key]["sal"].add(sal)
            schemat[key]["larare"].add(lar["id"])
            schema_klass_amne[dag].add(lar["ämne"])

            lektioner.append({
                "dag": dag,
                "start": f"{tid}:00",
                "slut": f"{tid+1}:00",
                "klass": klass,
                "ämne": lar["ämne"],
                "lärare": lar["id"],
                "sal": sal
            })
            dagraeknare[lar["id"]][dag] += 1
            placerade += 1

    st.session_state.generated_schema = pd.DataFrame(lektioner)
    st.success("✅ Schema genererat med begränsningar och spridning")

# --- Steg 6: Visuell schemavy ---
st.header("6. Visuell schemavy")
if "generated_schema" not in st.session_state or st.session_state.generated_schema.empty:
    st.info("Inget schema genererat ännu.")
else:
    df = st.session_state.generated_schema.copy()
    col1, col2 = st.columns([1, 2])
    with col1:
        filtrera_typ = st.selectbox("Visa schema för:", ["Lärare", "Klass", "Sal"])
    with col2:
        val = st.selectbox("Välj:", sorted(df[filtrera_typ.lower()].unique()))
        filtrerat = df[df[filtrera_typ.lower()] == val]

    if filtrerat.empty:
        st.warning("Inga lektioner hittades.")
    else:
        filtrerat = filtrerat.sort_values(by=["dag", "start"])
        def fargkodning(row):
            f = st.session_state.farg_val.get(row["ämne"], "#FFFFFF")
            return [f"background-color: {f}" if col == "ämne" else "" for col in row.index]
        st.dataframe(filtrerat.style.apply(fargkodning, axis=1), height=400, use_container_width=True)
