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
        st.header("Tider och raster")

with st.form(key='time_form'):
    starttid = st.time_input("Skoldagens starttid", value=datetime.time(8,30))
    sluttid = st.time_input("Skoldagens sluttid", value=datetime.time(15,0))

    rast_min = st.number_input("Rastlängd min (minuter)", min_value=1, max_value=30, value=5)
    rast_max = st.number_input("Rastlängd max (minuter)", min_value=rast_min, max_value=30, value=10)

    lunch_start = st.time_input("Lunchrast starttid", value=datetime.time(11,40))
    lunch_längd = st.number_input("Lunchrast längd (minuter)", min_value=20, max_value=60, value=40)

    lektion_min = st.number_input("Minsta lektionstid (minuter)", min_value=20, max_value=60, value=40)
    lektion_max = st.number_input("Största lektionstid (minuter)", min_value=lektion_min, max_value=90, value=60)

    submit_time = st.form_submit_button(label='Spara tider')

if submit_time:
    st.session_state['tider'] = {
        'starttid': starttid,
        'sluttid': sluttid,
        'rast_min': rast_min,
        'rast_max': rast_max,
        'lunch_start': lunch_start,
        'lunch_längd': lunch_längd,
        'lektion_min': lektion_min,
        'lektion_max': lektion_max
    }
    st.success("Tider och raster sparade!")

if 'tider' in st.session_state:
    tider = st.session_state['tider']
    st.write(f"Skoldag: {tider['starttid'].strftime('%H:%M')} - {tider['sluttid'].strftime('%H:%M')}")
    st.write(f"Rastlängd: {tider['rast_min']} - {tider['rast_max']} minuter")
    st.write(f"Lunchrast: Start {tider['lunch_start'].strftime('%H:%M')}, Längd {tider['lunch_längd']} minuter")
    st.write(f"Lektionstid: {tider['lektion_min']} - {tider['lektion_max']} minuter")
