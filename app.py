import streamlit as st

# --- Initieringar ---
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# --- Session State Init ---
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}

if "larare" not in st.session_state:
    st.session_state.larare = []

if "red_larare" not in st.session_state:
    st.session_state.red_larare = None

if "salar" not in st.session_state:
    st.session_state.salar = []

if "red_salar" not in st.session_state:
    st.session_state.red_salar = None

st.title("Skolplanerare – Inputs (Steg 1–3)")

# --- Steg 1: Färgval för ämnen ---
st.header("1. Välj färg för varje ämne")
with st.form("farg_form"):
    for amne in amnen:
        st.session_state.farg_val[amne] = st.color_picker(f"{amne}", value=st.session_state.farg_val[amne], key=f"farg_{amne}")
    if st.form_submit_button("💾 Spara färger"):
        st.success("Färger sparade!")

# --- Steg 2: Lägg till/redigera lärare ---
st.header("2. Lärare")

if st.session_state.red_larare is None:
    with st.form("add_larare_form", clear_on_submit=True):
        larar_id = st.text_input("Lärar-ID")
        larar_amne = st.selectbox("Ämne", amnen)
        larar_tid = st.number_input("Minuter/vecka", min_value=10, step=10)
        larar_klasser = st.multiselect("Klasser", klasser)
        larar_dagar = st.multiselect("Arbetsdagar", dagar, default=dagar)
        larar_onskemal = st.text_area("Önskemål (valfritt)")
        if st.form_submit_button("➕ Lägg till lärare"):
            if larar_id and larar_klasser and larar_tid > 0:
                ny = {
                    "id": larar_id,
                    "ämne": larar_amne,
                    "minuter": larar_tid,
                    "klasser": larar_klasser,
                    "dagar": larar_dagar,
                    "önskemål": larar_onskemal.strip()
                }
                st.session_state.larare.append(ny)
                st.success(f"Lärare {larar_id} tillagd!")
else:
    index = st.session_state.red_larare
    larare = st.session_state.larare[index]
    with st.form("edit_larare_form"):
        id_edit = st.text_input("Lärar-ID", value=larare["id"])
        amne_edit = st.selectbox("Ämne", amnen, index=amnen.index(larare["ämne"]))
        min_edit = st.number_input("Minuter/vecka", value=larare["minuter"], min_value=10, step=10)
        klasser_edit = st.multiselect("Klasser", klasser, default=larare["klasser"])
        dagar_edit = st.multiselect("Arbetsdagar", dagar, default=larare["dagar"])
        onske_edit = st.text_area("Önskemål", value=larare["önskemål"])
        col1, col2 = st.columns(2)
        if col1.form_submit_button("💾 Spara ändringar"):
            st.session_state.larare[index] = {
                "id": id_edit,
                "ämne": amne_edit,
                "minuter": min_edit,
                "klasser": klasser_edit,
                "dagar": dagar_edit,
                "önskemål": onske_edit.strip()
            }
            st.session_state.red_larare = None
        if col2.form_submit_button("↩️ Avbryt"):
            st.session_state.red_larare = None

st.subheader("📋 Inlagda lärare")
for i, l in enumerate(st.session_state.larare):
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"- **{l['id']} ({l['ämne']})** – {l['minuter']} min/vecka – {', '.join(l['klasser'])}")
    with col2:
        if st.button("✏️", key=f"edit_larare_{i}"):
            st.session_state.red_larare = i
        if st.button("🗑️", key=f"delete_larare_{i}"):
            st.session_state.larare.pop(i)
            st.experimental_rerun()

# --- Steg 3: Salar ---
st.header("3. Salar")

if st.session_state.red_salar is None:
    with st.form("add_sal_form", clear_on_submit=True):
        typ = st.radio("Typ", ["Hemklassrum", "Ämnesklassrum"], horizontal=True)
        namn = st.text_input("Salnamn")
        if typ == "Hemklassrum":
            klass = st.selectbox("Tilldelad klass", klasser)
            amne = None
        else:
            amne = st.selectbox("Tilldelat ämne", amnen)
            klass = None
        if st.form_submit_button("➕ Lägg till sal"):
            st.session_state.salar.append({
                "sal": namn,
                "typ": typ,
                "klass": klass,
                "ämne": amne
            })
            st.success(f"Sal {namn} tillagd!")
else:
    i = st.session_state.red_salar
    sal = st.session_state.salar[i]
    with st.form("edit_sal_form"):
        namn_edit = st.text_input("Salnamn", value=sal["sal"])
        typ_edit = st.radio("Typ", ["Hemklassrum", "Ämnesklassrum"], index=0 if sal["typ"] == "Hemklassrum" else 1)
        if typ_edit == "Hemklassrum":
            klass_edit = st.selectbox("Tilldelad klass", klasser, index=klasser.index(sal["klass"]))
            amne_edit = None
        else:
            amne_edit = st.selectbox("Tilldelat ämne", amnen, index=amnen.index(sal["ämne"]))
            klass_edit = None
        col1, col2 = st.columns(2)
        if col1.form_submit_button("💾 Spara sal"):
            st.session_state.salar[i] = {
                "sal": namn_edit,
                "typ": typ_edit,
                "klass": klass_edit,
                "ämne": amne_edit
            }
            st.session_state.red_salar = None
        if col2.form_submit_button("↩️ Avbryt"):
            st.session_state.red_salar = None

st.subheader("📋 Inlagda salar")
for i, s in enumerate(st.session_state.salar):
    col1, col2 = st.columns([5, 1])
    with col1:
        info = f"{s['sal']} – {s['typ']}"
        if s["klass"]:
            info += f", klass: {s['klass']}"
        if s["ämne"]:
            info += f", ämne: {s['ämne']}"
        st.write(info)
    with col2:
        if st.button("✏️", key=f"edit_sal_{i}"):
            st.session_state.red_salar = i
        if st.button("🗑️", key=f"delete_sal_{i}"):
            st.session_state.salar.pop(i)
            st.experimental_rerun()
