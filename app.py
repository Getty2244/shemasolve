# --- Import och funktioner ---
import streamlit as st
from streamlit.runtime.scriptrunner import RerunException, RerunData
import datetime
import pandas as pd
import random
import io

def rerun():
    raise RerunException(RerunData())

# --- Globala listor ---
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
dagar = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# --- Steg 0: Klasser ---
st.header("0. Klasser")

if "klasser" not in st.session_state:
    st.session_state.klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
if "edit_klass" not in st.session_state:
    st.session_state.edit_klass = None

with st.form("klass_form", clear_on_submit=True):
    ny_klass = st.text_input("Lägg till ny klass")
    if st.form_submit_button("➕ Lägg till klass"):
        if ny_klass and ny_klass not in st.session_state.klasser:
            st.session_state.klasser.append(ny_klass)
            rerun()

if st.session_state.klasser:
    st.markdown("**Inlagda klasser:**")
    sorted_klasser = sorted(st.session_state.klasser)
    col_count = min(5, len(sorted_klasser))  # max 5 per rad
    rows = [sorted_klasser[i:i+col_count] for i in range(0, len(sorted_klasser), col_count)]

    for row in rows:
        cols = st.columns(len(row))
        for i, klass in enumerate(row):
            with cols[i]:
                if st.session_state.edit_klass == klass:
                    ny_val = st.text_input("Redigera", value=klass, key=f"edit_input_{klass}")
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("✅", key=f"save_{klass}"):
                            if ny_val and ny_val != klass and ny_val not in st.session_state.klasser:
                                idx = st.session_state.klasser.index(klass)
                                st.session_state.klasser[idx] = ny_val
                            st.session_state.edit_klass = None
                            rerun()
                    with col2:
                        if st.button("↩️", key=f"cancel_{klass}"):
                            st.session_state.edit_klass = None
                            rerun()
                else:
                    st.markdown(f"**{klass}**")
                    if st.button("✏️", key=f"edit_{klass}"):
                        st.session_state.edit_klass = klass
                    if st.button("❌", key=f"del_{klass}"):
                        st.session_state.klasser.remove(klass)
                        rerun()




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
            st.markdown(f"`{hexkod}`")
    if st.form_submit_button("Spara färger"):
        for amne in amnen:
            old = st.session_state.farg_val[amne]
            new = farg_input[amne]
            st.session_state.farg_val[amne] = new
            st.session_state.farg_saved_val[amne] = new
        st.success("Färger sparade!")

# --- Steg 2: Lärare ---
st.header("2. Lärare")
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

# --- Steg 3: Timplan ---
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

# --- Resterande steg (4-7) ---
# Vill du att jag inkluderar salar, daginst, schemagenerering och vy/export direkt nu?
# Säg bara till så skickar jag allt med samma tillägg för klasser.

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

