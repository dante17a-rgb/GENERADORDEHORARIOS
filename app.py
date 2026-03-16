import streamlit as st
import pandas as pd
import itertools
from io import BytesIO

dias = ["lu","ma","mi","ju","vi","sa"]
horas = list(range(8,20))
letras = ["A","B","C","D","E","F"]

st.title("Generador de Horarios Universitarios")

# -----------------------------
# ESTADOS
# -----------------------------

if "inicio" not in st.session_state:
    st.session_state.inicio = False

if "n_cursos" not in st.session_state:
    st.session_state.n_cursos = None

# -----------------------------
# PANTALLA INICIAL
# -----------------------------

if not st.session_state.inicio:

    if st.button("Inicio"):
        st.session_state.inicio = True
        st.rerun()

# -----------------------------
# PEDIR NUMERO DE CURSOS
# -----------------------------

elif st.session_state.n_cursos is None:

    n = st.number_input("Numero de cursos",1,10,1)

    if st.button("Continuar"):
        st.session_state.n_cursos = n
        st.rerun()

# -----------------------------
# RESTO DEL PROGRAMA
# -----------------------------

else:

    n = st.session_state.n_cursos

    st.subheader("Configuracion de cruces")

    MAX_TT = st.number_input("Horas cruce teoria-teoria (max 4)",0,4,0)
    MAX_TP = st.number_input("Horas cruce teoria-practica (max 2)",0,2,0)

    cursos = []

    for i in range(n):

        st.subheader(f"Curso {i+1}")

        nombre = st.text_input(f"Nombre curso {i+1}")

        dias_teoria = st.number_input(
            f"Dias teoria curso {i+1}",
            1,5,1,
            key=f"dt{i}"
        )

        secciones = st.number_input(
            f"Numero de secciones curso {i+1}",
            1,6,1,
            key=f"sec{i}"
        )

        lista_secciones = []

        for s in range(secciones):

            letra = letras[s]
            st.write(f"Seccion {letra}")

            teorias = []

            for t in range(dias_teoria):

                d = st.selectbox(
                    f"Dia teoria {t+1}",
                    dias,
                    key=f"d{i}{s}{t}"
                )

                i_h = st.number_input(
                    f"Hora inicio teoria {t+1}",
                    8,19,
                    key=f"hi{i}{s}{t}"
                )

                f_h = st.number_input(
                    f"Hora fin teoria {t+1}",
                    9,20,
                    key=f"hf{i}{s}{t}"
                )

                teorias.append((d,i_h,f_h))

            d = st.selectbox(
                "Dia practica",
                dias,
                key=f"dp{i}{s}"
            )

            i_h = st.number_input(
                "Hora inicio practica",
                8,19,
                key=f"hip{i}{s}"
            )

            f_h = st.number_input(
                "Hora fin practica",
                9,20,
                key=f"hfp{i}{s}"
            )

            practica = (d,i_h,f_h)

            lista_secciones.append({
                "curso":nombre,
                "sec":letra,
                "teorias":teorias,
                "practica":practica
            })

        cursos.append(lista_secciones)

    # -----------------------------
    # VALIDAR
    # -----------------------------

    def validar(comb):

        horario = {h:{d:[] for d in dias} for h in horas}

        TT = 0
        TP = 0

        for sec in comb:

            for (d,i,f) in sec["teorias"]:
                for h in range(i,f):
                    horario[h][d].append(("T",sec["curso"],sec["sec"]))

            (d,i,f) = sec["practica"]

            for h in range(i,f):
                horario[h][d].append(("P",sec["curso"],sec["sec"]))

        for h in horas:
            for d in dias:

                celda = horario[h][d]

                if len(celda) <= 1:
                    continue

                tipos = [x[0] for x in celda]

                if tipos.count("P") > 1:
                    return None

                if tipos.count("T") > 1:
                    TT += 1

                if "T" in tipos and "P" in tipos:
                    TP += 1

                if TT > MAX_TT or TP > MAX_TP:
                    return None

        return horario

    # -----------------------------
    # GENERAR
    # -----------------------------

    if st.button("Generar horarios"):

        horarios_validos = []
        contador = 0

        for comb in itertools.product(*cursos):

            h = validar(comb)

            if not h:
                continue

            contador += 1
            horarios_validos.append(h)

            tabla = []

            for hr in horas:

                fila = []

                for d in dias:

                    celda = h[hr][d]

                    if celda:
                        texto = " / ".join([f"{c}-{s}-{t}" for t,c,s in celda])
                    else:
                        texto = ""

                    fila.append(texto)

                tabla.append(fila)

            df = pd.DataFrame(tabla,columns=dias)
            df.index = [f"{h}:00-{h+1}:00" for h in horas]

            st.subheader(f"Horario {contador}")
            st.dataframe(df)

        st.success(f"Total horarios validos: {contador}")
