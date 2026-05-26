import pandas as pd


def procesar_excel(nombre_archivo, anio):

    archivo = f"data/{nombre_archivo}"

    excel = pd.ExcelFile(archivo)

    excluir = [
        "ORIGINAL",
        "CONCENTRADO",
        "SUPERVISIONES2024",
        "SUPERVISIONES2025",
        "SUPERVISIONES2026"
    ]

    datos = []

    for hospital in excel.sheet_names:

        # Ignorar hojas no válidas
        if hospital in excluir:
            continue

        df = pd.read_excel(
            archivo,
            sheet_name=hospital,
            header=None
        )

        subtotales = []

        for i in range(len(df)):

            texto = str(df.iloc[i, 0])

            if "SUBTOTAL POR DOMINIO" in texto:

                valor = df.iloc[i, 2]

                subtotales.append(valor)

        # Completar si faltan dominios
        while len(subtotales) < 4:
            subtotales.append(0)

        datos.append([
            hospital,
            anio,
            subtotales[0],
            subtotales[1],
            subtotales[2],
            subtotales[3]
        ])

    resultado = pd.DataFrame(
        datos,
        columns=[
            "hospital",
            "anio",
            "integracion",
            "recursos",
            "procedimental",
            "operatividad"
        ]
    )

    return resultado


# Procesar todos los años
df_2024 = procesar_excel("2024.xlsx", 2024)
df_2025 = procesar_excel("2025.xlsx", 2025)
df_2026 = procesar_excel("2026.xlsx", 2026)

# Unir todo
concentrado_general = pd.concat([
    df_2024,
    df_2025,
    df_2026
])

# Guardar CSV general
concentrado_general.to_csv(
    "outputs/concentrado_general.csv",
    index=False,
    encoding="utf-8-sig"
)

print(concentrado_general)

print()
print("Concentrado general creado correctamente")