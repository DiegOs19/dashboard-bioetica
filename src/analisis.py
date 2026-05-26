import pandas as pd

# Leer datos
df = pd.read_csv(
    "outputs/concentrado_general.csv"
)

# Hospital a analizar
hospital = "CHBNativitas"

# Filtrar hospital
datos_hospital = df[
    df["hospital"] == hospital
]

# Ordenar por año
datos_hospital = datos_hospital.sort_values(
    by="anio"
)

print("=" * 50)
print(f"Hospital: {hospital}")
print("=" * 50)

print()

totales = []

for _, fila in datos_hospital.iterrows():

    total = (
        fila["integracion"] +
        fila["recursos"] +
        fila["procedimental"] +
        fila["operatividad"]
    )

    totales.append(total)

    print(
        f"{fila['anio']} → "
        f"Total: {total}"
    )

print()

# Detectar tendencia
if len(totales) >= 2:

    diferencia = totales[-1] - totales[0]

    if diferencia > 0:
        tendencia = "MEJORA"

    elif diferencia < 0:
        tendencia = "RETROCESO"

    else:
        tendencia = "ESTABLE"

    print(f"Tendencia: {tendencia}")
    print(f"Cambio total: {diferencia}")
    print()
    print("=" * 50)
    print("ANÁLISIS POR DOMINIO")
    print("=" * 50)

    primer_registro = datos_hospital.iloc[0]
    ultimo_registro = datos_hospital.iloc[-1]

    dominios = [
     "integracion",
     "recursos",
     "procedimental",
     "operatividad"
    ]

    for dominio in dominios:

     valor_inicial = primer_registro[dominio]
     valor_final = ultimo_registro[dominio]

     diferencia = valor_final - valor_inicial

     if diferencia > 0:
        simbolo = "↑"

     elif diferencia < 0:
        simbolo = "↓"

     else:
        simbolo = "="

     print(
         f"{dominio.capitalize()} "
         f"{simbolo} "
         f"{diferencia}"
     )

else:
    print(
        "No hay suficientes datos para comparar"
    )

