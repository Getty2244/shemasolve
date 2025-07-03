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
    st.session_state.timplan = {amne: {"7": 120, "8": 120, "9": 120} for amne in amnen}
if "salar" not in st.session_state:
    st.session_state.salar = []
if "red_salar" not in st.session_state:
    st.session_state.red_salar = None
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
    if st.form_submit_button("🗓️ Spara färger"):
        for amne in amnen:
            old = st.session_state.farg_val[amne]
            new = farg_input[amne]
            st.session_state.farg_changed[amne] = old != new
            st.session_state.farg_val[amne] = new
            st.session_state.farg_saved_val[amne] = new
        st.success("Färger sparade!")

# --- Steg 2: Lärare ---
st.header("2. Lärare")
with st.form("add_larare", clear_on_submit=True):
    lid = st.text_input("Lärar-ID")
    amne = st.selectbox("Ämne", amnen)
    minuter = st.number_input("Minuter/vecka", min_value=10, step=10)
    kl = st.multiselect("Klasser", klasser)
    dag = st.multiselect("Arbetsdagar", dagar, default=dagar)
    onske = st.text_area("Önskemål (valfritt)")
    if st.form_submit_button("➕ Lägg till lärare"):
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
for i, l in enumerate(st.session_state.larare):
    if st.session_state.red_larare == i:
        with st.form(f"edit_larare_{i}"):
            lid = st.text_input("Lärar-ID", l["id"])
            amne = st.selectbox("Ämne", amnen, index=amnen.index(l["ämne"]))
            minuter = st.number_input("Minuter/vecka", value=l["minuter"], min_value=10, step=10)
            kl = st.multiselect("Klasser", klasser, default=l["klasser"])
            dag = st.multiselect("Arbetsdagar", dagar, default=l["dagar"])
            onske = st.text_area("Önskemål", value=l["önskemål"])
            col1, col2, col3 = st.columns(3)
            if col1.form_submit_button("🗓️ Spara"):
                st.session_state.larare[i] = {
                    "id": lid,
                    "ämne": amne,
                    "minuter": minuter,
                    "klasser": kl,
                    "dagar": dag,
                    "önskemål": onske.strip()
                }
                st.session_state.red_larare = None
                rerun()
            if col2.form_submit_button("↩️ Avbryt"):
                st.session_state.red_larare = None
                rerun()
            if col3.form_submit_button("🚑 Ta bort"):
                st.session_state.larare.pop(i)
                st.session_state.red_larare = None
                rerun()
    else:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"**{l['id']} ({l['ämne']})** – {l['minuter']} min – Klasser: {', '.join(l['klasser'])}")
        with col2:
            if st.button("✏️", key=f"edit_larare_{i}"):
                st.session_state.red_larare = i

# --- Steg 3: Timplan ---
st.header("3. Lokal timplan")
with st.form("timplan_form"):
    for amne in amnen:
        st.markdown(f"**{amne}**")
        col7, col8, col9 = st.columns(3)
        st.session_state.timplan[amne]["7"] = col7.number_input(f"Åk 7", value=st.session_state.timplan[amne]["7"], step=10)
        st.session_state.timplan[amne]["8"] = col8.number_input(f"Åk 8", value=st.session_state.timplan[amne]["8"], step=10)
        st.session_state.timplan[amne]["9"] = col9.number_input(f"Åk 9", value=st.session_state.timplan[amne]["9"], step=10)
    if st.form_submit_button("🗓️ Spara timplan"):
        st.success("Timplan sparad!")

