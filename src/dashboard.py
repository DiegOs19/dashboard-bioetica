import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------
# MÁXIMOS POR DOMINIO
# ----------------------------------

MAX_INTEGRACION = 15
MAX_RECURSOS = 5
MAX_PROCEDIMENTAL = 7
MAX_OPERATIVIDAD = 16
MAX_TOTAL = 43

# ----------------------------------
# CONFIGURACIÓN
# ----------------------------------

st.set_page_config(
    page_title="Dashboard Bioética",
    layout="wide"
)

# ----------------------------------
# LEER DATOS
# ----------------------------------

from procesador_drive import generar_dataframe

with st.spinner(
    "Cargando información desde Drive..."
):

    df = generar_dataframe()

# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.title("Panel de análisis")

tipo = st.sidebar.radio(
    "Selecciona una vista",
    [
        "General estatal",
        "Comparación anual",
        "Hospital individual"
    ]
)

# ==================================
# 1. GENERAL ESTATAL
# ==================================

if tipo == "General estatal":

    st.title(
        "Evolución estatal de comités de bioética"
    )

    MAX_TOTAL = 43

    promedio = df.groupby("anio").agg({
        "integracion": "mean",
        "recursos": "mean",
        "procedimental": "mean",
        "operatividad": "mean"
    }).reset_index()

    promedio["total"] = (
        promedio["integracion"]
        + promedio["recursos"]
        + promedio["procedimental"]
        + promedio["operatividad"]
    )

    promedio["porcentaje"] = (
        promedio["total"]
        / MAX_TOTAL
    ) * 100

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.bar(
        promedio["anio"],
        promedio["integracion"],
        label="Integración"
    )

    ax.bar(
        promedio["anio"],
        promedio["recursos"],
        bottom=promedio["integracion"],
        label="Recursos"
    )

    ax.bar(
        promedio["anio"],
        promedio["procedimental"],
        bottom=(
            promedio["integracion"]
            + promedio["recursos"]
        ),
        label="Procedimental"
    )

    ax.bar(
        promedio["anio"],
        promedio["operatividad"],
        bottom=(
            promedio["integracion"]
            + promedio["recursos"]
            + promedio["procedimental"]
        ),
        label="Operatividad"
    )

    ax.set_xlabel(
        "Año de evaluación"
    )

    ax.set_ylabel(
        "Promedio estatal"
    )

    ax.legend()
    # Mostrar porcentajes dentro de barras
    for i in range(len(promedio)):

     x = promedio["anio"].iloc[i]

     integracion = promedio["integracion"].iloc[i]
     recursos = promedio["recursos"].iloc[i]
     procedimental = promedio["procedimental"].iloc[i]
     operatividad = promedio["operatividad"].iloc[i]

     p_integracion = (
         integracion / MAX_INTEGRACION
     ) * 100

     p_recursos = (
         recursos / MAX_RECURSOS
     ) * 100

     p_procedimental = (
         procedimental / MAX_PROCEDIMENTAL
     ) * 100

     p_operatividad = (
         operatividad / MAX_OPERATIVIDAD
     ) * 100

     ax.text(
         x,
         integracion / 2,
         f"{p_integracion:.0f}%",
         ha="center",
         color="white",
         fontweight="bold"
      )

     ax.text(
         x,
         integracion + recursos / 2,
         f"{p_recursos:.0f}%",
         ha="center",
         color="white",
         fontweight="bold"
      )

     ax.text(
         x,
         integracion
         + recursos
         + procedimental / 2,
         f"{p_procedimental:.0f}%",
         ha="center",
         color="white",
         fontweight="bold"
      )

     ax.text(
         x,
         integracion
         + recursos
         + procedimental
         + operatividad / 2,
         f"{p_operatividad:.0f}%",
         ha="center",
         color="white",
         fontweight="bold"
      )

    st.pyplot(fig)

# ==================================
# 2. COMPARACIÓN ANUAL
# ==================================

