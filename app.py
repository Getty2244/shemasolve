import streamlit as st
import datetime

st.title("AI-schemaplanerare för skolan")

st.write("Ladda upp lärardata, salar, lektionslängder och önskemål.")
st.write("Detta är en plats för din schemagenerator.")

# --- Lärare input (exempel) ---
st.header("Lärare och ämnen")

with st.form(key='teacher_form'):
    lärare_id = st.text_input("Lärar-ID (ex. bgk01)")
    ämne = st.selectbox("Ämne", ["Svenska", "Engelska", "Matematik", "NO", "SO", "Idrott", "Slöjd", "Hemkunskap"])
    klasser = st.multiselect("Klasser de undervisar", ["7a", "7b", "8a", "8b", "9a", "9b"])
    arbetsdagar = st.multiselect("Arbetsdagar", ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"])
    submit_teacher = st.form_submit_button("Spara lärare")

if submit_teacher:
    if 'lärare' not in st.session_state:
        st.session_state['lärare'] = []
    st.session_state['lärare'].append({
        "id": lärare_id,
        "ämne": ämne,
        "klasser": klasser,
        "arbetsdagar": arbetsdagar
    })
    st.success(f"Lärare {lärare_id} sparad!")

if 'lärare' in st.session_state:
    st.write("Sparade lärare:")
    st.write(st.session_state['lärare'])

# --- Salar input (exempel) ---
st.header("Salar")

with st.form(key='rooms_form'):
    sal_namn = st.text_input("Salsnamn eller nummer")
    sal_typ = st.selectbox("Typ av sal", ["Hemklassrum", "Ämnesklassrum"])
    submit_room = st.form_submit_button("Spara sal")

if submit_room:
    if 'salar' not in st.session_state:
        st.session_state['salar'] = []
    st.session_state['salar'].append({
        "namn": sal_namn,
        "typ": sal_typ
    })
    st.success(f"Sal {sal_namn} sparad!")

if 'salar' in st.session_state:
    st.write("Sparade salar:")
    st.write(st.session_state['salar'])

# --- Tider och raster ---
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
