import pandas as pd

df = pd.read_csv("locales_barcelona.csv")

print(f"📦 Total de filas: {len(df):,}")
print(f"\n📊 Distribución por categoría:")
print(df["categoria_principal"].value_counts())

print(f"\n🕳️  % de valores vacíos por columna:")
nulls = (df.isnull().sum() / len(df) * 100).round(1)
print(nulls[nulls > 0].sort_values(ascending=False).to_string())

print(f"\n✅ Tienen nombre: {df['name'].notna().sum():,} ({df['name'].notna().mean()*100:.1f}%)")
print(f"✅ Tienen dirección: {df['addr:street'].notna().sum():,} ({df['addr:street'].notna().mean()*100:.1f}%)")
print(f"✅ Tienen teléfono: {df['phone'].notna().sum():,} ({df['phone'].notna().mean()*100:.1f}%)")
print(f"✅ Tienen horario: {df['opening_hours'].notna().sum():,} ({df['opening_hours'].notna().mean()*100:.1f}%)")
print(f"✅ Tienen coordenadas: {df['lat'].notna().sum():,} ({df['lat'].notna().mean()*100:.1f}%)")