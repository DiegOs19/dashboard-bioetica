from lector_drive import obtener_excels

excels = obtener_excels()

print("\nTIPO:", type(excels))
print("AÑOS CARGADOS:", excels.keys())

for anio, archivo in excels.items():

    print(f"\n===== {anio} =====")

    print("Número de hojas:", len(archivo))

    print("Hojas:")

    for hoja in archivo.keys():

        print("-", hoja)
        