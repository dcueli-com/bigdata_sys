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


# %%
# REQUIRES
# ========
# System libraries
# ----------------
import time

# Third-party libraries
# ----------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# MODULES
# ========
# System modules
# --------------
from typing import Union
from pathlib import Path
from datetime import datetime

# Custom modules
# Defines
# -------
from src.config.globals import *

# Helpers functions
# -----------------
from src.helpers import funcs as hlp



# %%
# CHECK CHANGES ONF IMPORT FILES
# ==============================
import importlib
importlib.reload(hlp)

print(hlp.__file__)
print(hasattr(hlp, "SectionBegin"))
print([name for name in dir(hlp) if "Section" in name])

# %%
# PATHS
# =====
# CURRENT FILE PATH
NOTEBOOK_DIR = Path.cwd()
DATA_DIR = (NOTEBOOK_DIR.parent / "data").resolve()

# Global variables definition for this notebook
# ---------------------------------------------
# dataset:str = "../data/ventas_con_problemas.csv"
dataset: str = DATA_DIR / "ventas_con_problemas.csv"

# Pandas dataframe to hold the dataset
df: pd.DataFrame

# %%
# LOAD SOURCE DATASET (from CSV file)
# ===================================
hlp.SectionBegin(f"DATASET PATH: \n{dataset}", 0)
hlp.SectionBreak(0, 0)

try:
  df = pd.read_csv(dataset)
  print(f"File loaded successfully. Total of original rows: {len(df)}")
  print(f"First 5 rows of the dataset:")
  print(df.head())
  
except FileNotFoundError:
  print(f"Error: Please, check path. \n'{dataset}'")
  print(f"Error: File not found.")

hlp.SectionEnd(0)


# %%
# DATA CLEANING
# =============
# 1. CHECK OF NULL VALUES
# -----------------------
tInit: float = time.time()

# CheckNullValues
# ------------------------
# Totalize and print the number of null values per column in the dataset, 
# as well as the total number of rows with at least one null value.
# 
# @param pPf: pd.DataFrame The pandas dataframe to check for null values.
# @return None
def CheckNullValues(pPf: pd.DataFrame) -> None:
  # Total null values per column in the dataset
  nullValuesPerColumn: int = pPf.isnull().sum()
  print("Null values per column:")
  print(nullValuesPerColumn)
  hlp.SectionBreak(0,0)

  # Total rows with at least one null value
  rowsWithNulls: pd.DataFrame = pPf[pPf.isnull().any(axis=1)]
  print(f"Total rows with at least one null value: \n{len(rowsWithNulls)}")

# Execute script
hlp.SectionBegin("CHECK OF NULL VALUES", 0)
hlp.SectionBreak(0,0)

CheckNullValues(df)
hlp.SectionBreak(0,0)

tEnd: float = time.time()
print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
hlp.SectionEnd(0)

# %%
# DATA CLEANING
# =============
# 2. CHECK OF INVALID DATE VALUES
# -------------------------------
tInit: float = time.time()

# CheckInvalidDates
# -----------------
# Try to convert the date column to proper datetime format
# errors='coerce' converts all invalid dates to NaN
# 
# @param string pColumn Name of the column to convert to proper date format
# @return None
def CheckInvalidDates(pPf: pd.DataFrame, pColumn:str = 'fecha') -> None:
  properDateTime: pd.Series = pd.to_datetime(pPf[pColumn], errors='coerce')
  
  # How many dates were successfully converted and how many failed
  totRows: int = len(pPf)
  totProperDates: int = properDateTime.notna().sum()
  totInvalidDates: int = properDateTime.isna().sum()

  print(f"Total rows: {totRows}")
  print(f"Valid dates converted successfully: {totProperDates}")
  print(f"Invalid or null dates detected: {totInvalidDates}")

  # Show some of the rows with dates that failed
  print("\nExamples of rows with invalid dates:")
  print(df[properDateTime.isna()][pColumn].head(10))  
  
# Execute script
hlp.SectionBegin("CHECK OF INVALID DATE VALUES", 0)
print("+ Summary of conversion date column state:")
hlp.SectionBreak(0,0)

CheckInvalidDates(df, "fecha")
hlp.SectionBreak(0,0)

tEnd: float = time.time()
print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
hlp.SectionEnd(0)

# %%
# DATA CLEANING
# =============
# 3. CHECK OF DUPLICATED VALUES
# -----------------------------
tInit: float = time.time()

# CheckDuplicatedValues
# ---------------------
# Count exactly how many rows are duplicated, taking all columns in account
# 
# @param pd.DataFrame pPf The pandas dataframe to check
# @return None
def CheckDuplicatedValues(pPf: pd.DataFrame) -> None:
  cols:list[str] = ['fecha', 'producto', 'cantidad', 'precio_unitario', 'total']
  totDupl: int = pPf.duplicated(subset=cols).sum()  

  # Show a little snapshot
  if totDupl > 0:
    print(f"Snapshot of duplicated rows: ({totDupl})")
    hlp.nbsp()
    
    # keep=False show all instances of duplicates
    rowsDupl: pd.DataFrame = pPf[pPf.duplicated(keep=False)]
    print(rowsDupl.sort_values(by=cols)[cols].head(5))
  else:
    print("No duplicated rows found")
  
hlp.SectionBegin("CHECK OF DUPLICATED VALUES", 0)
print("+ Summary of fully duplicate rows found")
hlp.SectionBreak(0,0)
CheckDuplicatedValues(df)
hlp.SectionBreak(0,0)

tEnd: float = time.time()
print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
hlp.SectionEnd(0)

