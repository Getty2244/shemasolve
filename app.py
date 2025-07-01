import streamlit as st
from streamlit.runtime.scriptrunner import RerunException, RerunData
import datetime

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

# --- Steg 1: Färgval per ämne ---
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
    if st.form_submit_button("📅 Spara färger"):
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
            lid = st.text_input("Lärar-ID", l["id"], key=f"lid_{i}")
            amne = st.selectbox("Ämne", amnen, index=amnen.index(l["ämne"]), key=f"amne_{i}")
            minuter = st.number_input("Minuter/vecka", value=l["minuter"], min_value=10, step=10, key=f"minuter_{i}")
            kl = st.multiselect("Klasser", klasser, default=l["klasser"], key=f"klasser_{i}")
            dag = st.multiselect("Arbetsdagar", dagar, default=l["dagar"], key=f"dagar_{i}")
            onske = st.text_area("Önskemål", value=l["önskemål"], key=f"onske_{i}")
            col1, col2, col3 = st.columns(3)
            if col1.form_submit_button("📅 Spara"):
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

# --- Steg 3: Lokal timplan per årskurs ---
st.header("3. Lokal timplan (minuter/vecka per ämne och årskurs)")
with st.form("timplan_form"):
    for amne in amnen:
        st.markdown(f"**{amne}**")
        col7, col8, col9 = st.columns(3)
        with col7:
            st.session_state.timplan[amne]["7"] = col7.number_input(
                f"Åk 7", min_value=0, step=10,
                value=st.session_state.timplan[amne]["7"],
                key=f"timplan_{amne}_7"
            )
        with col8:
            st.session_state.timplan[amne]["8"] = col8.number_input(
                f"Åk 8", min_value=0, step=10,
                value=st.session_state.timplan[amne]["8"],
                key=f"timplan_{amne}_8"
            )
        with col9:
            st.session_state.timplan[amne]["9"] = col9.number_input(
                f"Åk 9", min_value=0, step=10,
                value=st.session_state.timplan[amne]["9"],
                key=f"timplan_{amne}_9"
            )
    if st.form_submit_button("📅 Spara timplan"):
        st.success("Timplan sparad!")

# --- Steg 4: Salar ---
st.header("4. Salar")
with st.form("sal_form", clear_on_submit=True):
    saltyp = st.radio("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], horizontal=True)
    namn = st.text_input("Salnamn")
    sal_klass = None
    sal_amne = None
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

st.subheader("📋 Inlagda salar")
for i, s in enumerate(st.session_state.salar):
    if st.session_state.red_salar == i:
        with st.form(f"edit_sal_{i}"):
            namn = st.text_input("Salnamn", s["sal"], key=f"sal_namn_{i}")
            saltyp = st.selectbox("Typ", ["Hemklassrum", "Ämnesklassrum"], index=["Hemklassrum", "Ämnesklassrum"].index(s["typ"]), key=f"typ_{i}")
            sal_klass = None
            sal_amne = None
            if saltyp == "Hemklassrum":
                sal_klass = st.selectbox("Tilldelad klass", klasser, index=klasser.index(s.get("klass", klasser[0])), key=f"klass_{i}")
            else:
                sal_amne = st.selectbox("Tilldelat ämne", amnen, index=amnen.index(s.get("ämne", amnen[0])), key=f"amne_{i}")
            col1, col2, col3 = st.columns(3)
            if col1.form_submit_button("📅 Spara"):
                st.session_state.salar[i] = {
                    "sal": namn,
                    "typ": saltyp,
                    "klass": sal_klass,
                    "ämne": sal_amne
                }
                st.session_state.red_salar = None
                rerun()
            if col2.form_submit_button("↩️ Avbryt"):
                st.session_state.red_salar = None
                rerun()
            if col3.form_submit_button("🚑 Ta bort"):
                st.session_state.salar.pop(i)
                st.session_state.red_salar = None
                rerun()
    else:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"**{s['sal']}** – {s['typ']} – {s.get('klass') or s.get('ämne')}")
        with col2:
            if st.button("✏️", key=f"edit_salar_{i}"):
                st.session_state.red_salar = i

# --- Steg 5: Inställningar för skoldagen ---
st.header("5. Inställningar för skoldagen")
with st.form("daginst_form"):
    starttid_str = st.text_input("Starttid (HH:MM)", value=st.session_state.daginst["starttid"].strftime("%H:%M"))
    sluttider = {}
    for dag in dagar:
        sluttider[dag] = st.text_input(f"Sluttid {dag} (HH:MM)", value=st.session_state.daginst["sluttider"][dag].strftime("%H:%M"))
    lunch = st.number_input("Lunchrastens längd (min)", min_value=20, max_value=60, value=st.session_state.daginst["lunch"])
    lek_min = st.number_input("Minsta lektionslängd (min)", min_value=30, max_value=60, value=st.session_state.daginst["lek_min"])
    lek_max = st.number_input("Största lektionslängd (min)", min_value=60, max_value=90, value=st.session_state.daginst["lek_max"])
    rast_min = st.number_input("Minsta rast (min)", min_value=5, max_value=15, value=st.session_state.daginst["rast_min"])
    rast_max = st.number_input("Största rast (min)", min_value=10, max_value=30, value=st.session_state.daginst["rast_max"])
    if st.form_submit_button("Spara inställningar"):
        try:
            start = datetime.datetime.strptime(starttid_str, "%H:%M").time()
            end_obj = {dag: datetime.datetime.strptime(t, "%H:%M").time() for dag, t in sluttider.items()}
            st.session_state.daginst = {
                "starttid": start,
                "sluttider": end_obj,
                "lunch": lunch,
                "lek_min": lek_min,
                "lek_max": lek_max,
                "rast_min": rast_min,
                "rast_max": rast_max
            }
            st.success("Inställningar sparade!")
        except:
            st.error("Felaktigt tidsformat. Använd HH:MM")

# --- Steg 6: Visuell schemavy med filter ---
st.header("6. Visuell schemavy")

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



