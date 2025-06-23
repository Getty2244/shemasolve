import streamlit as st

st.title("AI-schemaplanerare för skolan")

st.write("Ladda upp lärardata, salar, lektionslängder och önskemål.")
st.write("Detta är en plats för din schemagenerator.")

ämnen = [
    "Svenska",
    "Engelska",
    "Matematik",
    "SO (inkl. Religion)",
    "NO",
    "Idrott",
    "Slöjd",
    "Hemkunskap",
    "Spanska",
    "Franska",
    "Tyska",
    "Bild",
    "Musik",
    "Teknik"
]

st.header("Lärare")
with st.form(key='teacher_form'):
    lärarid = st.text_input("LärarID")
    ämne = st.selectbox("Ämne", ämnen)
    klasser = st.multiselect("Klasser", ["7a", "7b", "8a", "8b", "9a", "9b"])
    arbetsdagar = st.multiselect(
        "Arbetsdagar", 
        ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"], 
        default=["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]
    )

    submit_button = st.form_submit_button(label='Lägg till lärare')

if submit_button:
    st.write(f"LärarID: {lärarid}, Ämne: {ämne}, Klasser: {klasser}, Arbetsdagar: {arbetsdagar}")
# Salar - form
st.header("Salar")
with st.form(key='room_form'):
    sal_namn = st.text_input("Salens namn/nummer")
    sal_typ = st.selectbox("Typ av sal", ["Hemklassrum", "Ämnesklassrum"])
    special_utrustning = st.text_input("Specialutrustning (om någon) - t.ex. labb, datorer")
    submit_room = st.form_submit_button(label='Lägg till sal')

if submit_room:
    st.write(f"Sal: {sal_namn}, Typ: {sal_typ}, Utrustning: {special_utrustning}")
