import streamlit as st
import pandas as pd
from collections import defaultdict

st.title("AI-schemaplanerare för skolan")

# Här kan du lägga till din inputkod senare (exempelvis formulär)

# Statisk exempeldata just nu
teachers = [
    {"id": "bgk1", "subject": "SO", "classes": ["7a", "8a", "9a"], "days": ["Mon", "Tue", "Wed", "Thu", "Fri"]},
    {"id": "bgk2", "subject": "MA", "classes": ["7a", "8a", "9a"], "days": ["Mon", "Tue", "Wed", "Thu", "Fri"]},
]

classes = ["7a", "8a", "9a"]
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
time_slots = ["08:30-09:15", "09:20-10:05", "10:10-10:55", "11:00-11:45", "12:25-13:10", "13:15-14:00", "14:05-14:50"]

schedule = defaultdict(lambda: {"rooms": set(), "teachers": set(), "classes": set()})

result = []

def plan_lessons():
    for teacher in teachers:
        for cls in teacher["classes"]:
            lektioner_per_klass = 2
            booked = 0
            for day in teacher["days"]:
                if booked >= lektioner_per_klass:
                    break
                for slot in time_slots:
                    if (cls not in schedule[(day, slot)]["classes"] and
                        teacher["id"] not in schedule[(day, slot)]["teachers"]):
                        schedule[(day, slot)]["teachers"].add(teacher["id"])
                        schedule[(day, slot)]["classes"].add(cls)
                        result.append({
                            "Dag": day,
                            "Tid": slot,
                            "Klass": cls,
                            "Lärare": teacher["id"],
                            "Ämne": teacher["subject"]
                        })
                        booked += 1
                        break

plan_lessons()

df = pd.DataFrame(result)
st.write("Schema:")
st.dataframe(df)