elif tipo == "Comparación anual":

    st.title(
        "Comparación hospitalaria por año"
    )

    anio = st.selectbox(
        "Selecciona año",
        sorted(df["anio"].unique())
    )

    datos = df[
        df["anio"] == anio
    ]

    datos["total"] = (
        datos["integracion"]
        + datos["recursos"]
        + datos["procedimental"]
        + datos["operatividad"]
    )

    datos = datos.sort_values(
        by="total",
        ascending=False
    )

    fig, ax = plt.subplots(
        figsize=(12,6)
    )

    ax.bar(
        datos["hospital"],
        datos["integracion"],
        label="Integración"
    )

    ax.bar(
        datos["hospital"],
        datos["recursos"],
        bottom=datos["integracion"],
        label="Recursos"
    )

    ax.bar(
        datos["hospital"],
        datos["procedimental"],
        bottom=(
            datos["integracion"]
            + datos["recursos"]
        ),
        label="Procedimental"
    )

    ax.bar(
        datos["hospital"],
        datos["operatividad"],
        bottom=(
            datos["integracion"]
            + datos["recursos"]
            + datos["procedimental"]
        ),
        label="Operatividad"
    )

    plt.xticks(
        rotation=45
    )

    ax.legend()

    for i in range(len(datos)):

     x = datos["hospital"].iloc[i]

     integracion = datos["integracion"].iloc[i]
     recursos = datos["recursos"].iloc[i]
     procedimental = datos["procedimental"].iloc[i]
     operatividad = datos["operatividad"].iloc[i]

     p_integracion = (
         integracion / MAX_INTEGRACION
      ) * 100

     p_recursos = (
         recursos / MAX_RECURSOS
      ) * 100

     p_procedimental = (
         procedimental / MAX_PROCEDIMENTAL
      ) * 100

     p_operatividad = (
         operatividad / MAX_OPERATIVIDAD
      ) * 100

     ax.text(
         x,
         integracion / 2,
         f"{p_integracion:.0f}%",
         ha="center",
         color="white",
         fontsize=9,
         fontweight="bold"
      )

     ax.text(
         x,
         integracion + recursos / 2,
         f"{p_recursos:.0f}%",
         ha="center",
         color="white",
         fontsize=9,
         fontweight="bold"
      )

     ax.text(
         x,
         integracion
         + recursos
         + procedimental / 2,
         f"{p_procedimental:.0f}%",
         ha="center",
         color="white",
         fontsize=9,
         fontweight="bold"
      )

     ax.text(
         x,
         integracion
         + recursos
         + procedimental
         + operatividad / 2,
         f"{p_operatividad:.0f}%",
         ha="center",
         color="white",
         fontsize=9,
         fontweight="bold"
      )

    st.pyplot(fig)

# ==================================
# 3. HOSPITAL INDIVIDUAL
# ==================================

elif tipo == "Hospital individual":

    hospitales = sorted(
        df["hospital"].unique()
    )

    hospital = st.selectbox(
        "Selecciona hospital",
        hospitales
    )

    datos = df[
        df["hospital"] == hospital
    ]

    datos = datos.sort_values(
        by="anio"
    )

    st.subheader(
        f"Histórico de {hospital}"
    )

    st.dataframe(datos)

    # Verificar comparabilidad
    if len(datos) < 2:

        st.warning(
            "No existen suficientes datos para comparación."
        )

    else:

        datos["total"] = (
            datos["integracion"]
            + datos["recursos"]
            + datos["procedimental"]
            + datos["operatividad"]
        )

        fig, ax = plt.subplots(
            figsize=(8,5)
        )

        ax.bar(
            datos["anio"],
            datos["integracion"],
            label="Integración"
        )

        ax.bar(
            datos["anio"],
            datos["recursos"],
            bottom=datos["integracion"],
            label="Recursos"
        )

        ax.bar(
            datos["anio"],
            datos["procedimental"],
            bottom=(
                datos["integracion"]
                + datos["recursos"]
            ),
            label="Procedimental"
        )

        ax.bar(
            datos["anio"],
            datos["operatividad"],
            bottom=(
                datos["integracion"]
                + datos["recursos"]
                + datos["procedimental"]
            ),
            label="Operatividad"
        )

        ax.set_xlabel("Año")
        ax.set_ylabel("Puntaje")
        ax.legend()

        for i in range(len(datos)):

         x = datos["anio"].iloc[i]

         integracion = datos["integracion"].iloc[i]
         recursos = datos["recursos"].iloc[i]
         procedimental = datos["procedimental"].iloc[i]
         operatividad = datos["operatividad"].iloc[i]

         p_integracion = (
              integracion / MAX_INTEGRACION
           ) * 100

         p_recursos = (
             recursos / MAX_RECURSOS
           ) * 100

         p_procedimental = (
             procedimental / MAX_PROCEDIMENTAL
           ) * 100

         p_operatividad = (
             operatividad / MAX_OPERATIVIDAD
           ) * 100

         ax.text(
              x,
             integracion / 2,
             f"{p_integracion:.0f}%",
              ha="center",
             color="white",
             fontweight="bold"
           )

         ax.text(
              x,
             integracion + recursos / 2,
             f"{p_recursos:.0f}%",
             ha="center",
             color="white",
             fontweight="bold"
           )

         ax.text(
             x,
             integracion
             + recursos
             + procedimental / 2,
             f"{p_procedimental:.0f}%",
             ha="center",
             color="white",
             fontweight="bold"
           )

         ax.text(
             x,
             integracion
             + recursos
             + procedimental
             + operatividad / 2,
             f"{p_operatividad:.0f}%",
             ha="center",
             color="white",
            fontweight="bold"
           )
        st.pyplot(fig)