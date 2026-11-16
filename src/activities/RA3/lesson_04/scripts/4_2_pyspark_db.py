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
minWeight: int = 70
maxHeight: int = 180


# %%
# PYSPARK DATABASE, 4.2(.1, .2, .3, .4) CREATE DATAFRAME WITH SCHEMA (10 PEOPLE)
# ================================================================
tInit: float = time.perf_counter()
csl.SectionBegin("PYSPARK DATABASE, 4.2(.1, .2, .3, .4) CREATE DATAFRAME\n+ Initializing SparkSession, Schema, and 10 Fictional Records", 0)

try:
  # Requirement 1
  # Initialize SparkSession in local mode
  spark: SparkSession = (
    SparkSession.builder
    .appName('RA3_Lesson04_Ex2_PeopleDB')
    .master('local[*]')
    .getOrCreate()
  )
  spark.sparkContext.setLogLevel('ERROR')

  # Reqs 2 & 3
  # Define explicit schema with StringType and IntegerType
  peopleSchema: StructType = StructType([
    StructField('Nombre', StringType(), False),
    StructField('Edad', IntegerType(), False),
    StructField('Peso', IntegerType(), False),
    StructField('Talla', IntegerType(), False)
  ])

  # Req 4
  # Define 10 fictional people records: (Nombre, Edad, Peso [kg], Talla [cm])
  peopleData: list[tuple[str, int, int, int]] = [
    ('Ruben Gasque', 34, 78, 175),    # Matches: 70 < 78 and 180 > 175
    ('Nil Redón', 28, 62, 168),       # Weight <= 70
    ('Sergi Guillem', 41, 85, 184),   # Height >= 180
    ('Evelyn Cruz', 31, 74, 172),     # Matches: 70 < 74 and 180 > 172
    ('Angel Sardinha', 25, 70, 176),  # Boundary case: Weight == 70 (not > 70)
    ('Domenica Nieto', 39, 76, 180),  # Boundary case: Height == 180 (not < 180)
    ('Nacho Pérez', 45, 82, 178),     # Matches: 70 < 82 and 180 > 178
    ('Elba González', 22, 58, 164),   # Weight <= 70
    ('David Cueli', 48, 101, 190),    # Height >= 180
    ('Clara Sánchez', 29, 67, 171)    # Weight <= 70
  ]

  # Create PySpark DataFrame and perform initial exploration
  dfPeople: SparkDataFrame = spark.createDataFrame(data=peopleData, schema=peopleSchema)

  csl.SectionBreak(0, 0)
  print("PySpark DataFrame created successfully.")
  print(f"Total records: {dfPeople.count()}")
  csl.nbsp()
  print("DataFrame Schema:")
  dfPeople.printSchema()
  print("Initial 10 fictional records:")
  dfPeople.show(10, truncate=False)
  print(f"Execution time: {time.perf_counter() - tInit:.4f} seconds")

except Exception as e:
  CErr.Raise(500,
    sys._getframe(0).f_code.co_name,
    "Error creating PySpark DataFrame: %s",
    (str(e),),
    e
  )

csl.SectionEnd(0)


# %%
# PYSPARK DATABASE, 4.2(.5, .6) FILTER DATA (Peso > 70 kg AND Talla < 180 cm)
# =====================================================================
tInit: float = time.perf_counter()
csl.SectionBegin(f"PYSPARK DATABASE, 4.2(.5, .6) FILTERING\n+ Criteria: Peso > {minWeight} kg AND Talla < {maxHeight} cm", 0)

try:
  
  # Reqs 5 & 6
  # Filter people with Peso > 70 and Talla < 180 via BdOrchestrator
  dfWeightFlt: SparkDataFrame = BdOrchestrator.FilterData(
    'pyspark',
    dfPeople,
    'Peso',
    '>',
    minWeight,
    pPrintResult=False
  )['data']

  dfPeopleFlt: SparkDataFrame = BdOrchestrator.FilterData(
    'pyspark',
    dfWeightFlt,
    'Talla',
    '<',
    maxHeight,
    pPrintResult=True,
    pPreviewRows=10
  )['data']

except Exception as e:
  csl.SectionErrEndAndExit(e.args[0], tInit)

csl.SectionEnd(0)