# --- Steg 4: Salar ---
st.header("4. Salar")
with st.form("sal_form", clear_on_submit=True):
    saltyp = st.radio("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], horizontal=True)
    namn = st.text_input("Salnamn")
    sal_klass = sal_amne = None
    if saltyp == "Hemklassrum":
        sal_klass = st.selectbox("Tilldelad klass", klasser)
    else:
        sal_amne = st.selectbox("Tilldelat ämne", amnen)
    if st.form_submit_button("➕ Lägg till sal"):
        st.session_state.salar.append({
            "sal": namn,
            "typ": saltyp,
            "klass": sal_klass,
            "ämne": sal_amne
        })
        st.success(f"Sal {namn} tillagd!")

# --- Steg 5: Skoldagsinställningar ---
st.header("5. Inställningar för skoldagen")
with st.form("daginst_form"):
    starttid_str = st.text_input("Starttid (HH:MM)", value=st.session_state.daginst["starttid"].strftime("%H:%M"))
    sluttider = {}
    for dag in dagar:
        sluttider[dag] = st.text_input(f"Sluttid {dag} (HH:MM)", value=st.session_state.daginst["sluttider"][dag].strftime("%H:%M"))
    if st.form_submit_button("Spara inställningar"):
        try:
            start = datetime.datetime.strptime(starttid_str, "%H:%M").time()
            end_obj = {dag: datetime.datetime.strptime(t, "%H:%M").time() for dag, t in sluttider.items()}
            st.session_state.daginst["starttid"] = start
            st.session_state.daginst["sluttider"] = end_obj
            st.success("Inställningar sparade!")
        except:
            st.error("Fel format på tid.")

# --- Steg 6: Schema och schemavy ---
# (placera schemagenerering + visualisering här nedanför)
# Om du vill kan jag skicka det som separat block nu.

# --- Steg 6: Generera schema ---
st.header("6. Generera schema")

import pandas as pd
import random

if st.button("📅 Generera schema"):
    lektioner = []
    schemat = {}
    dagar = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    tider = list(range(8, 17))  # timmar 08–16
    max_per_dag = 5  # högre tak än tidigare

    def är_ledig(dag, tid, klass, sal, larare):
        key = f"{dag}_{tid}"
        if key not in schemat:
            return True
        bokade = schemat[key]
        return not (
            klass in bokade["klass"] or
            sal in bokade["sal"] or
            larare in bokade["larare"]
        )

    dagräknare = {}  # larare -> dag -> antal lektioner
    ämnesräknare = {}  # larare -> dag -> ämne -> antal

    for lar in st.session_state.larare:
        minuter_kvar = lar["minuter"]
        lektionslängd = 40
        antal = minuter_kvar // lektionslängd
        dagräknare[lar["id"]] = {dag: 0 for dag in dagar}
        ämnesräknare[lar["id"]] = {dag: {} for dag in dagar}

        möjliga = [(dag, tid) for dag in lar["dagar"] for tid in tider]
        random.shuffle(möjliga)

        placerade = 0
        for dag, tid in möjliga:
            if placerade >= antal:
                break

            sluttid = st.session_state.daginst["sluttider"][dag].hour
            if tid >= sluttid:
                continue

            if dagräknare[lar["id"]][dag] >= max_per_dag:
                continue

            if ämnesräknare[lar["id"]][dag].get(lar["ämne"], 0) >= 1:
                continue  # helst bara en lektion i samma ämne per dag

            klass = random.choice(lar["klasser"])

            matchande_sal = None
            for s in st.session_state.salar:
                if s["typ"] == "Hemklassrum" and s["klass"] == klass:
                    matchande_sal = s["sal"]
                elif s["typ"] == "Ämnesklassrum" and s["ämne"] == lar["ämne"]:
                    matchande_sal = s["sal"]
            sal = matchande_sal or "Saknas"

            if är_ledig(dag, tid, klass, sal, lar["id"]):
                key = f"{dag}_{tid}"
                if key not in schemat:
                    schemat[key] = {"klass": set(), "sal": set(), "larare": set()}
                schemat[key]["klass"].add(klass)
                schemat[key]["sal"].add(sal)
                schemat[key]["larare"].add(lar["id"])

                lektioner.append({
                    "dag": dag,
                    "start": f"{tid}:00",
                    "slut": f"{tid+1}:00",
                    "klass": klass,
                    "ämne": lar["ämne"],
                    "lärare": lar["id"],
                    "sal": sal
                })
                dagräknare[lar["id"]][dag] += 1
                ämnesräknare[lar["id"]][dag][lar["ämne"]] = ämnesräknare[lar["id"]][dag].get(lar["ämne"], 0) + 1
                placerade += 1

    st.session_state.generated_schema = pd.DataFrame(lektioner)
    st.success("✅ Schema genererat med spridning och begränsningar!")

# --- Steg 7: Visuell schemavy ---
st.header("7. Visuell schemavy")

if "generated_schema" not in st.session_state or st.session_state.generated_schema.empty:
    st.info("Inget schema genererat ännu.")
else:
    df = st.session_state.generated_schema.copy()

    col1, col2 = st.columns([1, 2])
    with col1:
        filtrera_typ = st.selectbox("Visa schema för:", ["Lärare", "Klass", "Sal"])
    with col2:
        if filtrera_typ == "Lärare":
            val = st.selectbox("Välj lärare:", sorted(df["lärare"].unique()))
            filtrerat = df[df["lärare"] == val]
        elif filtrera_typ == "Klass":
            val = st.selectbox("Välj klass:", sorted(df["klass"].unique()))
            filtrerat = df[df["klass"] == val]
        else:
            val = st.selectbox("Välj sal:", sorted(df["sal"].unique()))
            filtrerat = df[df["sal"] == val]

    if filtrerat.empty:
        st.warning("Inga lektioner hittades.")
    else:
        filtrerat = filtrerat.sort_values(by=["dag", "start"])

        def färgkodning(row):
            f = st.session_state.farg_val.get(row["ämne"], "#FFFFFF")
            return [f"background-color: {f}" if col == "ämne" else "" for col in row.index]

        st.dataframe(
            filtrerat.style.apply(färgkodning, axis=1),
            height=400,
            use_container_width=True
        )

