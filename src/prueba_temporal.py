from procesador_drive import generar_dataframe

df = generar_dataframe()

print(df.head())

print(
    sorted(
        df["anio"].unique()
    )
)