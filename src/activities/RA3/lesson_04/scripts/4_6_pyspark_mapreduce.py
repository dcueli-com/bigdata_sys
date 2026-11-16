# %%
# REQUIRES, IMPORTS, ETC.
# =======================
# System
# ------
import sys
import time
import importlib

# Third-party libraries (PySpark)
# -------------------------------
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import pyspark.sql.functions as F

# MODULES
# ========
# System
# --------------  
from pathlib import Path
from typing import Dict

# Custom
# Types, Defines
# --------------
import src.config.ctypes as ctp
importlib.reload(ctp)

import src.config.globals as glb
importlib.reload(glb)
from src.config.globals import *

import src.config.cerror as cer
importlib.reload(cer)
from src.config.cerror import CErr

# Helpers functions
# -----------------
import src.lib.helpers.validations as val
importlib.reload(val)

import src.lib.helpers.console as csl
importlib.reload(csl)

import src.lib.engines.bdorchestrator as bdo
importlib.reload(bdo)
from src.lib.engines.bdorchestrator import BdOrchestrator


# %%
# CHECK CHANGES OF IMPORT FILES
# ==============================
import importlib
importlib.reload(ctp)
importlib.reload(glb)
importlib.reload(cer)
importlib.reload(val)
importlib.reload(csl)
importlib.reload(bdo)

print(ctp.__file__)
print([name for name in dir(ctp)])
print("+ ")

print(glb.__file__)
print([name for name in dir(glb)])
print("+ ")

print(cer.__file__)
print([name for name in dir(cer)])
print("+ ")

print(val.__file__)
print([name for name in dir(val)])
print("+ ")

print(csl.__file__)
print([name for name in dir(csl)])
print("+ ")

print(bdo.__file__)
print([name for name in dir(bdo)])
print("+ ")



# %%
# GLOBAL VARIABLES, PATHS
# =======================
# Current file paths
# ------------------
NOTEBOOK_DIR = Path.cwd()

# Global variables definition for this notebook
# ---------------------------------------------
bUseRefraneroPhrases: bool = True
pvbPhrasesData: list[int, str] = [
  (1, 'Más vale pájaro en mano que ciento volando'),
  (2, 'Tanto va el cántaro a la fuente hasta que se rompe'),
  (3, 'Y dale con que la abuela fuma'),
  (4, 'A falta de pan, buenas son tortas'),
  (5, 'En casa del herrero cuchillo de palo'),
  (6, 'A caballo regalado no le mires el diente'),
  (7, 'De tal palo, tal astilla'),
  (8, 'A quien madruga, Dios le ayuda'),
  (9, 'En boca cerrada no entran moscas'),
  (10, 'El muerto al hoyo y el vivo al bollo')
]
bdtPhrasesData: list[int, str] = [
  (1, 'Big Data permite procesar grandes volumenes de datos en un cluster distribuido'),
  (2, 'El modelo MapReduce divide el procesamiento en la fase Map y la fase Reduce'),
  (3, 'PySpark ejecuta operaciones MapReduce en memoria dentro del ecosistema Big Data'),
  (4, 'La fase Map transforma cada frase en palabras individuales con valor uno'),
  (5, 'La fase Shuffle agrupa todas las palabras iguales antes de ejecutar Reduce'),
  (6, 'PySpark optimiza el procesamiento distribuido de datos frente al MapReduce clasico'),
  (7, 'Un cluster de Big Data escala el procesamiento de datos en paralelo con PySpark'),
  (8, 'La fase Reduce suma las ocurrencias de cada palabra agrupada en el Shuffle'),
  (9, 'MapReduce y PySpark son herramientas fundamentales en la arquitectura Big Data'),
  (10, 'El conteo de palabras demuestra como funciona el flujo Map Shuffle y Reduce en PySpark')
]


# %%
# PYSPARK MAPREDUCE, 4.6.1 CREATE PHRASES DATASET (10 SENTENCES)
# ==============================================================
tInit: float = time.perf_counter()
csl.SectionBegin("PYSPARK MAPREDUCE, 4.6.1 CREATE PHRASES DATASET\n+ Creating PySpark DataFrame with 10 Sentences", 0)

try:
  # Define explicit schema for the sentences dataset
  phrData: list[int, str] = pvbPhrasesData if bUseRefraneroPhrases else bdtPhrasesData
  phrSchema: StructType = StructType([
    StructField('id', IntegerType(), False),
    StructField('sentence', StringType(), False)
  ])

  # Create PySpark DataFrame through BdOrchestrator
  dfPhrases: SparkDataFrame = BdOrchestrator.CreateDataFrame('pyspark', phrData, phrSchema, 'M3_RA3_4_Ex6')['data']

except Exception as e:
  csl.SectionErrEndAndExit(e.args[0], tInit)

csl.SectionEnd(0)

# %%
# PYSPARK MAPREDUCE, 4.6.2a MAP PHASE (SPLIT WORDS & ASSIGN 1)
# ============================================================
tInit: float = time.perf_counter()
csl.SectionBegin("PYSPARK MAPREDUCE, 4.6.2a MAP PHASE\n+ Splitting sentences into words and assigning value 1", 0)

try:
  # Requirement 2a: Map phase via BdOrchestrator
  dfMapped: SparkDataFrame = BdOrchestrator.MapWords(
    'pyspark',
    dfPhrases,
    'sentence',
    'word',
    'count'
  )['data']

except Exception as e:
  csl.SectionErrEndAndExit(e.args[0], tInit)

csl.SectionEnd(0)

# %%
# PYSPARK MAPREDUCE, 4.6.2b SHUFFLE PHASE (GROUP IDENTICAL WORDS)
# ===============================================================
tInit: float = time.perf_counter()
csl.SectionBegin("PYSPARK MAPREDUCE, 4.6.2b SHUFFLE PHASE\n+ Grouping identical words and collecting occurrences", 0)

try:
  # Requirement 2b: Shuffle phase via BdOrchestrator
  dfShuffled: SparkDataFrame = BdOrchestrator.ShuffleWords(
    'pyspark',
    dfMapped,
    'word',
    'count',
    'occurrences',
    pPreviewRows=5
  )['data']

except Exception as e:
  csl.SectionErrEndAndExit(e.args[0], tInit)

csl.SectionEnd(0)

# %%
# PYSPARK MAPREDUCE, 4.6.2c & 4.6.3 REDUCE PHASE (SUM OCCURRENCES & WORD FREQUENCY)
# =================================================================================
tInit: float = time.perf_counter()
csl.SectionBegin("PYSPARK MAPREDUCE, 4.6.2c REDUCE PHASE\n+ Summing word occurrences to obtain final frequencies", 0)

try:
  # Requirement 2c & 3: Reduce phase via BdOrchestrator
  dfReduced: SparkDataFrame = BdOrchestrator.ReduceWords(
    'pyspark',
    dfShuffled,
    'word',
    'occurrences',
    'frequency',
    pPreviewRows=5
  )['data']

except Exception as e:
  csl.SectionErrEndAndExit(e.args[0], tInit)

csl.SectionEnd(0)


