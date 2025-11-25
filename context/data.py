import pyreadstat
import pandas as pd
import json
from datetime import datetime

file_path = "datos.sav"

# Leer el archivo SPSS
df, meta = pyreadstat.read_sav(file_path)

# Análisis completo del archivo
print("="*80)
print("ANÁLISIS COMPLETO DEL ARCHIVO DATOS.SAV")
print("="*80)

# 1. Información básica del DataFrame
print("\n1. INFORMACIÓN BÁSICA")
print("-"*80)
print(f"Número de filas (casos): {len(df)}")
print(f"Número de columnas (variables): {len(df.columns)}")
print(f"Dimensiones: {df.shape}")

# 2. Lista de columnas
print("\n2. COLUMNAS/VARIABLES")
print("-"*80)
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

# 3. Tipos de datos
print("\n3. TIPOS DE DATOS")
print("-"*80)
print(df.dtypes)

# 4. Información de metadatos
print("\n4. METADATOS DEL ARCHIVO SPSS")
print("-"*80)
print(f"Número de variables: {meta.number_columns}")
print(f"Número de casos: {meta.number_rows}")

# 5. Etiquetas de columnas (si existen)
print("\n5. ETIQUETAS DE COLUMNAS")
print("-"*80)
if meta.column_names_to_labels:
    for var, label in meta.column_names_to_labels.items():
        print(f"{var}: {label}")
else:
    print("No hay etiquetas de columnas disponibles")

# 6. Etiquetas de valores (para variables categóricas)
print("\n6. ETIQUETAS DE VALORES (Variables Categóricas)")
print("-"*80)
if meta.variable_value_labels:
    for var, labels in meta.variable_value_labels.items():
        print(f"\n{var}:")
        for value, label in labels.items():
            print(f"  {value}: {label}")
else:
    print("No hay etiquetas de valores disponibles")

# 7. Estadísticas descriptivas
print("\n7. ESTADÍSTICAS DESCRIPTIVAS")
print("-"*80)
print(df.describe(include='all'))

# 8. Valores faltantes
print("\n8. VALORES FALTANTES")
print("-"*80)
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "No hay valores faltantes")

# 9. Primeras y últimas filas
print("\n9. MUESTRA DE DATOS - PRIMERAS 5 FILAS")
print("-"*80)
print(df.head())

print("\n10. MUESTRA DE DATOS - ÚLTIMAS 5 FILAS")
print("-"*80)
print(df.tail())

# Preparar información para JSON
data_info = {
    "archivo": file_path,
    "fecha_analisis": datetime.now().isoformat(),
    "estructura": {
        "filas": int(len(df)),
        "columnas": int(len(df.columns)),
        "dimensiones": list(df.shape)
    },
    "columnas": list(df.columns),
    "tipos_datos": {col: str(dtype) for col, dtype in df.dtypes.items()},
    "metadatos": {
        "numero_variables": meta.number_columns,
        "numero_casos": meta.number_rows,
        "etiquetas_columnas": meta.column_names_to_labels if meta.column_names_to_labels else {},
        "etiquetas_valores": {
            var: {str(k): v for k, v in labels.items()} 
            for var, labels in (meta.variable_value_labels.items() if meta.variable_value_labels else {})
        }
    },
    "estadisticas_descriptivas": {},
    "valores_faltantes": {col: int(count) for col, count in df.isnull().sum().items() if count > 0}
}

# Agregar estadísticas por columna
for col in df.columns:
    col_stats = {}
    if pd.api.types.is_numeric_dtype(df[col]):
        col_stats = {
            "tipo": "numérica",
            "media": float(df[col].mean()) if not df[col].isna().all() else None,
            "mediana": float(df[col].median()) if not df[col].isna().all() else None,
            "min": float(df[col].min()) if not df[col].isna().all() else None,
            "max": float(df[col].max()) if not df[col].isna().all() else None,
            "desviacion_std": float(df[col].std()) if not df[col].isna().all() else None,
            "valores_unicos": int(df[col].nunique())
        }
    else:
        value_counts = df[col].value_counts()
        col_stats = {
            "tipo": "categórica/texto",
            "valores_unicos": int(df[col].nunique()),
            "valor_mas_frecuente": str(df[col].mode()[0]) if not df[col].empty and len(df[col].mode()) > 0 else None,
            "frecuencia_mas_comun": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0
        }
    data_info["estadisticas_descriptivas"][col] = col_stats

# Guardar información en JSON
json_output = "./context/data_info.json"
with open(json_output, 'w', encoding='utf-8') as f:
    json.dump(data_info, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print(f"Información guardada en: {json_output}")
print("="*80)

