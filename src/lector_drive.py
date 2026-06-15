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

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]


# ----------------------------------
# CONEXIÓN DRIVE
# ----------------------------------

def conectar_drive():

    try:

        credenciales_json = json.loads(
            st.secrets["GOOGLE_CREDENTIAL"]
        )

        credenciales = (
            service_account.Credentials
            .from_service_account_info(
                credenciales_json,
                scopes=SCOPES
            )
        )

    except:

        credenciales = (
            service_account.Credentials
            .from_service_account_file(
                "dashboard-bioetica-452e687d96e7.json",
                scopes=SCOPES
            )
        )

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