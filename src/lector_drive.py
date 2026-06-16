import io
import pandas as pd

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

import json
import streamlit as st


# ----------------------------------
# CONFIGURACIÓN
# ----------------------------------

CARPETA_ID = "18HSSWXvMr_zEtPwVMb3xOjAE8I9CYfkY"

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


# ----------------------------------
# CONEXIÓN DRIVE
# ----------------------------------

def conectar_drive():

    try:

        print("Intentando usar Streamlit Secrets")

        credenciales_json = dict(
            st.secrets["GOOGLE_CREDENTIAL"]
        )

        credenciales = (
            service_account.Credentials
            .from_service_account_info(
                credenciales_json,
                scopes=SCOPES
            )
        )

        print("Secrets cargados correctamente")

    except Exception as e:

        import traceback

        print("ERROR EN SECRETS:")
        print(type(e))
        print(str(e))
        traceback.print_exc()

        raise e

    servicio = build(
        "drive",
        "v3",
        credentials=credenciales
    )

    return servicio


# ----------------------------------
# LISTAR ARCHIVOS
# ----------------------------------

def listar_archivos_excel():

    servicio = conectar_drive()

    resultado = servicio.files().list(
     q=f"'{CARPETA_ID}' in parents and trashed = false",
     fields="files(id,name,mimeType,shortcutDetails)"
    ).execute()

    archivos = resultado.get(
        "files",
        []
    )

    excels = []

    for archivo in archivos:
        
        print(
            archivo["name"],
            archivo["mimeType"]
        )
        print("\nARCHIVO:")
        print("Nombre:", archivo["name"])
        print("Tipo:", archivo["mimeType"])

        if "shortcutDetails" in archivo:
          print(
             "Destino:",
             archivo["shortcutDetails"]
            )
        

        nombre = archivo["name"].lower()

        if (
            "cedula" in nombre
            or "cédula" in nombre
        ):
            excels.append(archivo)

    return excels


# ----------------------------------
# DESCARGAR EXCEL
# ----------------------------------

def descargar_excel(file_id):

    servicio = conectar_drive()

    request = servicio.files().export_media(
        fileId=file_id,
        mimeType=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    )

    archivo = io.BytesIO()

    downloader = MediaIoBaseDownload(
        archivo,
        request
    )

    done = False

    while not done:

        status, done = downloader.next_chunk()

    archivo.seek(0)

    return pd.read_excel(
        archivo,
        sheet_name=None
    )


# ----------------------------------
# OBTENER EXCELS
# ----------------------------------

def obtener_excels():

    excels_drive = listar_archivos_excel()

    datos = {}

    for archivo in excels_drive:

        try:

            nombre = archivo["name"]

            print(
                f"Cargando: {nombre}"
            )

            target_id = (
              archivo["shortcutDetails"]["targetId"]
            )
            
            hojas = descargar_excel(
              target_id
            )

            datos[nombre] = hojas

        except Exception as e:

            print(
                f"Error {nombre}: {e}"
            )

    return datos