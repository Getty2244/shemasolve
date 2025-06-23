import streamlit as st

st.title("AI-schemaplanerare för skolan")

st.write("Ladda upp lärardata, salar, lektionslängder och önskemål.")
st.write("Detta är en plats för din schemagenerator.")

st.header("Lärare")
with st.form(key='teacher_form'):
    namn = st.text_input("Lärarens namn")
    ämne = st.selectbox("Ämne", ["Svenska", "Engelska", "Matematik", "SO", "NO", "Idrott", "Slöjd", "Hemkunskap"])
    klasser = st.multiselect("Klasser", ["7a", "7b", "8a", "8b", "9a", "9b"])
    arbetsdagar = st.multiselect(
        "Arbetsdagar", 
        ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"], 
        default=["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]
    )

    submit_button = st.form_submit_button(label='Lägg till lärare')

if submit_button:
    st.write(f"Lärare: {namn}, Ämne: {ämne}, Klasser: {klasser}, Arbetsdagar: {arbetsdagar}")
