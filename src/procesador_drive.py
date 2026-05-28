import pandas as pd
from lector_drive import obtener_excels


def extraer_subtotales(df_hoja):

    subtotales = []

    # recorrer filas
    for _, fila in df_hoja.iterrows():

        texto_fila = " ".join(
            map(str, fila.values)
        ).lower()

        # buscar subtotal
        if "subtotal por dominio" in texto_fila:

            numeros = pd.to_numeric(
                fila,
                errors="coerce"
            ).dropna()

            valor = (
                numeros.iloc[-1]
                if len(numeros) > 0
                else 0
            )

            subtotales.append(valor)

    # asegurar 4 dominios
    while len(subtotales) < 4:

        subtotales.append(0)

    return {
        "integracion": subtotales[0],
        "recursos": subtotales[1],
        "procedimental": subtotales[2],
        "operatividad": subtotales[3]
    }   


def generar_dataframe():

    excels = obtener_excels()

    registros = []

    for anio, archivo in excels.items():

        HOJAS_EXCLUIDAS = [
              "original",
             "concentrado",
             "supervisiones",
             "supervision",
             "resumen",
             "general"
         ]
        
        for hospital, hoja in archivo.items():

          nombre = hospital.lower().strip()

         # excluir hojas no hospitalarias
          if any(
             palabra in nombre
             for palabra in HOJAS_EXCLUIDAS
          ):
           continue

        try:
             datos = extraer_subtotales(
                  hoja
             )

             fila = {
                 "anio": anio,
                  "hospital": hospital,
                  **datos
             }

             registros.append(
                 fila
              )
        except Exception as e:

              print(
              f"Error {hospital}: {e}"
           )
        
       

    df = pd.DataFrame(
        registros
    )

    return df