# %%
# DATA CLEANING
# =============
# 4. CHECK OF TOTAL COLUMN VALUE
# ------------------------------
tInit: float = time.time()

# CheckTotalColumnValues
# ----------------------
# Convert columns to numeric and check for negative or zero values
# 
# @param pd.DataFrame pPf The pandas dataframe to check
# @return None
def CheckTotalColumnValues(pPf: pd.DataFrame) -> None:
  # Ensure numeric conversion
  pPf['cantidad'] = pd.to_numeric(pPf['cantidad'], errors='coerce')
  pPf['precio_unitario'] = pd.to_numeric(pPf['precio_unitario'], errors='coerce')
  pPf['total'] = pd.to_numeric(pPf['total'], errors='coerce')

  # Get the expected Total
  pPf['total_temp'] = pPf['cantidad'] * pPf['precio_unitario']

  # Filter rows where both total amountnot do not match (using np.isclose with tolerance of 0.01)
  # Only check rows where any columns are null
  maskNoNull = pPf['cantidad'].notna() & pPf['precio_unitario'].notna() & pPf['total'].notna()
  inconsistencies = pPf[maskNoNull & (~np.isclose(pPf['total_temp'], pPf['total'], atol=0.01))]

  print(f"Rows with different totals: {len(inconsistencies)}")
  hlp.SectionBreak(0,0)
  print("Snapshot of rows with inconsistent total calculation:")
  print(inconsistencies[['producto', 'cantidad', 'precio_unitario', 'total', 'total_temp']].head(10))
  
hlp.SectionBegin("CHECK OF TOTAL COLUMN VALUE", 0)
print("+ Summary of rows with incorrect Total amount:")
hlp.SectionBreak(0,0)
CheckTotalColumnValues(df)
hlp.SectionBreak(0,0)

tEnd: float = time.time()
print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
hlp.SectionEnd(0)


# %%
# DATA CLEANING
# =============
# 5. CHECK OF NEGATIVE OR ZERO NUMERIC VALUES
# -------------------------------------------
tInit: float = time.time()

# CheckNumericValues
# -------------------
# Convert columns to numeric and check for negative or zero values
# 
# @param pd.DataFrame pPf The pandas dataframe to check
# @return None
def CheckNumericValues(pPf: pd.DataFrame) -> None:
  # dfTmp: pd.DataFrame
  # Convert to numeric by forcing errors to NaN values for security
  pPf['cantidad_num'] = pd.to_numeric(pPf['cantidad'], errors='coerce')
  pPf['precio_unitario_num'] = pd.to_numeric(pPf['precio_unitario'], errors='coerce')
  pPf['total_num'] = pd.to_numeric(pPf['total'], errors='coerce')

  # Identify rows with values <= 0
  negAmount = pPf[pPf['cantidad_num'] <= 0]
  negPrices = pPf[pPf['precio_unitario_num'] <= 0]
  negTotales = pPf[pPf['total_num'] <= 0]
  negRows = pPf[(pPf['cantidad_num'] <= 0) | (pPf['precio_unitario_num'] <= 0) | (pPf['total_num'] <= 0)]

  # Show summary of results
  print(f"Rows with any negative or zero values: {len(negRows)}")
  print(f"Rows with [precio_unitario <= 0]:      {len(negPrices)}")
  print(f"Rows with [cantidad <= 0]:             {len(negAmount)}")
  print(f"Rows with [total <= 0]:                {len(negTotales)}")

  hlp.SectionBreak(0,0)
  print("Snapshot of rows with negative amounts or quantities:")
  print(negRows[['fecha', 'producto', 'cantidad', 'precio_unitario', 'total']].head(10))
  
hlp.SectionBegin("CHECK OF NEGATIVE OR ZERO NUMERIC VALUES", 0)
print("+ Summary of rows with weird numeric values:")
hlp.SectionBreak(0,0)
CheckNumericValues(df)
hlp.SectionBreak(0,0)

tEnd: float = time.time()
print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
hlp.SectionEnd(0)




# %%
# DATA CLEANING
# =============
# 6. CHECK OF OUTLIERS VALUES
# ---------------------------
tInit: float = time.time()

# CheckOutliersValues
# -------------------
# Convert columns ensuring numeric values and show the biggest 
# values to detect prices or quantities that makes no sense
# 
# @param pd.DataFrame pPf The pandas dataframe to check
# @return None
def CheckOutliersValues(pPf: pd.DataFrame) -> None:
  # Ensure numeric conversion
  pPf['qty_temp'] = pd.to_numeric(pPf['cantidad'], errors='coerce')
  pPf['prc_temp'] = pd.to_numeric(pPf['precio_unitario'], errors='coerce')
  
  # Show the highest values
  highestQty = pPf.nlargest(5, 'qty_temp')
  print(f"Quantity highest values: {len(highestQty)}")
  hlp.nbsp()
  print(highestQty[['fecha', 'producto', 'cantidad', 'precio_unitario', 'total']].head(5))
  hlp.SectionBreak(0,0)

  highestPrc = pPf.nlargest(5, 'prc_temp')
  print(f"Price highest values: {len(highestPrc)}")
  hlp.nbsp()
  print(highestPrc[['fecha', 'producto', 'cantidad', 'precio_unitario', 'total']].head(5))
  
hlp.SectionBegin("CHECK OF OUTLIERS VALUES", 0)
print("+ Summary of rows with possible outlier values on Price and Quantity:")
hlp.SectionBreak(0,0)
CheckOutliersValues(df)
hlp.SectionBreak(0,0)

tEnd: float = time.time()
print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
hlp.SectionEnd(0)
