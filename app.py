import streamlit as st
import pandas as pd
import random
import datetime
from collections import defaultdict

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

dagar = ["Mon", "Tue", "Wed", "Thu", "Fri"]
amnen = ["SO", "ENG", "MA"]

# --- Steg 0: Klasser ---
st.header("0. Klasser")

if "klasser" not in st.session_state:
    st.session_state.klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
if "edit_arskurs" not in st.session_state:
    st.session_state.edit_arskurs = None

# Lägg till ny klass
with st.form("klass_form", clear_on_submit=True):
    ny_klass = st.text_input("Lägg till ny klass")
    if st.form_submit_button("➕ Lägg till klass"):
        if ny_klass and ny_klass not in st.session_state.klasser:
            st.session_state.klasser.append(ny_klass)
            st.rerun()

# Gruppvisning per årskurs
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

# --- Mellanblock: Årskurser och timplan-synk ---
alla_ar = sorted(set(k[0] for k in st.session_state.klasser if k and k[0].isdigit()))

# Se till att alla ämnen har timplan-data för varje årskurs
for amne in amnen:
    if amne not in st.session_state.timplan:
        st.session_state.timplan[amne] = {}
    for ar in alla_ar:
        if ar not in st.session_state.timplan[amne]:
            st.session_state.timplan[amne][ar] = 120  # eller valfri standardtid









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

# Initiera redigeringsindex om det inte finns
if "edit_larare_index" not in st.session_state:
    st.session_state.edit_larare_index = None

# Om redigering pågår – visa formulär för aktuell lärare
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

# Annars – visa formulär för att lägga till ny lärare
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

# --- Steg 2b: Läraröversikt ---
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



# --- Steg 3: Lokal timplan ---
st.header("3. Lokal timplan")
with st.form("timplan_form"):
    for amne in amnen:
        st.markdown(f"**{amne}**")
        cols = st.columns(len(alla_ar))
        for i, ar in enumerate(alla_ar):
            st.session_state.timplan[amne][ar] = cols[i].number_input(
                f"Åk {ar}", value=st.session_state.timplan[amne][ar], step=10, key=f"tp_{amne}_{ar}"
            )
    if st.form_submit_button("Spara timplan"):
        st.success("Timplan sparad!")


# --- Steg 4: Salar ---
st.header("4. Salar")

saltyp = st.radio("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], horizontal=True, key="saltyp_val")

with st.form("sal_form", clear_on_submit=True):
    namn = st.text_input("Salnamn")
    sal_klass = sal_amne = None

    if saltyp == "Hemklassrum":
        sal_klass = st.selectbox("Tilldelad klass", st.session_state.klasser)
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

st.subheader("📋 Inlagda salar")
for i, s in enumerate(st.session_state.salar):
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"**{s['sal']}** – {s['typ']} – {s.get('klass') or s.get('ämne')}")
    with col2:
        if st.button("✏️", key=f"edit_salar_{i}"):
            pass  # Redigering är inte aktiv just nu

# --- Steg 5: Inställningar för skoldagen ---
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

# --- Steg 6: Generera schema ---
st.header("6. Generera schema")

if st.button("🗓️ Generera schema"):
    lektioner = []
    schemat = {}
    tider = list(range(8, 17))
    max_per_dag = 5

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

    dagräknare = {}
    ämnesräknare = {}

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
                continue

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
    st.success("✅ Schema genererat!")

# --- Steg 7: Visuell schemavy + export ---
st.header("7. Visuell schemavy")

if "generated_schema" in st.session_state and not st.session_state.generated_schema.empty:
    df = st.session_state.generated_schema.copy()

    col1, col2 = st.columns([1, 2])
    with col1:
        typ = st.selectbox("Visa schema för:", ["Lärare", "Klass", "Sal"])
    with col2:
        if typ == "Lärare":
            val = st.selectbox("Välj lärare:", sorted(df["lärare"].unique()))
            df = df[df["lärare"] == val]
        elif typ == "Klass":
            val = st.selectbox("Välj klass:", sorted(df["klass"].unique()))
            df = df[df["klass"] == val]
        else:
            val = st.selectbox("Välj sal:", sorted(df["sal"].unique()))
            df = df[df["sal"] == val]

    df = df.sort_values(by=["dag", "start"])

    def färg_raden(row):
        f = st.session_state.farg_val.get(row["ämne"], "#FFFFFF")
        return [f"background-color: {f}"] * len(row)

    st.dataframe(df.style.apply(färg_raden, axis=1), use_container_width=True, height=400)

    import io
    excel_data = io.BytesIO()
    df.to_excel(excel_data, index=False)
    st.download_button("⬇️ Ladda ner som Excel", data=excel_data.getvalue(), file_name="schema.xlsx")
else:
    st.info("Inget schema genererat ännu.")

# --- Spara och ladda data ---
st.header("💾 Spara / Ladda schema")

import pickle
import base64

# Lista över vilka keys i session_state som ska sparas
keys_to_save = [
    "klasser", "larare", "farg_val", "farg_saved_val", "timplan",
    "salar", "daginst", "generated_schema"
]

# 🎒 Spara data till fil
if st.button("💾 Spara konfiguration"):
    data_to_save = {k: st.session_state.get(k) for k in keys_to_save}
    with open("schema_data.pkl", "wb") as f:
        pickle.dump(data_to_save, f)
    with open("schema_data.pkl", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:file/pkl;base64,{b64}" download="schema_data.pkl">⬇️ Klicka här för att ladda ner</a>'
        st.markdown(href, unsafe_allow_html=True)

# 📂 Ladda data från fil
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
# --- Spara och ladda data med profilnamn ---
st.header("💾 Spara / Ladda schema")

import pickle
import base64

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
                href = f'<a href="data:file/pkl;base64,{b64}" download="{filnamn}">⬇️ Klicka här för att ladda ner "{filnamn}"</a>'
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


