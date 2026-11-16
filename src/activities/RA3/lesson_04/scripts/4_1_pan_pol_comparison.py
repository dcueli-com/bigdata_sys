# %%
# REQUIRES, IMPORTS, ETC.
# =======================
# System
# ------
# import sys
import time
import importlib

# Third-party libraries
# ----------------------
import pandas as pd
import polars as pl

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

# Helpers functions
# -----------------
import src.lib.helpers.validations as val
importlib.reload(val)
import src.lib.helpers.console as csl
importlib.reload(csl)
import src.lib.helpers.charts as cht
importlib.reload(cht)
import src.lib.engines.bdorchestrator as bdo
importlib.reload(bdo)
from src.lib.engines.bdorchestrator import BdOrchestrator


# %%
# CHECK CHANGES OF IMPORT FILES
# ==============================
import importlib
importlib.reload(ctp)
importlib.reload(csl)
importlib.reload(cht)
importlib.reload(val)
importlib.reload(bdo)

print(csl.__file__)
print([name for name in dir(ctp)])
print("+ ")

print(csl.__file__)
print([name for name in dir(csl)])
print("+ ")

print(cht.__file__)
print([name for name in dir(cht)])
print("+ ")

print(val.__file__)
print([name for name in dir(val)])

print(bdo.__file__)
print([name for name in dir(bdo)])

# %%
# GLOBAL VARIABLES, PATHS
# =======================
# Current file paths
# ------------------
NOTEBOOK_DIR = Path.cwd()
DATA_DIR = (NOTEBOOK_DIR.parent / "data").resolve()
ML20_DIR = (NOTEBOOK_DIR.parent / "data" / "ml-20m").resolve()

# Global variables definition for this notebook
# ---------------------------------------------
mvDataset: str = ML20_DIR / "movies.csv"
rtDataset: str = ML20_DIR / "ratings.csv"

# Pandas dataframe to hold the dataset
df: pd.DataFrame
# Algorithm result
res: Dict[str, any]

# %%
# LIBRARIES COMPARISON, 4.1.1 LOAD SOURCE DATASET (from CSV file)
# ===============================================================
tInit: float = time.time()
csl.SectionBegin("LIBRARIES COMPARISON, 4.1.1 LOAD SOURCE DATASET (from CSV file)\n+ Loading Movies & Ratings Datasets", 0)

try:
  # a. PANDAS::LOAD DATASET
  mvDfPd = BdOrchestrator.CleanMoviesData('pandas', 
    BdOrchestrator.LoadDataset('pandas', str(mvDataset), pPrintResult=False)['data'], 3
  )['data']
  rtDfPd: pd.DataFrame = BdOrchestrator.LoadDataset('pandas', str(rtDataset))['data']

  # b. POLARS::LOAD DATASET
  mvDfPl = BdOrchestrator.CleanMoviesData('polars', 
    BdOrchestrator.LoadDataset('polars', str(mvDataset), pPrintResult=False)['data'], 3
  )['data']
  rtDfPl: pl.DataFrame = BdOrchestrator.LoadDataset('polars', str(rtDataset))['data']

except Exception as e:
  csl.SectionErrEndAndExit(e.args[0], tInit)

# %%
# LIBRARIES COMPARISON, 4.1.2a BASIC OPERATIONS: FILTERING
# =========================================================
csl.SectionBegin("LIBRARIES COMPARISON, 4.1.2a FILTERING\n+ Movies (2000 <= year) & Ratings (4 <= rating)", 0)

try:
  # a. PANDAS::FILTER & JOIN
  tInitPd: float = time.perf_counter()
  fltDfPd: pd.DataFrame = pd.merge(
    BdOrchestrator.FilterData('pandas', mvDfPd, 'year', '>=', 2000, pPrintResult=False)['data'], 
    BdOrchestrator.FilterData('pandas', rtDfPd, 'rating', '>=', 4, pPrintResult=False)['data'], 
    on='movieId', how='inner'
  )

  csl.SectionBreak(0, 0)
  print(f"Executing operation with PANDAS...")
  csl.nbsp()
  print(fltDfPd.head(3))
  csl.nbsp()
  print(f"Filtered successfully. Dataset total rows: {len(fltDfPd)}")
  print(f"Execution time: {time.perf_counter() - tInitPd:.4f} seconds")

  # b. POLARS::FILTER & JOIN
  tInitPl: float = time.perf_counter()
  fltDfPl: pl.DataFrame = BdOrchestrator.FilterData('polars', mvDfPl, 'year', '>=', 2000, pPrintResult=False)['data'].join(
     BdOrchestrator.FilterData('polars', rtDfPl, 'rating', '>=', 4, pPrintResult=False)['data'], on='movieId', how='inner'
  )

  csl.SectionBreak(0, 0)
  print(f"Executing operation with POLARS...")
  csl.nbsp()
  print(fltDfPl.head(3))
  csl.nbsp()
  print(f"Filtered successfully. Dataset total rows: {len(fltDfPl)}")
  print(f"Execution time: {time.perf_counter() - tInitPl:.4f} seconds")

except Exception as e:
  csl.SectionErrEndAndExit(e.args[0], tInit)

csl.SectionEnd(0)

# %%
# LIBRARIES COMPARISON, 4.1.2b BASIC OPERATIONS: SORTING
# ======================================================
tInit: float = time.time()
sortCols: list[str] = ['year', 'rating', 'movieId', 'userId']
sortDirs: list[bool] = [False, False, True, True]

csl.SectionBegin( f"LIBRARIES COMPARISON, 4.1.3 SORTING\n+ Sort by: {sortCols} | Ascending: {sortDirs}", 0)

try:

  # a. PANDAS::SORT DATA
  srtDfPd: pd.DataFrame = BdOrchestrator.SortData(
    'pandas',
    fltDfPd,
    sortCols,
    sortDirs,
    pPreviewRows=3
  )['data']

  # b. POLARS::SORT DATA
  srtDfPl: pl.DataFrame = BdOrchestrator.SortData(
    'polars',
    fltDfPl,
    sortCols,
    sortDirs,
    pPreviewRows=3
  )['data']

except Exception as e:
  csl.SectionErrEndAndExit(e.args[0], tInit)

csl.SectionEnd(0)

# %%
# LIBRARIES COMPARISON, 4.1.2c BASIC OPERATIONS: AGGREGATION
# =========================================================
tInit: float = time.time()
groupCols: list[str] = ['year', 'movieId', 'title']
targetCol: str = 'rating'
aggOperation: str = 'mean'
aliasCol: str = 'avg_rating'

csl.SectionBegin(f"LIBRARIES COMPARISON, 4.1.2c AGGREGATION\n+ Group by: {groupCols}\n+ Operation: {aggOperation}('{targetCol}') as '{aliasCol}'", 0)

try:
  # a. PANDAS::AGGREGATE DATA
  aggDfPd: pd.DataFrame = BdOrchestrator.AggregateData(
    'pandas',
    srtDfPd,
    groupCols,
    targetCol,
    aggOperation,
    aliasCol,
    pPreviewRows=3
  )['data']

  # b. POLARS::AGGREGATE DATA
  aggDfPl: pl.DataFrame = BdOrchestrator.AggregateData(
    'polars',
    srtDfPl,
    groupCols,
    targetCol,
    aggOperation,
    aliasCol,
    pPreviewRows=3
  )['data']

except Exception as e:
  csl.SectionErrEndAndExit(e.args[0], tInit)

csl.SectionEnd(0)


