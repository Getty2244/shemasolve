import streamlit as st
import pandas as pd
import datetime
from streamlit.runtime.scriptrunner.script_runner import RerunException, RerunData

def rerun():
    raise RerunException(RerunData())

# === ÄMNEN OCH KLASSER ===
amnen = ["SO", "MA", "NO", "SV", "ENG", "IDROTT", "TRÄSLÖJD", "SY", "HK"]
klasser = ["7a", "7b", "8a", "8b", "9a", "9b"]
dagar_val = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Initiera session_state-variabler för lärareinput
if "input_larar_id" not in st.session_state:
    st.session_state.input_larar_id = ""
if "input_amne" not in st.session_state:
    st.session_state.input_amne = amnen[0]
if "input_undervisningstid" not in st.session_state:
    st.session_state.input_undervisningstid = 0
if "input_larar_klasser" not in st.session_state:
    st.session_state.input_larar_klasser = []
if "input_arbetsdagar" not in st.session_state:
    st.session_state.input_arbetsdagar = dagar_val
if "input_onskemal" not in st.session_state:
    st.session_state.input_onskemal = ""

# Initiera session_state-variabler för salinput
if "input_sal_namn" not in st.session_state:
    st.session_state.input_sal_namn = ""
if "input_sal_klass" not in st.session_state:
    st.session_state.input_sal_klass = klasser[0]
if "input_sal_amne" not in st.session_state:
    st.session_state.input_sal_amne = amnen[0]

st.title("AI-schemaplanerare för skolan")

# === 1. FÄRGVAL FÖR ÄMNEN ===
if "temp_farg_val" not in st.session_state:
    st.session_state.temp_farg_val = {amne: "#FFFFFF" for amne in amnen}
if "farg_val" not in st.session_state:
    st.session_state.farg_val = {amne: "#FFFFFF" for amne in amnen}

st.header("1. Färgval för ämnen")
for amne in amnen:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state.temp_farg_val[amne] = st.color_picker(f"{amne}", st.session_state.temp_farg_val[amne], key=f"farg_{amne}")
    with col2:
        st.write(st.session_state.temp_farg_val[amne])

if st.button("Spara färger", key="spara_farger_knapp"):
    st.session_state.farg_val = st.session_state.temp_farg_val.copy()
    st.success("Färger sparade!")

# === 2. LÄGG TILL LÄRARE ===
st.header("2. Lägg till lärare")
with st.form("larare_form"):
    larar_id = st.text_input("Lärar-ID (ex: bgk1)", key="input_larar_id")
    amne = st.selectbox("Ämne", options=amnen, key="input_amne")
    undervisningstid = st.number_input("Undervisningsminuter per vecka", min_value=0, step=10, key="input_undervisningstid")
    larar_klasser = st.multiselect("Undervisar i klasser", options=klasser, key="input_larar_klasser")
    arbetsdagar = st.multiselect("Arbetsdagar", options=dagar_val, default=dagar_val, key="input_arbetsdagar")
    onskemal = st.text_area("Extra önskemål (valfritt)", key="input_onskemal")

    with st.expander("ℹ️ Se exempel på vanliga önskemål"):
        st.markdown("""
        **Exempel på extra önskemål:**
        - Undvik SO på måndagar  
        - Idrott helst efter lunch  
        - NO bör ej ligga första lektionen  
        - Engelska i följd om möjligt  
        - Fredagar helst undervisningsfri  
        - Matte inte alla dagar i rad  
        - Slöjd ska ej vara efter idrott  
        - Mentorstid varje tisdag 10:00
        """)

    skicka = st.form_submit_button("Lägg till lärare")

