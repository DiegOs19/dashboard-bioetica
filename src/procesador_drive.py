import pandas as pd
from lector_drive import obtener_excels
import re



def obtener_anio_desde_excel(archivo):

    for nombre_hoja, hoja in archivo.items():

        try:

            for fila in range(
                min(20, len(hoja))
            ):

                texto = " ".join(
                    str(x)
                    for x in hoja.iloc[fila]
                    if pd.notna(x)
                )

                if (
                    "fecha de visita"
                    in texto.lower()
                ):

                    for valor in hoja.iloc[fila]:

                        if pd.notna(valor):

                            texto_valor = str(valor)

                            if "20" in texto_valor:

                                fecha = pd.to_datetime(
                                    texto_valor,
                                    errors="coerce"
                                )

                                if pd.notna(fecha):

                                    return int(
                                        fecha.year
                                    )

        except:
            pass

    return None



def obtener_anio(nombre_archivo, archivo):

    # 1. Buscar año en el nombre
    coincidencia = re.search(
        r"20\d{2}",
        nombre_archivo
    )

    if coincidencia:

        return int(
            coincidencia.group()
        )

    # 2. Buscar fecha dentro del excel
    return obtener_anio_desde_excel(
        archivo
    )



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

def normalizar_nombre(nombre):

    nombre = nombre.lower()

    reemplazos = {

     # IMSS
     "chbdelimss": "CHB IMSS",
     "chbimss1": "CHB IMSS Z1",
     "chbimssz1": "CHB IMSS Z1",
     "chbimss2": "CHB IMSS Z2",
     "chbimssz2": "CHB IMSS Z2",
     "chbimss8": "CHB IMSS Z8",
     "chbimssz8": "CHB IMSS Z8",

     # ISSSTE
     "chbissste": "CHB ISSSTE",
     "chbdelissste": "CHB ISSSTE",
     "chbdelissste": "CHB ISSSTE",

     # HIT
     "chbhit": "CHB HIT",
     "chbdelhit": "CHB HIT",

     # HUMANITAS
     "chbhumanitas": "CHB Humanitas",

     # HUAMANTLA
     "chbhuamantla": "CHB Huamantla",

     # NATIVITAS
     "chbnativitas": "CHB Nativitas",

     # SPM
     "chbhgspm": "CHB SPM",
     "chbdespm": "CHB SPM",

     # CALPULALPAN
     "chbhcalpulalpan": "CHB Calpulalpan",
     "chbdelhgcalpulapan": "CHB Calpulalpan",

     # HMT
     "chbdelhmt": "CHB HMT",
     "cbasdelhmt": "CBAS HMT",

     # HRESP
     "chbhresp": "CHB HRESP",
     "chbdelhresp": "CHB HRESP",

     # SAN CARLOS
     "cbassancarlos": "CBAS San Carlos",

     # CEI
     "ceiissste": "CEI ISSSTE",
     "ceidelimss": "CEI IMSS",
     "ceihit": "CEI HIT",
     "ceidelhit": "CEI HIT",
     "ceiopdsesa": "CEI OPD",
     "ceidelopd": "CEI OPD",
     "ceihgt": "CEI HGT",
     "ceidelauat": "CEI UAT"
    }

    limpio = (
        nombre
        .replace(" ", "")
        .replace("#", "")
    )

    return reemplazos.get(
        limpio,
        nombre.upper()
    )

def generar_dataframe():

    excels = obtener_excels()

    registros = []

    HOJAS_EXCLUIDAS = [
        "original",
        "concentrado",
        "supervision",
        "supervisiones",
        "copia de"
    ]

    for nombre_archivo, archivo in excels.items():

        anio = obtener_anio(
            nombre_archivo,
            archivo
        )

        print(
            f"\nArchivo: {nombre_archivo}"
        )

        print(
            f"Año detectado: {anio}"
        )

        if anio is None:

            print(
                "No se pudo detectar año"
            )

            continue

        for hospital, hoja in archivo.items():

            nombre = (
                hospital
                .lower()
                .strip()
            )

            if any(
                palabra in nombre
                for palabra
                in HOJAS_EXCLUIDAS
            ):
                continue

            try:

                datos = extraer_subtotales(
                    hoja
                )

                fila = {

                    "anio": anio,

                    "hospital":
                    normalizar_nombre(
                        hospital
                    ),

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

    print(
        "\nHospitales detectados:"
    )

    print(
        sorted(
            df["hospital"].unique()
        )
    )

    return df
    
