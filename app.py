import streamlit as st
import pandas as pd

# Exempeldata (din schemalista)
data = [
    ["Mon", "08:30-09:15", "7a", "bgk1", "SO"],
    ["Tue", "08:30-09:15", "7a", "bgk1", "SO"],
    ["Mon", "09:20-10:05", "8a", "bgk1", "SO"],
    ["Tue", "09:20-10:05", "8a", "bgk1", "SO"],
    ["Mon", "10:10-10:55", "9a", "bgk1", "SO"],
    ["Tue", "10:10-10:55", "9a", "bgk1", "SO"],
    ["Mon", "09:20-10:05", "7a", "bgk2", "MA"],
    ["Tue", "09:20-10:05", "7a", "bgk2", "MA"],
    ["Mon", "08:30-09:15", "8a", "bgk2", "MA"],
    ["Tue", "08:30-09:15", "8a", "bgk2", "MA"],
    ["Mon", "11:00-11:45", "9a", "bgk2", "MA"],
    ["Tue", "11:00-11:45", "9a", "bgk2", "MA"],
]

df = pd.DataFrame(data, columns=["Dag", "Tid", "Klass", "Lärare", "Ämne"])

# Skapa en "cell" med ämne + klass + lärare
df["Info"] = df.apply(lambda r: f"{r['Ämne']} {r['Klass']} ({r['Lärare']})", axis=1)

# Gör en pivottabell: rader = Tid, kolumner = Dag, värde = Info
pivot = df.pivot(index="Tid", columns="Dag", values="Info")

# Byt ordning på dagarna så det blir måndag-fredag (de dagar som finns)
order = ["Mon", "Tue", "Wed", "Thu", "Fri"]
pivot = pivot.reindex(columns=order)

st.write("### Schema (dagar som kolumner, tider som rader)")
st.dataframe(pivot.fillna(""))  # Fyll tomma celler med tomt sträng
