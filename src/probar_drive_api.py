from lector_drive import obtener_excels

excels = obtener_excels()

print()

print("ARCHIVOS ENCONTRADOS:")

for nombre in excels.keys():

    print(nombre)