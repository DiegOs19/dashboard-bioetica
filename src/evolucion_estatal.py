import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# MÁXIMOS POR DOMINIO
# ----------------------------

MAX_INTEGRACION = 15
MAX_RECURSOS = 5
MAX_PROCEDIMENTAL = 7
MAX_OPERATIVIDAD = 16
MAX_TOTAL = 43

# ----------------------------
# LEER DATOS
# ----------------------------

df = pd.read_csv(
    "outputs/concentrado_general.csv"
)

# ----------------------------
# PROMEDIO ESTATAL POR AÑO
# ----------------------------

promedio = df.groupby("anio").agg({
    "integracion": "mean",
    "recursos": "mean",
    "procedimental": "mean",
    "operatividad": "mean"
}).reset_index()

promedio = promedio.round(2)

# ----------------------------
# CALCULAR TOTALES
# ----------------------------

promedio["total"] = (
    promedio["integracion"]
    + promedio["recursos"]
    + promedio["procedimental"]
    + promedio["operatividad"]
)

promedio["porcentaje_total"] = (
    promedio["total"] / MAX_TOTAL
) * 100

# ----------------------------
# PORCENTAJE POR DOMINIO
# ----------------------------

promedio["p_integracion"] = (
    promedio["integracion"]
    / MAX_INTEGRACION
) * 100

promedio["p_recursos"] = (
    promedio["recursos"]
    / MAX_RECURSOS
) * 100

promedio["p_procedimental"] = (
    promedio["procedimental"]
    / MAX_PROCEDIMENTAL
) * 100

promedio["p_operatividad"] = (
    promedio["operatividad"]
    / MAX_OPERATIVIDAD
) * 100

# ----------------------------
# VARIABLES
# ----------------------------

anios = promedio["anio"]

integracion = promedio["integracion"]
recursos = promedio["recursos"]
procedimental = promedio["procedimental"]
operatividad = promedio["operatividad"]

totales = promedio["total"]
porcentaje_total = promedio["porcentaje_total"]

# ----------------------------
# CREAR FIGURA
# ----------------------------

fig, ax1 = plt.subplots(
    figsize=(12, 7)
)

# COLORES
color_integracion = "#4E79A7"
color_recursos = "#F28E2B"
color_procedimental = "#59A14F"
color_operatividad = "#E15759"

# ----------------------------
# BARRAS APILADAS
# ----------------------------

ax1.bar(
    anios,
    integracion,
    color=color_integracion,
    label="Integración"
)

ax1.bar(
    anios,
    recursos,
    bottom=integracion,
    color=color_recursos,
    label="Recursos y suministros"
)

ax1.bar(
    anios,
    procedimental,
    bottom=integracion + recursos,
    color=color_procedimental,
    label="Marco procedimental"
)

ax1.bar(
    anios,
    operatividad,
    bottom=(
        integracion
        + recursos
        + procedimental
    ),
    color=color_operatividad,
    label="Operatividad"
)

# ----------------------------
# % DENTRO DE CADA DOMINIO
# ----------------------------

for i in range(len(anios)):

    x = anios.iloc[i]

    # Integración
    ax1.text(
        x,
        integracion.iloc[i] / 2,
        f"{promedio['p_integracion'].iloc[i]:.0f}%",
        ha="center",
        va="center",
        color="white",
        fontweight="bold"
    )

    # Recursos
    ax1.text(
        x,
        integracion.iloc[i]
        + recursos.iloc[i] / 2,
        f"{promedio['p_recursos'].iloc[i]:.0f}%",
        ha="center",
        va="center",
        color="white",
        fontweight="bold"
    )

    # Procedimental
    ax1.text(
        x,
        integracion.iloc[i]
        + recursos.iloc[i]
        + procedimental.iloc[i] / 2,
        f"{promedio['p_procedimental'].iloc[i]:.0f}%",
        ha="center",
        va="center",
        color="white",
        fontweight="bold"
    )

    # Operatividad
    ax1.text(
        x,
        integracion.iloc[i]
        + recursos.iloc[i]
        + procedimental.iloc[i]
        + operatividad.iloc[i] / 2,
        f"{promedio['p_operatividad'].iloc[i]:.0f}%",
        ha="center",
        va="center",
        color="white",
        fontweight="bold"
    )

# ----------------------------
# TOTAL ARRIBA
# ----------------------------

for x, y in zip(
    anios,
    porcentaje_total
):

    ax1.text(
        x,
        totales.loc[anios == x].values[0] + 0.8,
        f"{y:.0f}%",
        ha="center",
        fontsize=11,
        fontweight="bold"
    )

# ----------------------------
# ESTILO
# ----------------------------

ax1.set_title(
    "Evolución estatal de los comités de bioética",
    fontsize=15,
    pad=20
)

ax1.set_xlabel(
    "Año de evaluación"
)

ax1.set_ylabel(
    "Promedio estatal de puntaje"
)

ax1.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

plt.xticks(anios)

ax1.legend()

plt.tight_layout()

# Guardar
plt.savefig(
    "outputs/evolucion_estatal.png"
)

plt.show()