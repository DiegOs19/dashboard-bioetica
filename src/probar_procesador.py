from procesador_drive import obtener_excels

excels = obtener_excels()

# tomar solo un hospital de ejemplo
archivo = excels[2026]

hospital = "CHBHumanitas"

hoja = archivo[hospital]

for i in range(len(hoja)):

    fila = hoja.iloc[i]

    texto = " ".join(
        map(str, fila.values)
    )

    if "subtotal" in texto.lower():

        print("\nFILA:", i)
        print(texto)