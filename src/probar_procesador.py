from procesador_drive import generar_dataframe

df = generar_dataframe()

print("\nCOLUMNAS:")
print(df.columns.tolist())

print("\nTAMAÑO:")
print(df.shape)

print("\nHOSPITALES ÚNICOS:")
print(sorted(df["hospital"].unique()))

print("\nPRIMERAS 30 FILAS:")
print(df.head(30))