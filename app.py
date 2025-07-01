import streamlit as st

# --- Init ---
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# --- Session state ---
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}
if "farg_saved_val" not in st.session_state:
    st.session_state.farg_saved_val = {amne: None for amne in amnen}
if "larare" not in st.session_state:
    st.session_state.larare = []
if "red_larare" not in st.session_state:
    st.session_state.red_larare = None
if "salar" not in st.session_state:
    st.session_state.salar = []
if "red_salar" not in st.session_state:
    st.session_state.red_salar = None
if "saltyp" not in st.session_state:
    st.session_state.saltyp = "Hemklassrum"

st.title("Skolplanerare – Steg 1–3")

# --- Steg 1: Färgval ---
st.header("1. Färgval per ämne")
with st.form("farg_form"):
    for amne in amnen:
        col1, col2 = st.columns([3, 1])
        with col1:
            ny_farg = st.color_picker(amne, value=st.session_state.farg_val[amne], key=f"farg_{amne}")
        with col2:
            if st.session_state.farg_saved_val[amne] and st.session_state.farg_saved_val[amne] != st.session_state.farg_val[amne]:
                st.markdown("✔️")
        st.session_state.farg_val[amne] = ny_farg
    if st.form_submit_button("💾 Spara färger"):
        for amne in amnen:
            st.session_state.farg_saved_val[amne] = st.session_state.farg_val[amne]
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
                st.experimental_rerun()
            if col2.form_submit_button("🗑️ Ta bort"):
                st.session_state.larare.pop(i)
                st.session_state.red_larare = None
                st.experimental_rerun()
    else:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"**{l['id']} ({l['ämne']})** – {l['minuter']} min – Klasser: {', '.join(l['klasser'])}")
        with col2:
            if st.button("✏️", key=f"edit_larare_{i}"):
                st.session_state.red_larare = i

# --- Steg 3: Salar ---
st.header("3. Salar")

# Dynamisk saltyp
st.radio("Typ av sal", ["Hemklassrum", "Ämnesklassrum"], horizontal=True, key="saltyp")

with st.form("add_sal", clear_on_submit=True):
    namn = st.text_input("Salnamn")
    if st.session_state.saltyp == "Hemklassrum":
        klass = st.selectbox("Tilldelad klass", klasser, key="klass_sal")
        amne = None
    else:
        amne = st.selectbox("Tilldelat ämne", amnen, key="amne_sal")
        klass = None
    if st.form_submit_button("➕ Lägg till sal"):
        st.session_state.salar.append({
            "sal": namn,
            "typ": st.session_state.saltyp,
            "klass": klass,
            "ämne": amne
        })
        st.success(f"Sal {namn} tillagd!")

st.subheader("📋 Inlagda salar")
for i, s in enumerate(st.session_state.salar):
    if st.session_state.red_salar == i:
        with st.form(f"edit_sal_{i}"):
            namn = st.text_input("Salnamn", value=s["sal"], key=f"sal_namn_{i}")
            typ = st.radio("Typ", ["Hemklassrum", "Ämnesklassrum"], index=0 if s["typ"] == "Hemklassrum" else 1, key=f"sal_typ_{i}")
            if typ == "Hemklassrum":
                klass = st.selectbox("Tilldelad klass", klasser, index=klasser.index(s["klass"]), key=f"sal_klass_{i}")
                amne = None
            else:
                amne = st.selectbox("Tilldelat ämne", amnen, index=amnen.index(s["ämne"]), key=f"sal_amne_{i}")
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
                st.experimental_rerun()
            if col2.form_submit_button("🗑️ Ta bort"):
                st.session_state.salar.pop(i)
                st.session_state.red_salar = None
                st.experimental_rerun()
    else:
        col1, col2 = st.columns([6, 1])
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
