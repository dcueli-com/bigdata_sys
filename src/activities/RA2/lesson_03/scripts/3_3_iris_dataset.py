# Original statement of the exercise:
# ===================================
# EJERCICIO 3: Análisis del Dataset Iris:
# 
# 1.	Carga el dataset Iris: Carga el dataset Iris usando pandas.read_csv().
# 2.	Histograma multivariable: Crea un histograma que muestre la distribución de cada una de las cuatro características (sepal_length, sepal_width, petal_length, petal_width) para cada especie.
# 3.	Diagrama de dispersión con pares: Utiliza sns.pairplot() para crear un diagrama de dispersión que muestre la relación entre cada par de características. Agrega color a los puntos para diferenciar las especies.
# 4.	Mapa de calor de correlación: Crea un mapa de calor que muestre la correlación entre las diferentes características del dataset.
# 5.	Gráfico de violín: Crea un gráfico de violín (violinplot) para cada una de las características (sepal_length, sepal_width, petal_length, petal_width), agrupado por especie.
# 
# Extrae conclusiones sobre el porque de los resultados obtenidos. 

# %%
# REQUIRES, IMPORTS, ETC.
# =======================
# System
# ------
import time

# Third-party libraries
# ----------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# MODULES
# ========
# System
# --------------
from pathlib import Path
from typing import Dict

# Custom
# Defines
# -------
from src.config.globals import *

# Helpers functions
# -----------------
import src.helpers.validations as val
import src.helpers.console as csl
import src.helpers.charts as cht

# %%
# CHECK CHANGES ONF IMPORT FILES
# ==============================
import importlib
importlib.reload(csl)
importlib.reload(cht)
importlib.reload(val)

print(csl.__file__)
print([name for name in dir(csl)])
print("+ ")

print(cht.__file__)
print([name for name in dir(cht)])
print("+ ")

print(val.__file__)
print([name for name in dir(val)])

# %%
# GLOBAL VARIABLES, PATHS
# =======================
# Current file paths
# ------------------
NOTEBOOK_DIR = Path.cwd()
DATA_DIR = (NOTEBOOK_DIR.parent / "data").resolve()

# Global variables definition for this notebook
# ---------------------------------------------
dataset: str = DATA_DIR / "iris.csv"

# Pandas dataframe to hold the dataset
df: pd.DataFrame
# Algorithm result
res: dict[str, any]
# Kind of sepals
sepalFeatures: dict[str] = [
  "sepal_length",
  "sepal_width",
  "petal_length",
  "petal_width"
]

# %%
# DATA ANALYSIS IRIS, 1. LOAD SOURCE DATASET (from CSV file)
# ==========================================================
csl.SectionBegin(f"DATA ANALYSIS IRIS, 1. LOAD SOURCE DATASET (from CSV file)\nDATASET PATH: \n{dataset}", 0)
csl.SectionBreak(0, 0)

try:
  df = pd.read_csv(dataset)
  print(f"File loaded successfully. Total of original rows: {len(df)}")
  print(f"First 5 rows of the dataset:")
  print(df.head())
  
except FileNotFoundError:
  print(f"Error: Please, check path. \n'{dataset}'")
  print(f"Error: File not found.")

csl.SectionEnd(0)


# %%
# DATA ANALYSIS IRIS, 2. MULTIVAR HISTOGRAM
# =========================================
tInit: float = time.time()

# MultivarHistogram
# -----------------
# Show the multivariable histogram plot by species
# 
# @param pDf: pd.DataFrame The pandas dataframe.
# @return None
def MultivarHistogram(pDf: pd.DataFrame) -> list[dict]:
  fig, axes = plt.subplots(2, 2, figsize=(14, 10))

  for feature, ax in zip(sepalFeatures, axes.flatten()):
    sns.histplot(
      data=pDf,
      x=feature,
      hue="species",
      bins=15,
      multiple="layer",
      alpha=0.5,
      ax=ax
    )

    ax.set_title(f"Distribution of {feature}")
    ax.set_xlabel(feature)
    ax.set_ylabel("Frequency")

  fig.suptitle("Iris dataset: feature distributions by species", fontsize=14)
  plt.tight_layout()
  plt.show()
  
  return {'bOk': True}

