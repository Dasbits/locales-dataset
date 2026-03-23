import pandas as pd

df = pd.read_csv("locales_barcelona.csv")

# 1. Quedarse solo con columnas relevantes
cols = ["categoria_principal", "shop", "amenity", "office",
        "tourism", "leisure", "craft", "healthcare",
        "name", "addr:street", "addr:housenumber", "lat", "lon"]
df = df[cols]

# 2. Crear columna unificada "tipo_actividad"
def get_tipo(row):
    for col in ["shop", "amenity", "office", "tourism", "leisure", "craft", "healthcare"]:
        if pd.notna(row[col]):
            return row[col]
    return None

df["tipo_actividad"] = df.apply(get_tipo, axis=1)

# 3. Eliminar filas sin tipo (no sirven para análisis de competencia)
df = df[df["tipo_actividad"].notna()]

# 4. Eliminar duplicados por coordenada exacta
df = df.drop_duplicates(subset=["lat", "lon"])

print(f"✅ Dataset listo: {len(df):,} locales con tipo de actividad")
print(f"\nTop 20 tipos de actividad:")
print(df["tipo_actividad"].value_counts().head(20))

df.to_csv("locales_bcn_analisis.csv", index=False, encoding="utf-8-sig")