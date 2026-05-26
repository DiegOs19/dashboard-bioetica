import pandas as pd

archivo = "data/2024.xlsx"

excel = pd.ExcelFile(archivo)

# Hojas que NO queremos analizar
excluir = [
    "ORIGINAL",
    "CONCENTRADO",
    "SUPERVISIONES2024"
]

datos = []

for hospital in excel.sheet_names:

    # Saltar hojas no deseadas
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

    # Si faltan subtotales, rellenar con 0
    while len(subtotales) < 4:
        subtotales.append(0)

    datos.append([
        hospital,
        2024,
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

print(resultado)

resultado.to_csv(
    "outputs/concentrado_2024.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print("Archivo CSV generado correctamente")