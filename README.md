# Dataset de Locales Comerciales — Barcelona

Dataset de locales y establecimientos de la ciudad de Barcelona obtenido desde OpenStreetMap, orientado al análisis de proximidad y competencia para nuevos negocios.

---

## Requisitos

```bash
pip install osmnx pandas geopandas
```

---

## 1. Obtener el dataset

Ejecuta `obtener_dataset.py` para descargar todos los locales de Barcelona directamente desde la API de OpenStreetMap.

```python
# obtener_dataset.py

import osmnx as ox
import pandas as pd
import geopandas as gpd

print("⏳ Descargando locales de Barcelona...")

tags = {
    "shop": True,
    "amenity": True,
    "office": True,
    "tourism": True,
    "leisure": True,
    "craft": True,
    "healthcare": True,
}

gdfs = []
for tag_key, tag_val in tags.items():
    try:
        print(f"  → Descargando '{tag_key}'...")
        gdf = ox.features_from_place("Barcelona, Spain", tags={tag_key: tag_val})
        gdf["categoria_principal"] = tag_key
        gdfs.append(gdf)
    except Exception as e:
        print(f"  ⚠️ Sin resultados para '{tag_key}': {e}")

combined = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
combined["lon"] = combined.geometry.centroid.x
combined["lat"] = combined.geometry.centroid.y

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

cols_presentes = [c for c in cols_utiles if c in combined.columns]
df = pd.DataFrame(combined[cols_presentes])
df = df[df["name"].notna() | df["shop"].notna() | df["amenity"].notna()]

df.to_csv("locales_barcelona.csv", index=False, encoding="utf-8-sig")
print(f"\n✅ Listo! {len(df):,} locales guardados en 'locales_barcelona.csv'")
```

**Tiempo estimado:** 3–8 minutos según conexión.

**Resultado:** fichero `locales_barcelona.csv` con ~48.000 filas y las siguientes columnas:

| Columna | Descripción |
|---|---|
| `categoria_principal` | Tag OSM principal (`shop`, `amenity`, `office`...) |
| `shop` / `amenity` / `office`... | Tipo de actividad específico |
| `name` | Nombre del local |
| `addr:street` / `addr:housenumber` | Dirección |
| `addr:postcode` / `addr:city` | CP y ciudad |
| `phone` / `website` / `email` | Contacto |
| `opening_hours` | Horario |
| `lat` / `lon` | Coordenadas geográficas |
| `osmid` | ID único en OpenStreetMap |

---

## 2. Evaluar el dataset

Ejecuta `evaluar_dataset.py` para obtener un diagnóstico de calidad y cobertura.

```python
# evaluar_dataset.py

import pandas as pd

df = pd.read_csv("locales_barcelona.csv")

print(f"📦 Total de filas: {len(df):,}")
print(f"\n📊 Distribución por categoría:")
print(df["categoria_principal"].value_counts())

print(f"\n🕳️  % de valores vacíos por columna:")
nulls = (df.isnull().sum() / len(df) * 100).round(1)
print(nulls[nulls > 0].sort_values(ascending=False).to_string())

print(f"\n✅ Tienen nombre:       {df['name'].notna().sum():,} ({df['name'].notna().mean()*100:.1f}%)")
print(f"✅ Tienen dirección:    {df['addr:street'].notna().sum():,} ({df['addr:street'].notna().mean()*100:.1f}%)")
print(f"✅ Tienen teléfono:     {df['phone'].notna().sum():,} ({df['phone'].notna().mean()*100:.1f}%)")
print(f"✅ Tienen horario:      {df['opening_hours'].notna().sum():,} ({df['opening_hours'].notna().mean()*100:.1f}%)")
print(f"✅ Tienen coordenadas:  {df['lat'].notna().sum():,} ({df['lat'].notna().mean()*100:.1f}%)")
```

**Resultados esperados:**

| Campo | Cobertura típica |
|---|---|
| Coordenadas | ~100% |
| Nombre | ~55–60% |
| Dirección | ~25–35% |
| Teléfono / Horario | ~10–15% |

---

## 3. Limpiar el dataset

Ejecuta `limpiar_dataset.py` para generar un CSV optimizado para análisis de proximidad, eliminando columnas irrelevantes, unificando el tipo de actividad y eliminando duplicados.

```python
# limpiar_dataset.py

import pandas as pd

df = pd.read_csv("locales_barcelona.csv")

# Columnas relevantes para análisis de proximidad
cols = [
    "categoria_principal", "shop", "amenity", "office",
    "tourism", "leisure", "craft", "healthcare",
    "name", "addr:street", "addr:housenumber", "lat", "lon"
]
df = df[cols]

# Columna unificada con el tipo de actividad
def get_tipo(row):
    for col in ["shop", "amenity", "office", "tourism", "leisure", "craft", "healthcare"]:
        if pd.notna(row[col]):
            return row[col]
    return None

df["tipo_actividad"] = df.apply(get_tipo, axis=1)

# Eliminar filas sin tipo de actividad
df = df[df["tipo_actividad"].notna()]

# Eliminar duplicados por coordenada exacta
df = df.drop_duplicates(subset=["lat", "lon"])

print(f"✅ Dataset limpio: {len(df):,} locales")
print(f"\nTop 20 tipos de actividad:")
print(df["tipo_actividad"].value_counts().head(20))

df.to_csv("locales_bcn_analisis.csv", index=False, encoding="utf-8-sig")
print("\n💾 Guardado en 'locales_bcn_analisis.csv'")
```

**Resultado:** fichero `locales_bcn_analisis.csv` listo para análisis.

---

## Notas sobre los datos

- **Fuente:** [OpenStreetMap](https://www.openstreetmap.org) vía API pública
- **Cobertura:** Ciudad de Barcelona
- **Actualización:** Los datos reflejan el estado de OSM en el momento de la descarga. Se recomienda re-ejecutar `obtener_dataset.py` cada 3–6 meses
- **Licencia:** [ODbL 1.0](https://opendatacommons.org/licenses/odbl/) — datos libres con atribución requerida
- **Limitación:** OSM es colaborativo, por lo que la cobertura puede ser desigual en barrios periféricos
