import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# CONFIGURACIÓN
# -----------------------------

hospital = "CHBHuamantla"

# -----------------------------
# LEER DATOS
# -----------------------------

df = pd.read_csv(
    "outputs/concentrado_general.csv"
)

# Filtrar hospital
datos = df[
    df["hospital"] == hospital
]

# Ordenar por año
datos = datos.sort_values(
    by="anio"
)

# -----------------------------
# DATOS DE DOMINIOS
# -----------------------------

anios = datos["anio"]

integracion = datos["integracion"]
recursos = datos["recursos"]
procedimental = datos["procedimental"]
operatividad = datos["operatividad"]

# Totales
totales = (
    integracion
    + recursos
    + procedimental
    + operatividad
)

# -----------------------------
# CREAR GRÁFICA
# -----------------------------

plt.figure(figsize=(10, 6))

# Barras apiladas
plt.bar(
    anios,
    integracion,
    label="Integración"
)

plt.bar(
    anios,
    recursos,
    bottom=integracion,
    label="Recursos y suministros"
)

plt.bar(
    anios,
    procedimental,
    bottom=integracion + recursos,
    label="Marco procedimental"
)

plt.bar(
    anios,
    operatividad,
    bottom=(
        integracion
        + recursos
        + procedimental
    ),
    label="Operatividad"
)

# -----------------------------
# MOSTRAR TOTAL ARRIBA
# -----------------------------

for x, total in zip(
    anios,
    totales
):

    plt.text(
        x,
        total + 0.5,
        str(total),
        ha="center",
        fontsize=11
    )

# -----------------------------
# DETALLES VISUALES
# -----------------------------

plt.title(
    f"Evolución histórica del comité de bioética\n{hospital}",
    fontsize=14,
    pad=15
)

plt.xlabel(
    "Año de evaluación",
    fontsize=12
)

plt.ylabel(
    "Puntaje obtenido",
    fontsize=12
)

# Mostrar años completos
plt.xticks(anios)

# Leyenda
plt.legend()

# Cuadrícula horizontal
plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

# Ajustar márgenes
plt.tight_layout()

# Guardar imagen
plt.savefig(
    f"outputs/{hospital}_barras.png"
)

# Mostrar
plt.show()