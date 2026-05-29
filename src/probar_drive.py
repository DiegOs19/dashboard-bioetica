from lector_drive import obtener_excels

excels = obtener_excels()

for anio, archivo in excels.items():

    print(f"\nAÑO {anio}")

    print(
        list(archivo.keys())
    )