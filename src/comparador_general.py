import pandas as pd

# Leer dataset
df = pd.read_csv(
    "outputs/concentrado_general.csv"
)

# Contar registros por hospital
conteo = df["hospital"].value_counts()

comparables = []

for hospital, cantidad in conteo.items():

    if cantidad >= 2:
        comparables.append(hospital)

resultados = []

for hospital in comparables:

    datos_hospital = df[
        df["hospital"] == hospital
    ]

    datos_hospital = datos_hospital.sort_values(
        by="anio"
    )

    primer = datos_hospital.iloc[0]
    ultimo = datos_hospital.iloc[-1]

    # Total inicial
    total_inicial = (
        primer["integracion"] +
        primer["recursos"] +
        primer["procedimental"] +
        primer["operatividad"]
    )

    # Total final
    total_final = (
        ultimo["integracion"] +
        ultimo["recursos"] +
        ultimo["procedimental"] +
        ultimo["operatividad"]
    )

    cambio_total = (
        total_final - total_inicial
    )

    # Tendencia
    if cambio_total > 0:
        tendencia = "MEJORA"

    elif cambio_total < 0:
        tendencia = "RETROCESO"

    else:
        tendencia = "ESTABLE"

    # Cambios por dominio
    cambio_integracion = (
        ultimo["integracion"]
        - primer["integracion"]
    )

    cambio_recursos = (
        ultimo["recursos"]
        - primer["recursos"]
    )

    cambio_procedimental = (
        ultimo["procedimental"]
        - primer["procedimental"]
    )

    cambio_operatividad = (
        ultimo["operatividad"]
        - primer["operatividad"]
    )

    resultados.append([
        hospital,
        f"{primer['anio']} - {ultimo['anio']}",
        tendencia,
        cambio_total,
        cambio_integracion,
        cambio_recursos,
        cambio_procedimental,
        cambio_operatividad
    ])

resultado_final = pd.DataFrame(
    resultados,
    columns=[
        "hospital",
        "periodo",
        "tendencia",
        "cambio_total",
        "integracion",
        "recursos",
        "procedimental",
        "operatividad"
    ]
)

print(resultado_final)

resultado_final.to_csv(
    "outputs/comparacion_hospitales.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print("Comparación general creada")