import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
# ----------------------------------
# MÁXIMOS POR DOMINIO
# ----------------------------------

MAX_INTEGRACION = 15
MAX_RECURSOS = 5
MAX_PROCEDIMENTAL = 7
MAX_OPERATIVIDAD = 16
MAX_TOTAL = 43

# ----------------------------------
# ETIQUETAS DE PORCENTAJE
# ----------------------------------

def agregar_porcentajes(
    ax,
    x,
    integracion,
    recursos,
    procedimental,
    operatividad
):

    def obtener_tamano(valor):

        if valor >= 8:
            return 10

        elif valor >= 5:
            return 9

        elif valor >= 3:
            return 8

        elif valor >= 2:
            return 7

        else:
            return 6

    p_integracion = min(
        (integracion / MAX_INTEGRACION) * 100,
        100
    )

    p_recursos = min(
        (recursos / MAX_RECURSOS) * 100,
        100
    )

    p_procedimental = min(
        (procedimental / MAX_PROCEDIMENTAL) * 100,
        100
    )

    p_operatividad = min(
        (operatividad / MAX_OPERATIVIDAD) * 100,
        100
    )

    # ----------------------------
    # INTEGRACIÓN
    # ----------------------------

    if integracion > 0:

        ax.text(
            x,
            integracion / 2,
            f"{p_integracion:.0f}%",
            ha="center",
            va="center",
            color="white",
            fontsize=obtener_tamano(integracion),
            fontweight="bold"
        )

    # ----------------------------
    # RECURSOS
    # ----------------------------

    if recursos > 0:

        ax.text(
            x,
            integracion + recursos / 2,
            f"{p_recursos:.0f}%",
            ha="center",
            va="center",
            color="white",
            fontsize=obtener_tamano(recursos),
            fontweight="bold"
        )

    # ----------------------------
    # PROCEDIMENTAL
    # ----------------------------

    if procedimental > 0:

        ax.text(
            x,
            integracion
            + recursos
            + procedimental / 2,
            f"{p_procedimental:.0f}%",
            ha="center",
            va="center",
            color="white",
            fontsize=obtener_tamano(procedimental),
            fontweight="bold"
        )

    # ----------------------------
    # OPERATIVIDAD
    # ----------------------------

    if operatividad > 0:

        ax.text(
            x,
            integracion
            + recursos
            + procedimental
            + operatividad / 2,
            f"{p_operatividad:.0f}%",
            ha="center",
            va="center",
            color="white",
            fontsize=obtener_tamano(operatividad),
            fontweight="bold"
        )

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

@st.cache_data(ttl=300)
def cargar_datos():
    return generar_dataframe()

df = cargar_datos()

# ----------------------------------
# SIDEBAR
# ----------------------------------

col1, col2, col3 = st.columns(
    [1, 3, 1]
)

with col1:
    st.image(
        "assets/cobiet.jpg",
        width=200
    )

with col3:
    st.image(
        "assets/sesa.jpg",
        width=200
    )

with col2:
    st.markdown(
        """
        <h1 style='text-align:center; margin-top:25px;'>
        Comisión de Bioética
        </h1>
        """,
        unsafe_allow_html=True
    )

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

    for i in range(len(promedio)):
        agregar_porcentajes(
            ax,
            promedio["anio"].iloc[i],
            promedio["integracion"].iloc[i],
            promedio["recursos"].iloc[i],
            promedio["procedimental"].iloc[i],
            promedio["operatividad"].iloc[i]
        )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
     "Hospitales",
     df["hospital"].nunique()
    )

    ultimo_anio = df["anio"].max()

    actual = df[
     df["anio"] == ultimo_anio
    ]

    promedio_actual = (
       (
          actual["integracion"]
          + actual["recursos"]
          + actual["procedimental"]
          + actual["operatividad"]
        ).mean()
       / 43
    ) * 100

    col2.metric(
     "Promedio Estatal",
     f"{promedio_actual:.1f}%"
    )

    actual["total"] = (
     actual["integracion"]
     + actual["recursos"]
     + actual["procedimental"]
     + actual["operatividad"]
    )

    mejor = actual.loc[
     actual["total"].idxmax()
    ]

    col3.metric(
     "Mejor Hospital",
     mejor["hospital"]
    )

    col4.metric(
     "Último Año",
     int(ultimo_anio)
    )
    plt.tight_layout()
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
        figsize=(16,8)
    )

    ax.set_ylim(0, 46)

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

    plt.tight_layout()

    ax.set_ylabel(
     "Puntaje obtenido"
    )

    ax.set_xlabel(
      "Hospital"
    )

    ax.legend()

    for i in range(len(datos)):

     agregar_porcentajes(
          ax,
          datos["hospital"].iloc[i],
          datos["integracion"].iloc[i],
          datos["recursos"].iloc[i],
          datos["procedimental"].iloc[i],
          datos["operatividad"].iloc[i]
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
    
    datos_mostrar = datos.rename(
       columns={
         "anio": "Año",
         "hospital": "Hospital",
         "integracion": "Integración",
         "recursos": "Recursos",
         "procedimental": "Procedimental",
         "operatividad": "Operatividad"
       }
    )

    st.dataframe(
      datos_mostrar,
      use_container_width=True
    )

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
            agregar_porcentajes(
                ax,
                datos["anio"].iloc[i],
                datos["integracion"].iloc[i],
                datos["recursos"].iloc[i],
                datos["procedimental"].iloc[i],
                datos["operatividad"].iloc[i]
            )
        plt.tight_layout()
        st.pyplot(fig)