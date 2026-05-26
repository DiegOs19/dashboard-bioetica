import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------
# CONFIGURACIÓN
# --------------------------------

anio = 2026

# Máximos por dominio
MAX_INTEGRACION = 15
MAX_RECURSOS = 5
MAX_PROCEDIMENTAL = 7
MAX_OPERATIVIDAD = 16

MAX_TOTAL = (
    MAX_INTEGRACION
    + MAX_RECURSOS
    + MAX_PROCEDIMENTAL
    + MAX_OPERATIVIDAD
)

# --------------------------------
# LEER DATOS
# --------------------------------

df = pd.read_csv(
    "outputs/concentrado_general.csv"
)

# Filtrar año
datos = df[
    df["anio"] == anio
]

# Ordenar por total
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

# --------------------------------
# VARIABLES
# --------------------------------

hospitales = datos["hospital"]

integracion = datos["integracion"]
recursos = datos["recursos"]
procedimental = datos["procedimental"]
operatividad = datos["operatividad"]

totales = datos["total"]

# Calcular porcentaje
porcentajes = (
    (totales / MAX_TOTAL) * 100
).round(0)

# --------------------------------
# CREAR FIGURA
# --------------------------------

fig, ax1 = plt.subplots(
    figsize=(14, 8)
)

# --------------------------------
# BARRAS APILADAS
# --------------------------------

ax1.bar(
    hospitales,
    integracion,
    label="Integración"
)

ax1.bar(
    hospitales,
    recursos,
    bottom=integracion,
    label="Recursos y suministros"
)

ax1.bar(
    hospitales,
    procedimental,
    bottom=integracion + recursos,
    label="Marco procedimental"
)

ax1.bar(
    hospitales,
    operatividad,
    bottom=(
        integracion
        + recursos
        + procedimental
    ),
    label="Operatividad"
)

# --------------------------------
# EJE IZQUIERDO
# --------------------------------

ax1.set_ylabel(
    "Puntaje obtenido",
    fontsize=12
)

ax1.set_xlabel(
    "Hospital",
    fontsize=12
)

ax1.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

# Rotar nombres
plt.xticks(
    rotation=45,
    ha="right"
)

# --------------------------------
# EJE DERECHO (%)
# --------------------------------

ax2 = ax1.twinx()

ax2.plot(
    hospitales,
    porcentajes,
    marker="o",
    linewidth=2
)

ax2.set_ylabel(
    "Porcentaje de cumplimiento (%)",
    fontsize=12
)

# --------------------------------
# MOSTRAR %
# --------------------------------

for x, y in zip(
    hospitales,
    porcentajes
):

    ax2.text(
        x,
        y + 1,
        f"{int(y)}%",
        ha="center",
        fontsize=10
    )

# --------------------------------
# TÍTULO
# --------------------------------

plt.title(
    f"Comparación general de comités de bioética - {anio}",
    fontsize=15,
    pad=20
)

# Leyenda
ax1.legend(
    loc="upper left"
)

# Ajustar espacios
plt.tight_layout()

# Guardar imagen
plt.savefig(
    f"outputs/comparacion_general_{anio}.png"
)

# Mostrar
plt.show()