# Förutsatt att df = st.session_state.generated_schema finns

if "generated_schema" in st.session_state:
    df = st.session_state.generated_schema

    col1, col2 = st.columns([2, 3])  # två kolumner bredvid varandra

    with col1:
        visningstyp = st.selectbox("Visa schema för:", ["Klass", "Lärare", "Sal"])

    with col2:
        if visningstyp == "Klass":
            val = st.selectbox("Välj klass:", sorted(df["klass"].unique()))
        elif visningstyp == "Lärare":
            val = st.selectbox("Välj lärare:", sorted(df["lärare"].unique()))
        else:
            val = st.selectbox("Välj sal:", sorted(df["sal"].unique()))

    # Filtrera data
    if visningstyp == "Klass":
        vis_df = df[df["klass"] == val]
    elif visningstyp == "Lärare":
        vis_df = df[df["lärare"] == val]
    else:
        vis_df = df[df["sal"] == val]

    if not vis_df.empty:
        st.dataframe(vis_df)
    else:
        st.info("Inget schema hittades för det valet.")
else:
    st.info("Generera schema först.")
