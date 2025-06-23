import streamlit as st

st.title("AI-schemaplanerare för skolan")

# Initiera session_state för lärare och salar om det inte finns
if 'lärare' not in st.session_state:
    st.session_state['lärare'] = []

if 'salar' not in st.session_state:
    st.session_state['salar'] = []

# Lärare - form
st.header("Lärare")
with st.form(key='teacher_form'):
    lärarid = st.text_input("LärarID")
    ämne = st.selectbox("Ämne", ["Svenska", "Engelska", "Matematik", "SO (inkl. Religion)", "NO", "Idrott", "Slöjd", "Hemkunskap", "Spanska", "Franska", "Tyska", "Bild", "Musik", "Teknik"])
    klasser = st.multiselect("Klasser", ["7a", "7b", "8a", "8b", "9a", "9b"])
    arbetsdagar = st.multiselect(
        "Arbetsdagar", 
        ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"], 
        default=["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]
    )
    submit_teacher = st.form_submit_button(label='Lägg till lärare')

if submit_teacher:
    ny_lärare = {
        'lärarid': lärarid,
        'ämne': ämne,
        'klasser': klasser,
        'arbetsdagar': arbetsdagar
    }
    st.session_state.lärare.append(ny_lärare)
    st.success(f"Lärare {lärarid} tillagd!")

# Visa alla lärare
if st.session_state.lärare:
    st.subheader("Alla lärare")
    for i, lärare in enumerate(st.session_state.lärare):
        st.write(f"{i+1}. ID: {lärare['lärarid']}, Ämne: {lärare['ämne']}, Klasser: {', '.join(lärare['klasser'])}, Arbetsdagar: {', '.join(lärare['arbetsdagar'])}")

# Salar - form
st.header("Salar")
with st.form(key='room_form'):
    sal_namn = st.text_input("Salens namn/nummer")
    sal_typ = st.selectbox("Typ av sal", ["Hemklassrum", "Ämnesklassrum"])
    submit_room = st.form_submit_button(label='Lägg till sal')

if submit_room:
    ny_sal = {
        'namn': sal_namn,
        'typ': sal_typ
    }
    st.session_state.salar.append(ny_sal)
    st.success(f"Sal {sal_namn} tillagd!")

# Visa alla salar
if st.session_state.salar:
    st.subheader("Alla salar")
    for i, sal in enumerate(st.session_state.salar):
        st.write(f"{i+1}. Sal: {sal['namn']}, Typ: {sal['typ']}")
