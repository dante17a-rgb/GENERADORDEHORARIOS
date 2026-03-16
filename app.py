import streamlit as st
import subprocess

st.title("Generador de Horarios")

st.write("Presiona el botón para ejecutar el modelo")

if st.button("Run Model"):

    st.write("Ejecutando...")

    resultado = subprocess.run(
        ["python3", "generadordehorarios.py"],
        capture_output=True,
        text=True
    )

    st.subheader("Salida del programa")
    st.text(resultado.stdout)

    if resultado.stderr:
        st.subheader("Errores")
        st.text(resultado.stderr)
