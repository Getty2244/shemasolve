import streamlit as st

# --- Init ---
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# --- Session state ---
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}
if "farg_saved" not in st.session_state:
    st.session_state.farg_saved = False
if "larare" not in st.session_state:
    st.session_state.larare = []
if "red_larare" not in st.session_state:
    st.session_state.red_larare = None
if "salar" not in st.session_state:
    st.session_state.salar = []
if "red_salar" not in st.session_state:
    st.session_state.red_salar = None

st.title("Skolplanerare – Steg 1–3")

# --- Steg 1: Färgval ---
st.header("1. Färgval per ämne")
with st.form("farg_form"):
    cols = st.columns(3)
    for idx, amne in enumerate(amnen):
        with cols[idx % 3]:
            st.session_state.farg_val[amne] = st.color_picker(amne, value=st.session_state.farg_val[amne], key=f"farg_{amne}")
            if st.session_state.farg_saved:
                st.markdown("✔️")
    if st.form_submit_button("💾 Spara färger"):
        st.session_state.farg_saved = True
        st.success("Färger sparade!")

# --- Steg 2: Lärare ---
st.header("2. Lärare")

if st.session_state.red_larare is None:
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
else:
    i = st.session_state.red_larare
    l = st.session_state.larare[i]
    with st.form("edit_larare"):
        lid = st.text_input("Lärar-ID", l["id"])
        amne = st.selectbox("Ämne", amnen, index=amnen.index(l["ämne"]))
        minuter = st.number_input("Minuter/vecka", value=l["minuter"], min_value=10, step=10)
        kl = st.multiselect("Klasser", klasser, default=l["klasser"])
        dag = st.multiselect("Arbetsdagar", dagar, default=l["dagar"])
        onske = st.text_area("Önskemål", value=l["önskemål"])
        col1, col2 = st.columns(2)
        if col1.form_submit_button("💾 Spara ändringar"):
            st.session_state.larare[i] = {
                "id": lid,
                "ämne": amne,
                "minuter": minuter,
                "klasser": kl,
                "dagar": dag,
                "önskemål": onske.strip()
            }
            st.session_state.red_larare = None
        if col2.form_submit_button("↩️ Avbryt"):
            st.session_state.red_larare = None

st.subheader("📋 Inlagda lärare")
for i, l in enumerate(st.session_state.larare):
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"**{l['id']} ({l['ämne']})** – {l['minuter']} min – Klasser: {', '.join(l['klasser'])}")
    with col2:
        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("✏️", key=f"edit_larare_{i}"):
                st.session_state.red_larare = i
        with btn2:
            if st.button("🗑️", key=f"delete_larare_{i}"):
                st.session_state.larare.pop(i)
                st.experimental_rerun()

# --- Steg 3: Salar ---
st.header("3. Salar")

if st.session_state.red_salar is None:
    with st.form("add_sal", clear_on_submit=True):
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
    s = st.session_state.salar[i]
    with st.form("edit_sal"):
        namn = st.text_input("Salnamn", value=s["sal"])
        typ = st.radio("Typ", ["Hemklassrum", "Ämnesklassrum"], index=0 if s["typ"] == "Hemklassrum" else 1)
        if typ == "Hemklassrum":
            klass = st.selectbox("Tilldelad klass", klasser, index=klasser.index(s["klass"]))
            amne = None
        else:
            amne = st.selectbox("Tilldelat ämne", amnen, index=amnen.index(s["ämne"]))
            klass = None
        col1, col2 = st.columns(2)
        if col1.form_submit_button("💾 Spara sal"):
            st.session_state.salar[i] = {
                "sal": namn,
                "typ": typ,
                "klass": klass,
                "ämne": amne
            }
            st.session_state.red_salar = None
        if col2.form_submit_button("↩️ Avbryt"):
            st.session_state.red_salar = None

st.subheader("📋 Inlagda salar")
for i, s in enumerate(st.session_state.salar):
    col1, col2 = st.columns([6, 1])
    with col1:
        text = f"{s['sal']} – {s['typ']}"
        if s["klass"]:
            text += f", klass: {s['klass']}"
        if s["ämne"]:
            text += f", ämne: {s['ämne']}"
        st.write(text)
    with col2:
        b1, b2 = st.columns(2)
        with b1:
            if st.button("✏️", key=f"edit_sal_{i}"):
                st.session_state.red_salar = i
        with b2:
            if st.button("🗑️", key=f"delete_sal_{i}"):
                st.session_state.salar.pop(i)
                st.experimental_rerun()
