import streamlit as st
import subprocess

st.title("Generador de Horarios")

if st.button("Run Model"):

    resultado = subprocess.run(
        ["python", "tu_archivo.py"],
        capture_output=True,
        text=True
    )

    st.text(resultado.stdout)
