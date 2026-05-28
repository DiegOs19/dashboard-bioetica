import pandas as pd

# --------------------------
# IDS DE DRIVE
# --------------------------

ARCHIVOS = {
    2024: "1Wuct2Cj55GlmRMLVUr-pljAt5s8SnpSdjS-sj-H3_4Y",
    2025: "14jmDthpc8Zs5Ekp0VLLtjeeTT0QhmAsMVFHDEnIA30A",
    2026: "1cT-NPquELjaeWNRisemfeMaHsf6XacchepO0oClvSZc"
}


def leer_excel_drive(file_id):

    url = (
        f"https://drive.google.com/uc?id={file_id}"
    )

    df = pd.read_excel(
        url,
        sheet_name=None
    )

    return df


def obtener_excels():

    datos = {}

    for anio, file_id in ARCHIVOS.items():

        try:

            datos[anio] = leer_excel_drive(
                file_id
            )

            print(
                f"{anio} cargado"
            )

        except Exception as e:

            print(
                f"Error {anio}: {e}"
            )

    return datos