# Execute script
csl.SectionBegin("DATA ANALYSIS IRIS, 2. MULTIVAR HISTOGRAM", 0)
csl.SectionBreak(0,0)

res = MultivarHistogram(df)
if not res['bOk']: 
  print(f"Error({res['err']['code']}): In {res['err']['whre']}:")
  print(res['err']['mssg'])

csl.SectionBreak(0,0)
tEnd: float = time.time()
print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
csl.SectionEnd(0)

# %%
# DATA ANALYSIS IRIS, 3. PAIRPLOT WITH RELATIONSHIPS BETWEEN FEATURES
# ===================================================================
tInit: float = time.time()

# PairPlot
# --------
# Show the plot with relationships between features 
# 
# @param pDf: pd.DataFrame The pandas dataframe
# @return None
def PairPlot(pDf: pd.DataFrame) -> list[dict]:
  sns.pairplot(
    data=pDf,
    vars=sepalFeatures,
    hue="species",
    diag_kind="hist"
  ).figure.suptitle("Iris dataset: relationships between features", y=1.02)
  
  plt.show()
  
  return {'bOk': True}

# Execute script
csl.SectionBegin("DATA ANALYSIS IRIS, 3. PAIRPLOT WITH RELATIONSHIPS BETWEEN FEATURES", 0)
csl.SectionBreak(0,0)

res = PairPlot(df)
if not res['bOk']: 
  print(f"Error({res['err']['code']}): In {res['err']['whre']}:")
  print(res['err']['mssg'])

csl.SectionBreak(0,0)
tEnd: float = time.time()
print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
csl.SectionEnd(0)

# %%
# DATA ANALYSIS IRIS, 4. CORRELATION HEATMAP
# ==========================================
tInit: float = time.time()

# CorrelationHeatmap
# ------------------
# Show the heatmap plot with correlations between features 
# 
# @param pDf: pd.DataFrame The pandas dataframe
# @return None
def CorrelationHeatmap(pDf: pd.DataFrame) -> list[dict]:
  correlation: pd.DataFrame = pDf[sepalFeatures].corr()

  fig, ax = plt.subplots(figsize=(14, 8))

  sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    vmin=-1,
    vmax=1,
    ax=ax
  )

  ax.set_title("Iris dataset: feature correlation")

  plt.tight_layout()
  plt.show()
  
  return {'bOk': True}

# Execute script
csl.SectionBegin("DATA ANALYSIS IRIS, 4. CORRELATION HEATMAP", 0)
csl.SectionBreak(0,0)

res = CorrelationHeatmap(df)
if not res['bOk']: 
  print(f"Error({res['err']['code']}): In {res['err']['whre']}:")
  print(res['err']['mssg'])

csl.SectionBreak(0,0)
tEnd: float = time.time()
print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
csl.SectionEnd(0)

# %%
# DATA ANALYSIS IRIS, 5. VIOLIN PLOTS OF FEATURES BY SPECIES
# ==========================================================
tInit: float = time.time()

# ViolinplotBySpecies
# -------------------
# Show the plot with relationships between features 
# 
# @param pDf: pd.DataFrame The pandas dataframe
# @return None
def ViolinplotBySpecies(pDf: pd.DataFrame) -> list[dict]:
  fig, axes = plt.subplots(2, 2, figsize=(14, 6))

  for feature, ax in zip(sepalFeatures, axes.flatten()):
    sns.violinplot(
      data=df,
      x="species",
      y=feature,
      ax=ax
    )

    ax.set_title(f"{feature} by species")
    ax.set_xlabel("Species")
    ax.set_ylabel(feature)

  fig.suptitle("Iris dataset: feature distributions by species", fontsize=14)

  plt.tight_layout()
  plt.show()
  
  return {'bOk': True}

# Execute script
csl.SectionBegin("DATA ANALYSIS IRIS, 5. VIOLIN PLOTS OF FEATURES BY SPECIES", 0)
csl.SectionBreak(0,0)

res = ViolinplotBySpecies(df)
if not res['bOk']: 
  print(f"Error({res['err']['code']}): In {res['err']['whre']}:")
  print(res['err']['mssg'])

csl.SectionBreak(0,0)
tEnd: float = time.time()
print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
csl.SectionEnd(0)


