# pip install osmnx pandas geopandas

import osmnx as ox
import pandas as pd
import geopandas as gpd

print("⏳ Descargando locales de Barcelona...")

# Todos los tipos de locales relevantes
tags = {
    "shop": True,        # Comercios (supermercados, ropa, farmacias...)
    "amenity": True,     # Restaurantes, bares, bancos, hospitales...
    "office": True,      # Oficinas y despachos
    "tourism": True,     # Hoteles, museos, atracciones
    "leisure": True,     # Gimnasios, spas, ocio
    "craft": True,       # Talleres artesanales
    "healthcare": True,  # Centros médicos, clínicas
}

# Descarga por cada tag y acumula
gdfs = []
for tag_key, tag_val in tags.items():
    try:
        print(f"  → Descargando '{tag_key}'...")
        gdf = ox.features_from_place(
            "Barcelona, Spain",
            tags={tag_key: tag_val}
        )
        gdf["categoria_principal"] = tag_key
        gdfs.append(gdf)
    except Exception as e:
        print(f"  ⚠️ Sin resultados para '{tag_key}': {e}")

# Combinar todos
print("🔀 Combinando datos...")
combined = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

# Extraer lat/lon desde la geometría (puntos y polígonos)
combined["lon"] = combined.geometry.centroid.x
combined["lat"] = combined.geometry.centroid.y

# Columnas útiles a conservar
cols_utiles = [
    "categoria_principal",
    "name", "brand",
    "shop", "amenity", "office", "tourism", "leisure", "craft", "healthcare",
    "addr:street", "addr:housenumber", "addr:postcode", "addr:city",
    "phone", "website", "email",
    "opening_hours",
    "lat", "lon",
    "osmid"
]

# Quedarse solo con las columnas que existen en el dataframe
cols_presentes = [c for c in cols_utiles if c in combined.columns]
df = pd.DataFrame(combined[cols_presentes])

# Limpiar filas sin nombre ni tipo (poco útiles)
df = df[df["name"].notna() | df["shop"].notna() | df["amenity"].notna()]

# Exportar
output_path = "locales_barcelona.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\n✅ Listo! {len(df):,} locales guardados en '{output_path}'")
print(df.head())