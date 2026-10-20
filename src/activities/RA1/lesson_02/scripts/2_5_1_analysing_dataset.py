# Original statement of the exercise:
# ===================================
# EJERCICIO 5:  Una empresa de comercio electrónico está implementando un sistema de análisis de ventas en tiempo real. Como parte de este proyecto, necesitan asegurar la calidad de los datos que alimentarán su sistema. Se te ha proporcionado un archivo CSV llamado 'ventas_con_problemas.csv' que contiene datos de ventas de los últimos 30 días. Este archivo contiene varios problemas de calidad de datos que deben ser identificados y corregidos.Tu tarea es desarrollar un script en Python que realice las siguientes operaciones:
# 1. Carga el archivo CSV y realiza una exploración inicial de los datos.
# 2. Identifica y maneja los siguientes problemas de calidad de datos:
#    - Valores nulos en campos críticos (fecha, producto, cantidad, precio_unitario, total)
#    - Fechas inválidas
#    - Valores negativos en campos numéricos (cantidad, precio_unitario, total)
#    - Inconsistencias en el cálculo del total (comparando cantidad * precio_unitario con el total registrado)
#    - Valores atípicos (outliers) en campos numéricos
#    - Duplicados
# 3.	Implementa técnicas de limpieza de datos para corregir o eliminar los problemas identificados.
# 4.	Genera un informe que incluya:
#    - Número de filas originales vs. número de filas después de la limpieza
#    - Cantidad de problemas identificados y corregidos por cada tipo
#    - Estadísticas descriptivas de los datos limpios (media, mediana, desviación estándar) para campos numéricos
# 5.	Crea visualizaciones que ayuden a entender la distribución de los datos y los efectos de la limpieza.
# 6.	Guarda los datos limpios en un nuevo archivo CSV.
#
# Módulos que pueden usar: pandas, numpy, matplotlib, seaborn


# REQUIRES
# ========
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Defines
# -------
from src.config.globals import *

# Helpers functions
# -----------------
from src.helpers import funcs as hlp

# PATHS
# =====
# CURRENT FILE PATH
CURR_EXECERCISES_FILES_PATH = Path(__file__).resolve()
DATA_DIR = CURR_EXECERCISES_FILES_PATH.parent / "data"

# Carga del archivo CSV del origen de datos
# dataset:str = "../data/ventas_con_problemas.csv"
dataset:str = DATA_DIR / "ventas_con_problemas.csv"

# Definimos las variabes previamente
df: pd.DataFrame

print(f"+ =========================================================")
print(f"+ DATASET PATH: \n{dataset}")
print(f"+ ---------------------------------------------------------")
try:
  df = pd.read_csv(dataset)
  print(f"File loaded successfully. Total of original rows: {len(df)}")
  print(f"First 5 rows of the dataset:")
  print(df.head())
  
except FileNotFoundError:
  print(f"Error: Please, check path. \n'{dataset}'")
  print(f"Error: File not found.")

hlp.LineBreak(1)

# # 2. Conversión a tipos numéricos seguros
# df['cantidad_num'] = pd.to_numeric(df['cantidad'], errors='coerce')
# df['precio_num'] = pd.to_numeric(df['precio_unitario'], errors='coerce')
# df['total_num'] = pd.to_numeric(df['total'], errors='coerce')

# # 3. Validación estricta de fechas (Año 2026 válido)
# def parsear_fecha_estricta(val):
#     if pd.isna(val): return pd.NaT
#     try:
#         dt = pd.to_datetime(str(val).strip(), errors='raise')
#         return dt if dt.year == 2026 else pd.NaT
#     except:
#         return pd.NaT

# df['fecha_limpia'] = df['fecha'].apply(parsear_fecha_estricta)

# # 4. Filtrado de registros inválidos, negativos, nulos y outliers extremos
# df_clean = df.dropna(subset=['fecha_limpia', 'producto', 'cantidad_num', 'precio_num', 'total_num']).copy()
# df_clean = df_clean[
#     (df_clean['cantidad_num'] > 0) & (df_clean['cantidad_num'] <= 50) &
#     (df_clean['precio_num'] > 0) & (df_clean['precio_num'] <= 500) &
#     (df_clean['total_num'] > 0)
# ]

# # 5. Validación de consistencia aritmética (cantidad * precio_unitario == total)
# df_clean['total_calc'] = df_clean['cantidad_num'] * df_clean['precio_num']
# df_clean = df_clean[np.isclose(df_clean['total_calc'], df_clean['total_num'], atol=1.0)]

# # 6. Estadísticas descriptivas de los datos limpios
# stats = df_clean[['cantidad_num', 'precio_num', 'total_num']].agg(['mean', 'median', 'std'])
# print(stats)

# # 7. Guardar el resultado en un nuevo archivo CSV limpio
# df_export = df_clean[['fecha_limpia', 'producto', 'cantidad_num', 'precio_num', 'total_num']].copy()
# df_export.columns = ['fecha', 'producto', 'cantidad', 'precio_unitario', 'total']
# df_export.to_csv('ventas_limpias_v2.csv', index=False)