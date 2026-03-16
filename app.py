import streamlit as st
import generadordehorarios

st.title("Generador de Horarios")

if st.button("Run Model"):
    st.write("Ejecutando modelo...")
    generadordehorarios.main()