if skicka:
    if (st.session_state.input_larar_id and st.session_state.input_amne and
        st.session_state.input_larar_klasser and st.session_state.input_arbetsdagar and
        st.session_state.input_undervisningstid > 0):

        ny_larare = {
            "id": st.session_state.input_larar_id,
            "ämne": st.session_state.input_amne,
            "klasser": st.session_state.input_larar_klasser,
            "dagar": st.session_state.input_arbetsdagar,
            "minuter_per_vecka": st.session_state.input_undervisningstid,
            "önskemål": st.session_state.input_onskemal or ""
        }
        if "larare_data" not in st.session_state:
            st.session_state.larare_data = []
        st.session_state.larare_data.append(ny_larare)
        st.success(f"Lärare {st.session_state.input_larar_id} tillagd!")

        # Rensa inputfält
        st.session_state.input_larar_id = ""
        st.session_state.input_amne = amnen[0]
        st.session_state.input_undervisningstid = 0
        st.session_state.input_larar_klasser = []
        st.session_state.input_arbetsdagar = dagar_val
        st.session_state.input_onskemal = ""

        rerun()

# Visa/redigera lärare
st.subheader("📋 Inlagda lärare")
if "larare_data" not in st.session_state or not st.session_state.larare_data:
    st.info("Inga lärare inlagda ännu.")
else:
    if "redigera_larare_index" not in st.session_state:
        st.session_state.redigera_larare_index = None

    for i, larare in enumerate(st.session_state.larare_data):
        if st.session_state.redigera_larare_index == i:
            st.write(f"✏️ Redigerar lärare **{larare['id']}**")
            nytt_id = st.text_input("Lärar-ID", value=larare["id"], key=f"edit_id_{i}")
            nytt_amne = st.selectbox("Ämne", options=amnen, index=amnen.index(larare["ämne"]), key=f"edit_amne_{i}")
            nya_klasser = st.multiselect("Klasser", options=klasser, default=larare["klasser"], key=f"edit_klass_{i}")
            nya_dagar = st.multiselect("Arbetsdagar", options=dagar_val, default=larare["dagar"], key=f"edit_dagar_{i}")
            nya_minuter = st.number_input("Undervisningsminuter/vecka", value=larare["minuter_per_vecka"], min_value=0, step=10, key=f"edit_min_{i}")
            nya_onskemal = st.text_area("Extra önskemål", value=larare.get("önskemål", ""), key=f"edit_onskemal_{i}")

            if st.button("💾 Spara", key=f"spara_larare_{i}"):
                st.session_state.larare_data[i] = {
                    "id": nytt_id,
                    "ämne": nytt_amne,
                    "klasser": nya_klasser,
                    "dagar": nya_dagar,
                    "minuter_per_vecka": nya_minuter,
                    "önskemål": nya_onskemal
                }
                st.session_state.redigera_larare_index = None
                rerun()

            if st.button("❌ Ta bort", key=f"ta_bort_larare_{i}"):
                st.session_state.larare_data.pop(i)
                st.session_state.redigera_larare_index = None
                rerun()

            if st.button("Avbryt", key=f"avbryt_larare_{i}"):
                st.session_state.redigera_larare_index = None
                rerun()
        else:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"""
                - **{larare['id']}** ({larare['ämne']})  
                  Klasser: {', '.join(larare['klasser'])}  
                  Dagar: {', '.join(larare['dagar'])}  
                  Minuter/vecka: {larare['minuter_per_vecka']}  
                  Önskemål: _{larare.get('önskemål', '')}_  
                """)
            with col2:
                if st.button("✏️ Redigera", key=f"redigera_larare_{i}"):
                    st.session_state.redigera_larare_index = i
                    rerun()

# === 3. LÄGG TILL SAL ===
st.header("3. Lägg till sal")

sal_typ = st.radio("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], horizontal=True, key="sal_typ")

with st.form("sal_form"):
    sal_namn = st.text_input("Salnamn (t.ex. A101, NO-labb)", key="input_sal_namn")
    sal_klass = None
    sal_amne = None

    if sal_typ == "Hemklassrum":
        sal_klass = st.selectbox("Tilldelad klass", options=klasser, key="input_sal_klass")
    else:
        sal_amne = st.selectbox("Tilldelat ämne", options=amnen, key="input_sal_amne")

    sal_submit = st.form_submit_button("Lägg till sal")

if "sal_data" not in st.session_state:
    st.session_state.sal_data = []

if sal_submit and st.session_state.input_sal_namn:
    ny_sal = {
        "sal": st.session_state.input_sal_namn,
        "typ": sal_typ,
        "klass": st.session_state.input_sal_klass if sal_typ == "Hemklassrum" else None,
        "ämne": st.session_state.input_sal_amne if sal_typ == "Ämnesklassrum" else None
    }
    st.session_state.sal_data.append(ny_sal)
    st.success(f"Sal {st.session_state.input_sal_namn} tillagd!")

    # Rensa sal-formulär
    st.session_state.input_sal_namn = ""
    if sal_typ == "Hemklassrum":
        st.session_state.input_sal_klass = klasser[0]
    else:
        st.session_state.input_sal_amne = amnen[0]
    rerun()

# Visa/redigera salar
st.subheader("📋 Inlagda salar")
if "sal_data" not in st.session_state or not st.session_state.sal_data:
    st.info("Inga salar inlagda ännu.")
else:
    if "redigera_sal_index" not in st.session_state:
        st.session_state.redigera_sal_index = None

    for i, sal in enumerate(st.session_state.sal_data):
        if st.session_state.redigera_sal_index == i:
            st.write(f"✏️ Redigerar sal **{sal['sal']}**")
            nytt_namn = st.text_input("Salnamn", value=sal["sal"], key=f"edit_sal_namn_{i}")
            ny_typ = st.selectbox("Typ av sal", options=["Hemklassrum", "Ämnesklassrum"], index=["Hemklassrum", "Ämnesklassrum"].index(sal["typ"]), key=f"edit_sal_typ_{i}")

            ny_klass = None
            ny_amne = None
            if ny_typ == "Hemklassrum":
                ny_klass = st.selectbox("Tilldelad klass", options=klasser, index=klasser.index(sal["klass"]) if sal["klass"] else 0, key=f"edit_klass_{i}")
            else:
                ny_amne = st.selectbox("Tilldelat ämne", options=amnen, index=amnen.index(sal["ämne"]) if sal["ämne"] else 0, key=f"edit_amne_{i}")

            if st.button("💾 Spara sal", key=f"spara_sal_{i}"):
                st.session_state.sal_data[i] = {
                    "sal": nytt_namn,
                    "typ": ny_typ,
                    "klass": ny_klass if ny_typ == "Hemklassrum" else None,
                    "ämne": ny_amne if ny_typ == "Ämnesklassrum" else None
                }
                st.session_state.redigera_sal_index = None
                rerun()

            if st.button("❌ Ta bort", key=f"ta_bort_sal_{i}"):
                st.session_state.sal_data.pop(i)
                st.session_state.redigera_sal_index = None
                rerun()

            if st.button("Avbryt", key=f"avbryt_sal_{i}"):
                st.session_state.redigera_sal_index = None
                rerun()
        else:
            col1, col2 = st.columns([5, 1])
            with col1:
                info = f"{sal['sal']} – {sal['typ']}"
                if sal["klass"]:
                    info += f", klass: {sal['klass']}"
                if sal["ämne"]:
                    info += f", ämne: {sal['ämne']}"
                st.write(info)
            with col2:
                if st.button("✏️ Redigera", key=f"redigera_sal_{i}"):
                    st.session_state.redigera_sal_index = i
                    rerun()

# === 4. Inställningar för skoldagen ===
st.header("4. Inställningar för skoldagen")

with st.form("form_skoldag_tider"):
    starttid_str = st.text_input("Skoldagens starttid (HH:MM)", value="08:30", key="input_starttid")
    sluttider = {}
    for dag in dagar_val:
        sluttider[dag] = st.text_input(f"Sluttid för {dag} (HH:MM)", value="15:00", key=f"input_sluttid_{dag}")
    lunchmin = st.number_input("Lunchrastens längd (min)", min_value=20, max_value=60, value=40, key="input_lunchmin")
    lek_min = st.number_input("Minsta lektionslängd (min)", min_value=30, max_value=60, value=40, key="input_lek_min")
    lek_max = st.number_input("Max lektionslängd (min)", min_value=60, max_value=90, value=60, key="input_lek_max")
    rast_min = st.number_input("Minsta rast (min)", min_value=5, max_value=15, value=5, key="input_rast_min")
    rast_max = st.number_input("Största rast (min)", min_value=10, max_value=30, value=15, key="input_rast_max")

    spara_tid = st.form_submit_button("Spara inställningar")

if spara_tid:
    try:
        starttid = datetime.datetime.strptime(st.session_state.input_starttid, "%H:%M").time()
        sluttider_obj = {dag: datetime.datetime.strptime(st.session_state[f"input_sluttid_{dag}"], "%H:%M").time() for dag in dagar_val}
        st.session_state.daginst = {
            "starttid": starttid,
            "sluttider": sluttider_obj,
            "lunch": st.session_state.input_lunchmin,
            "lek_min": st.session_state.input_lek_min,
            "lek_max": st.session_state.input_lek_max,
            "rast_min": st.session_state.input_rast_min,
            "rast_max": st.session_state.input_rast_max
        }
        st.success("Skoldagens inställningar sparade!")
    except ValueError:
        st.error("Felaktigt tidsformat. Använd HH:MM")

# === 5. Schemagenereringsfunktion ===
def intelligent_generate_schedule(session_state):
    import random

    if not ("daginst" in session_state and session_state.get("larare_data") and session_state.get("sal_data")):
        return None

    daginst = session_state["daginst"]
    starttid = datetime.datetime.combine(datetime.date.today(), daginst["starttid"])
    sluttider = {dag: datetime.datetime.combine(datetime.date.today(), t) for dag, t in daginst["sluttider"].items()}
    lek_min = daginst["lek_min"]
    rast_min = daginst["rast_min"]

    schema = []
    bokningar_klass = {}
    bokningar_larare = {}
    bokningar_sal = {}

    dagar_val = list(sluttider.keys())

    lektioner_per_amne_per_dag = {amne: {dag: 0 for dag in dagar_val} for amne in amnen}
    lektioner_per_klass_per_dag = {klass: {dag: 0 for dag in dagar_val} for klass in klasser}
    max_pass_per_dag = 4

    starttider_per_dag = [
        datetime.timedelta(hours=8, minutes=30),
        datetime.timedelta(hours=9, minutes=30),
        datetime.timedelta(hours=10, minutes=40),
        datetime.timedelta(hours=11, minutes=40),
        datetime.timedelta(hours=13, minutes=0),
        datetime.timedelta(hours=14, minutes=0),
        datetime.timedelta(hours=15, minutes=0),
    ]

    lunch_start = datetime.timedelta(hours=12, minutes=30)
    lunch_slut = datetime.timedelta(hours=13, minutes=0)

    def tid_är_lunch(tid):
        return lunch_start <= tid < lunch_slut

    def ledigt(dag, start, slut, klass, larare, sal):
        for tid in bokningar_klass.get((dag, klass), []):
            if not (slut <= tid[0] or start >= tid[1]):
                return False
        for tid in bokningar_larare.get((dag, larare), []):
            if not (slut <= tid[0] or start >= tid[1]):
                return False
        for tid in bokningar_sal.get((dag, sal), []):
            if not (slut <= tid[0] or start >= tid[1]):
                return False
        return True

    def boka(dag, start, slut, klass, larare, sal):
        bokningar_klass.setdefault((dag, klass), []).append((start, slut))
        bokningar_larare.setdefault((dag, larare), []).append((start, slut))
        bokningar_sal.setdefault((dag, sal), []).append((start, slut))

    def önskemål_till_placering(ämne, önskemål):
        önsk = önskemål.lower()
        if "idrott efter lunch" in önsk and ämne.lower() == "idrott":
            return "efter_lunch"
        if "undvik måndag" in önsk:
            return "inte_måndag"
        return "ingen_spec"

    for larare in session_state["larare_data"]:
        kvar_minuter = larare["minuter_per_vecka"]
        larar_id = larare["id"]
        amne = larare["ämne"]
        klasser_larar = larare["klasser"]
        dagar = larare["dagar"]
        onskemal = larare.get("önskemål", "")

        placering_typ = önskemål_till_placering(amne, onskemal)

        def hitta_sal(klass):
            for sal in session_state["sal_data"]:
                if sal["typ"] == "Ämnesklassrum" and sal["ämne"] == amne:
                    return sal["sal"]
            for sal in session_state["sal_data"]:
                if sal["typ"] == "Hemklassrum" and sal.get("klass") == klass:
                    return sal["sal"]
            return None

        while kvar_minuter >= lek_min:
            möjliga_dagar = [d for d in dagar if lektioner_per_klass_per_dag[klass][d] < max_pass_per_dag]
            if placering_typ == "inte_måndag":
                möjliga_dagar = [d for d in möjliga_dagar if d != "Mon"]
            if not möjliga_dagar:
                break

            dag = min(möjliga_dagar, key=lambda d: lektioner_per_amne_per_dag[amne][d])
            schema_lagd = False

            for klass in klasser_larar:
                for tid_delta in starttider_per_dag:
                    if tid_är_lunch(tid_delta):
                        continue

                    tid = starttid + tid_delta
                    slut = tid + datetime.timedelta(minutes=lek_min)

                    sal = hitta_sal(klass)
                    if sal is None:
                        continue

                    if lektioner_per_klass_per_dag[klass][dag] >= max_pass_per_dag:
                        continue

                    if ledigt(dag, tid, slut, klass, larar_id, sal):
                        boka(dag, tid, slut, klass, larar_id, sal)
                        schema.append({
                            "dag": dag,
                            "start": tid.strftime("%H:%M"),
                            "slut": slut.strftime("%H:%M"),
                            "klass": klass,
                            "ämne": amne,
                            "lärare": larar_id,
                            "sal": sal
                        })
                        lektioner_per_klass_per_dag[klass][dag] += 1
                        lektioner_per_amne_per_dag[amne][dag] += 1
                        kvar_minuter -= lek_min
                        schema_lagd = True
                        break
                if schema_lagd:
                    break

            if not schema_lagd:
                break

    return schema

# === 6. Schemagenerering & visning ===
st.header("5. Schemagenering – komplett schema")

if st.button("Generera komplett schema"):
    nytt_schema = intelligent_generate_schedule(st.session_state)
    if nytt_schema:
        st.session_state.generated_schema = pd.DataFrame(nytt_schema)
        st.success("Schema genererat!")
    else:
        st.error("Fyll i alla nödvändiga data först (lärare, salar, tider).")

if "generated_schema" in st.session_state:
    df = st.session_state.generated_schema

    col1, col2 = st.columns([1, 2])

    with col1:
        visningstyp = st.selectbox("Visa schema för:", ["Klass", "Lärare", "Sal"])

    with col2:
        if visningstyp == "Klass":
            val = st.selectbox("Välj klass:", options=sorted(df["klass"].unique()))
        elif visningstyp == "Lärare":
            val = st.selectbox("Välj lärare:", options=sorted(df["lärare"].unique()))
        else:
            val = st.selectbox("Välj sal:", options=sorted(df["sal"].unique()))

    if visningstyp == "Klass":
        vis_df = df[df["klass"] == val]
    elif visningstyp == "Lärare":
        vis_df = df[df["lärare"] == val]
    else:
        vis_df = df[df["sal"] == val]

    if not vis_df.empty:
        vis_df = vis_df.sort_values(by=["dag", "start"])

        def färgkod_amne(row):
            färger = st.session_state.farg_val
            färg = färger.get(row["ämne"], "#FFFFFF")
            return [f"background-color: {färg}" if col == "ämne" else "" for col in row.index]

        st.dataframe(vis_df.style.apply(färgkod_amne, axis=1), height=400)
    else:
        st.info("Inget schema hittades för det valet.")
else:
    st.info("Generera schema först.")
