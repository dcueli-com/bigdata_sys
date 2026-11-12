'''
============================================================================
@version     1.1.0
@author      dcueli
@date        2026-11-11
@brief
Master AI & Big Data
26-27_1_1_M-IA_5074_Sistemas de Big Data
RA3 - Lesson 04
-----------------------------------------------------------------------------
bdorchestrator.py
-----------------
Provides static engine classes (PandasEngine, PolarsEngine) and the central
BigDataOrchestrator class to execute and benchmark dataset operations.

------------------
@VERSION     1.0.0
------------------
class PandasEngine
------------------
Initial version of the PandasEngine module with methods to load datasets.
-----------------------------------------------------------------------------

class PolarsEngine
------------------
Initial version of the PolarsEngine module with methods to load datasets.
-----------------------------------------------------------------------------

class BigDataOrchestrator
-------------------------
Initial version of the BigDataOrchestrator module with Pandas and Polars engines.
- ValidateEnvironment: Validates library installation and dataset file existence.
- GetEngine: Resolves the engine class based on the selected library.
- LoadDataset: Orchestrates dataset loading with execution time measurement.
- PrintOperationResult: Prints execution metrics and dataset preview to console.

------------------
@VERSION     1.1.0
------------------
class PandasEngine
------------------
- FilterData: Filters a Pandas DataFrame by genre and movieId threshold.
-----------------------------------------------------------------------------

class PolarsEngine
------------------
- FilterData: Filters a Polars DataFrame by genre and movieId threshold.
-----------------------------------------------------------------------------

class BigDataOrchestrator
-------------------------
- FilterData: Filters a Pandas DataFrame by genre and movieId threshold.
=============================================================================
'''

# REQUIRES
# ========
# System
# ------
import sys
import time
import importlib.util
from pathlib import Path
from typing import Dict

# Third-party libraries
# ----------------------
import pandas as pd
import polars as pl

# Custom
# Types, Defines
# --------------
import src.config.cerror as cer
importlib.reload(cer)
from src.config.cerror import CErr

import src.config.ctypes as ctp
importlib.reload(ctp)
from src.config.ctypes import FilterOp, BigDataLib

# Helpers functions
# -----------------
import src.helpers.console as csl
importlib.reload(csl)

# CLASSES DEFINITIONS
# ===================
# PandasEngine Class
# ------------------
# Static class implementing dataset operations using the Pandas library.
class PandasEngine:

  # LoadDataset
  # -----------
  # Loads a CSV dataset into a Pandas DataFrame.
  #
  # @param str pFilePath Path to the source CSV file.
  # 
  # @throws Exception Standardized ErrorResponse dictionary on failure.
  # @return Dict[str, any] Standardized response dictionary with 'bOk' and 'data' (pd.DataFrame).
  @staticmethod
  def LoadDataset(pFilePath: str) -> Dict[str, any]:
    try:
      dfPd: pd.DataFrame = pd.read_csv(pFilePath)
      return {'bOk': True, 'data': dfPd}

    except Exception as e:
      CErr.Raise(
        500,
        f"PandasEngine.{sys._getframe(0).f_code.co_name}",
        "Error loading CSV with Pandas from '%s': %s",
        (pFilePath, str(e)),
        e
      )

  # CleanMoviesData
  # ---------------
  # Extracts the 4-digit release year from the 'title' column into a new 'year'
  # integer column, removes the '(YYYY)' suffix from 'title', and drops rows
  # without a valid release year.
  #
  # @param pd.DataFrame pDf Source movies Pandas DataFrame.
  # 
  # @throws Exception Standardized ErrorResponse dictionary on failure.
  # @return Dict[str, any] Standardized response dictionary with 'bOk' and cleaned 'data'.
  @staticmethod
  def CleanMoviesData(pDf: pd.DataFrame) -> Dict[str, any]:
    try:
      dfCln: pd.DataFrame = pDf.copy()

      # 1. Extract 4-digit year from the end of 'title'
      dfCln['year'] = pd.to_numeric(
        dfCln['title'].str.extract(r'\((\d{4})\)\s*$', expand=False),
        errors='coerce'
      )

      # 2. Remove rows where 'year' could not be extracted (NaN) and cast to int64
      dfCln = dfCln.dropna(subset=['year']).copy()
      dfCln['year'] = dfCln['year'].astype('int64')

      # 3. Clean 'title' removing the trailing '(YYYY)' and extra whitespace
      dfCln['title'] = dfCln['title'].str.replace(r'\s*\(\d{4}\)\s*$', '', regex=True).str.strip()

      return {'bOk': True, 'data': dfCln}

    except Exception as e:
      CErr.Raise(
        500,
        f"PandasEngine.{sys._getframe(0).f_code.co_name}",
        "Error cleaning movies DataFrame with Pandas: %s",
        (str(e),),
        e
      )
  
  # FilterData
  # ----------
  # Filters a Pandas DataFrame evaluating pFilterByCol against pFilterByVal
  # using the comparison operator pFilterComparison after validating type compatibility.
  #
  # @param pd.DataFrame      pDf               Source Pandas DataFrame.
  # @param str               pFilterByCol      Column name to evaluate.
  # @param FilterOp          pFilterComparison Comparison operator ('==', '!=', '<', '<=', '>', '>=', 'contains').
  # @param int | float | str pFilterByVal      Target value to compare against.
  # 
  # @throws Exception Standardized ErrorResponse dictionary on validation or execution failure.
  # @return Dict[str, any] Standardized response dictionary with 'bOk' and filtered 'data'.
  @staticmethod
  def FilterData(
    pDf: pd.DataFrame,
    pFilterByCol: str,
    pFilterComparison: FilterOp,
    pFilterByVal: int | float | str
  ) -> Dict[str, any]:
    try:
      # Verify column exists in DataFrame
      if pFilterByCol not in pDf.columns:
        CErr.Raise(404,
          f"PandasEngine.{sys._getframe(0).f_code.co_name}",
          "Column '%s' not found in Pandas DataFrame.",
          (pFilterByCol,)
        )

      colSeries: pd.Series = pDf[pFilterByCol]
      bIsStrCol: bool = pd.api.types.is_string_dtype(colSeries)
      bIsNumCol: bool = pd.api.types.is_numeric_dtype(colSeries)
      bIsStrVal: bool = isinstance(pFilterByVal, str)
      bIsNumVal: bool = isinstance(pFilterByVal, (int, float)) and not isinstance(pFilterByVal, bool)

      # Validate column data type vs parameter value data type
      if bIsStrCol and not bIsStrVal:
        CErr.Raise(
          400,
          f"PandasEngine.{sys._getframe(0).f_code.co_name}",
          "Type mismatch: column '%s' is string but filter value '%s' is %s.",
          (pFilterByCol, str(pFilterByVal), type(pFilterByVal).__name__)
        )

      if bIsNumCol and not bIsNumVal:
        CErr.Raise(400,
          f"PandasEngine.{sys._getframe(0).f_code.co_name}",
          "Type mismatch: column '%s' is numeric but filter value '%s' is %s.",
          (pFilterByCol, str(pFilterByVal), type(pFilterByVal).__name__)
        )

      # Evaluate parameterized comparison (pFilterByCol [op] pFilterByVal)
      bFilterMask: pd.Series
      if '==' == pFilterComparison:
        bFilterMask = (pFilterByVal == colSeries)
      elif '!=' == pFilterComparison:
        bFilterMask = (pFilterByVal != colSeries)
      elif '<' == pFilterComparison:
        bFilterMask = (pFilterByVal > colSeries)
      elif '<=' == pFilterComparison:
        bFilterMask = (pFilterByVal >= colSeries)
      elif '>' == pFilterComparison:
        bFilterMask = (pFilterByVal < colSeries)
      elif '>=' == pFilterComparison:
        bFilterMask = (pFilterByVal <= colSeries)
      elif 'contains' == pFilterComparison:
        if not bIsStrCol:
          CErr.Raise(400,
            f"PandasEngine.{sys._getframe(0).f_code.co_name}",
            "Operator 'contains' is only valid for string columns, not '%s'.",
            (pFilterByCol,)
          )
        bFilterMask = colSeries.str.contains(str(pFilterByVal), case=False, na=False, regex=False)
      else:
        CErr.Raise(
          400,
          f"PandasEngine.{sys._getframe(0).f_code.co_name}",
          "Unsupported comparison operator: '%s'.",
          (pFilterComparison,)
        )

      dfFiltered: pd.DataFrame = pDf.loc[bFilterMask]
      return {'bOk': True, 'data': dfFiltered}

    except Exception as e:
      CErr.Raise(500,
        f"PandasEngine.{sys._getframe(0).f_code.co_name}",
        "Error filtering Pandas DataFrame (%s %s %s): %s",
        (pFilterByCol, pFilterComparison, str(pFilterByVal), str(e)),
        e
      )

# PolarsEngine Class
# ------------------
# Static class implementing dataset operations using the Polars library.
class PolarsEngine:

  # LoadDataset
  # -----------
  # Loads a CSV dataset into a Polars DataFrame.
  #
  # @param str pFilePath Path to the source CSV file.
  # 
  # @throws Exception Standardized ErrorResponse dictionary on failure.
  # @return Dict[str, any] Standardized response dictionary with 'bOk' and 'data' (pl.DataFrame).
  @staticmethod
  def LoadDataset(pFilePath: str) -> Dict[str, any]:
    try:
      dfPl: pl.DataFrame = pl.read_csv(pFilePath)
      return {'bOk': True, 'data': dfPl}

    except Exception as e:
      CErr.Raise(
        500,
        f"PolarsEngine.{sys._getframe(0).f_code.co_name}",
        "Error loading CSV with Polars from '%s': %s",
        (pFilePath, str(e)),
        e
      )

  # CleanMoviesData
  # ---------------
  # Extracts the 4-digit release year from the 'title' column into a new 'year'
  # integer column, removes the '(YYYY)' suffix from 'title', and drops rows
  # without a valid release year.
  #
  # @param pl.DataFrame pDf Source movies Polars DataFrame.
  # 
  # @throws Exception Standardized ErrorResponse dictionary on failure.
  # @return Dict[str, any] Standardized response dictionary with 'bOk' and cleaned 'data'.
  @staticmethod
  def CleanMoviesData(pDf: pl.DataFrame) -> Dict[str, any]:
    try:
      # 1. Extract 4-digit year, clean 'title' text, and filter out null years
      dfCln: pl.DataFrame = (
        pDf.with_columns([
          pl.col('title').str.extract(r'\((\d{4})\)\s*$', 1).cast(pl.Int64, strict=False).alias('year'),
          pl.col('title').str.replace(r'\s*\(\d{4}\)\s*$', '').str.strip_chars().alias('title')
        ])
        .drop_nulls(subset=['year'])
      )

      return {'bOk': True, 'data': dfCln}

    except Exception as e:
      CErr.Raise(
        500,
        f"PolarsEngine.{sys._getframe(0).f_code.co_name}",
        "Error cleaning movies DataFrame with Polars: %s",
        (str(e),),
        e
      )

  # FilterData
  # ----------
  # Filters a Polars DataFrame evaluating pFilterByCol against pFilterByVal
  # using the comparison operator pFilterComparison after validating type compatibility.
  #
  # @param pl.DataFrame      pDf               Source Polars DataFrame.
  # @param str               pFilterByCol      Column name to evaluate.
  # @param FilterOp          pFilterComparison Comparison operator ('==', '!=', '<', '<=', '>', '>=', 'contains').
  # @param int | float | str pFilterByVal      Target value to compare against.
  # 
  # @throws Exception Standardized ErrorResponse dictionary on validation or execution failure.
  # @return Dict[str, any] Standardized response dictionary with 'bOk' and filtered 'data'.
  
  @staticmethod
  def FilterData(
    pDf: pl.DataFrame,
    pFilterByCol: str,
    pFilterComparison: FilterOp,
    pFilterByVal: int | float | str
  ) -> Dict[str, any]:
    try:
      # Verify column exists in DataFrame
      if pFilterByCol not in pDf.columns:
        CErr.Raise(404,
          f"PolarsEngine.{sys._getframe(0).f_code.co_name}",
          "Column '%s' not found in Polars DataFrame.",
          (pFilterByCol,)
        )

      colDtype: pl.DataType = pDf.schema[pFilterByCol]
      bIsStrCol: bool = (pl.String == colDtype) or (pl.Utf8 == colDtype)
      bIsNumCol: bool = colDtype.is_numeric()
      bIsStrVal: bool = isinstance(pFilterByVal, str)
      bIsNumVal: bool = isinstance(pFilterByVal, (int, float)) and not isinstance(pFilterByVal, bool)

      # Validate column data type vs parameter value data type
      if bIsStrCol and not bIsStrVal:
        CErr.Raise(400,
          f"PolarsEngine.{sys._getframe(0).f_code.co_name}",
          "Type mismatch: column '%s' is string but filter value '%s' is %s.",
          (pFilterByCol, str(pFilterByVal), type(pFilterByVal).__name__)
        )

      if bIsNumCol and not bIsNumVal:
        CErr.Raise(400,
          f"PolarsEngine.{sys._getframe(0).f_code.co_name}",
          "Type mismatch: column '%s' is numeric but filter value '%s' is %s.",
          (pFilterByCol, str(pFilterByVal), type(pFilterByVal).__name__)
        )

      # Evaluate parameterized comparison (pFilterByCol [op] pFilterByVal)
      filterExpr: pl.Expr
      if '==' == pFilterComparison:
        filterExpr = (pFilterByVal == pl.col(pFilterByCol))
      elif '!=' == pFilterComparison:
        filterExpr = (pFilterByVal != pl.col(pFilterByCol))
      elif '<' == pFilterComparison:
        filterExpr = (pFilterByVal > pl.col(pFilterByCol))
      elif '<=' == pFilterComparison:
        filterExpr = (pFilterByVal >= pl.col(pFilterByCol))
      elif '>' == pFilterComparison:
        filterExpr = (pFilterByVal < pl.col(pFilterByCol))
      elif '>=' == pFilterComparison:
        filterExpr = (pFilterByVal <= pl.col(pFilterByCol))
      elif 'contains' == pFilterComparison:
        if not bIsStrCol:
          CErr.Raise(400,
            f"PolarsEngine.{sys._getframe(0).f_code.co_name}",
            "Operator 'contains' is only valid for string columns, not '%s'.",
            (pFilterByCol,)
          )
        filterExpr = pl.col(pFilterByCol).str.to_lowercase().str.contains(str(pFilterByVal).lower(), literal=True)
      else:
        CErr.Raise(400,
          f"PolarsEngine.{sys._getframe(0).f_code.co_name}",
          "Unsupported comparison operator: '%s'.",
          (pFilterComparison,)
        )

      dfFiltered: pl.DataFrame = pDf.filter(filterExpr)
      return {'bOk': True, 'data': dfFiltered}

    except Exception as e:
      CErr.Raise(500,
        f"PolarsEngine.{sys._getframe(0).f_code.co_name}",
        "Error filtering Polars DataFrame (%s %s %s): %s",
        (pFilterByCol, pFilterComparison, str(pFilterByVal), str(e)),
        e
      )

# BigDataOrchestrator
# -------------------
# Static orchestrator class that validates file existence and library availability,
# routes calls to the selected engine (Pandas or Polars), and measures execution time.
class BigDataOrchestrator:

  # ValidateEnvironment
  # --------------------
  # Verifies that the selected library is installed and the dataset file exists on disk.
  #
  # @param BigDataLib pLibName  Target library name ('pandas', 'polars', 'pyspark').
  # @param str        pFilePath Path to the dataset file (optional if already loaded).
  # 
  # @throws Exception Standardized ErrorResponse dictionary if validation fails.
  # @return Dict[str, any] Standardized validation status dictionary.
  @staticmethod
  def ValidateEnvironment(
    pLibName: BigDataLib,
    pFilePath: str = ''
  ) -> Dict[str, any]:
    try:
      # 1. Verify library is installed and can be imported
      if importlib.util.find_spec(pLibName) is None:
        CErr.Raise(
          404,
          f"BigDataOrchestrator.{sys._getframe(0).f_code.co_name}",
          "Library '%s' is not installed or cannot be imported.",
          (pLibName,)
        )

      # 2. Verify dataset file exists when a file path is provided
      if pFilePath:
        filePathObj: Path = Path(pFilePath)
        if not filePathObj.is_file():
          CErr.Raise(
            404,
            f"BigDataOrchestrator.{sys._getframe(0).f_code.co_name}",
            "Dataset file not found at path: '%s'.",
            (pFilePath,)
          )

      return {'bOk': True}

    except Exception as e:
      CErr.Raise(
        500,
        f"BigDataOrchestrator.{sys._getframe(0).f_code.co_name}",
        "Unexpected error validating environment for '%s': %s",
        (pLibName, str(e)),
        e
      )

  # GetEngine
  # ----------
  # Resolves and returns the static engine class matching pLibName.
  #
  # @param BigDataLib pLibName Target library name ('pandas', 'polars', 'pyspark').
  # @throws Exception Standardized ErrorResponse dictionary if engine is not implemented.
  # 
  # @return Dict[str, any] Standardized dictionary containing the engine class in 'data'.
  @staticmethod
  def GetEngine(pLibName: BigDataLib) -> Dict[str, any]:
    try:
      if 'pandas' == pLibName:
        return {'bOk': True, 'data': PandasEngine}
      elif 'polars' == pLibName:
        return {'bOk': True, 'data': PolarsEngine}
      else:
        CErr.Raise(
          501,
          f"BigDataOrchestrator.{sys._getframe(0).f_code.co_name}",
          "Engine for library '%s' is not implemented yet.",
          (pLibName,)
        )

    except Exception as e:
      CErr.Raise(
        500,
        f"BigDataOrchestrator.{sys._getframe(0).f_code.co_name}",
        "Unexpected error resolving engine '%s': %s",
        (pLibName, str(e)),
        e
      )

  # LoadDataset
  # -----------
  # Validates environment, delegates dataset loading to the selected engine,
  # measures execution time, and optionally prints the console summary.
  #
  # @param BigDataLib pLibName     Target library name ('pandas', 'polars', 'pyspark').
  # @param str        pFilePath    Path to the source CSV file.
  # @param bool       pPrintResult Whether to automatically print the console summary.
  # @param int        pPreviewRows Number of preview rows to print when pPrintResult is True.
  # 
  # @throws Exception Standardized ErrorResponse dictionary on failure.
  # @return Dict[str, any] Standardized response dictionary with 'bOk', 'data', 'time', and 'lib'.
  @staticmethod
  def LoadDataset(
    pLibName: BigDataLib,
    pFilePath: str,
    pPreviewRows: int = 5,
    pPrintResult: bool = True
  ) -> Dict[str, any]:
    try:
      BigDataOrchestrator.ValidateEnvironment(pLibName, str(pFilePath))
      resEng: Dict[str, any] = BigDataOrchestrator.GetEngine(pLibName)
      engineClass: any = resEng['data']

      # Measure execution time of the underlying engine method
      tInit: float = time.perf_counter()
      resLoad: Dict[str, any] = engineClass.LoadDataset(str(pFilePath))
      tEnd: float = time.perf_counter()

      resLoad['time'] = tEnd - tInit
      resLoad['lib'] = pLibName

      if pPrintResult:
        BigDataOrchestrator.PrintOperationResult(resLoad, f"File loaded: {pFilePath}\n", pPreviewRows)

      return resLoad

    except Exception as e:
      CErr.Raise(
        500,
        f"BigDataOrchestrator.{sys._getframe(0).f_code.co_name}",
        "Error orchestrating dataset load with '%s': %s",
        (pLibName, str(e)),
        e
      )

  # CleanMoviesData
  # ---------------
  # Validates environment, delegates movies dataset cleaning ('year' extraction)
  # to the selected engine, measures execution time, and prints the summary.
  #
  # @param BigDataLib pLibName     Target library name ('pandas', 'polars', 'pyspark').
  # @param any        pDf          Loaded movies DataFrame.
  # @param bool       pPrintResult Whether to automatically print the console summary.
  # @param int        pPreviewRows Number of preview rows to print when pPrintResult is True.
  # @throws Exception Standardized ErrorResponse dictionary on failure.
  # @return Dict[str, any] Standardized response dictionary with 'bOk', 'data', 'time', and 'lib'.
  @staticmethod
  def CleanMoviesData(
    pLibName: BigDataLib,
    pDf: any,
    pPreviewRows: int = 5,
    pPrintResult: bool = True
  ) -> Dict[str, any]:
    try:
      BigDataOrchestrator.ValidateEnvironment(pLibName)
      resEng: Dict[str, any] = BigDataOrchestrator.GetEngine(pLibName)
      engineClass: any = resEng['data']

      # Measure execution time of the underlying engine cleaning method
      tInit: float = time.perf_counter()
      resClean: Dict[str, any] = engineClass.CleanMoviesData(pDf)
      tEnd: float = time.perf_counter()

      resClean['time'] = tEnd - tInit
      resClean['lib'] = pLibName

      if pPrintResult:
        BigDataOrchestrator.PrintOperationResult(
          resClean,
          "Movies dataset cleaned ('year' extracted)",
          pPreviewRows
        )

      return resClean

    except Exception as e:
      CErr.Raise(
        500,
        f"BigDataOrchestrator.{sys._getframe(0).f_code.co_name}",
        "Error orchestrating movies data cleaning with '%s': %s",
        (pLibName, str(e)),
        e
      )

  # FilterData
  # ----------
  # Validates environment, delegates single-DataFrame parameterized filtering to the
  # selected engine, measures execution time, and optionally prints the console summary.
  #
  # @param BigDataLib        pLibName          Target library name ('pandas', 'polars', 'pyspark').
  # @param any               pDf               Loaded DataFrame matching the target library.
  # @param str               pFilterByCol      Column name to filter by.
  # @param FilterOp          pFilterComparison Comparison operator ('==', '!=', '<', '<=', '>', '>=', 'contains').
  # @param int | float | str pFilterByVal      Target value to compare against.
  # @param bool              pPrintResult      Whether to automatically print the console summary.
  # @param int               pPreviewRows      Number of preview rows to print when pPrintResult is True.
  # @throws Exception Standardized ErrorResponse dictionary on failure.
  # @return Dict[str, any] Standardized response dictionary with 'bOk', 'data', 'time', and 'lib'.
  @staticmethod
  def FilterData(
    pLibName: BigDataLib,
    pDf: any,
    pFilterByCol: str,
    pFilterComparison: FilterOp,
    pFilterByVal: int | float | str,
    pPrintResult: bool = True,
    pPreviewRows: int = 3
  ) -> Dict[str, any]:
    try:
      BigDataOrchestrator.ValidateEnvironment(pLibName)
      resEng: Dict[str, any] = BigDataOrchestrator.GetEngine(pLibName)
      engineClass: any = resEng['data']

      # Measure execution time of the underlying engine filtering method
      tInit: float = time.perf_counter()
      resFilter: Dict[str, any] = engineClass.FilterData(pDf, pFilterByCol, pFilterComparison, pFilterByVal)
      tEnd: float = time.perf_counter()

      resFilter['time'] = tEnd - tInit
      resFilter['lib'] = pLibName

      if pPrintResult:
        BigDataOrchestrator.PrintOperationResult(
          resFilter,
          f"Data filtered by '{pFilterByCol} {pFilterComparison} {pFilterByVal}'",
          pPreviewRows
        )

      return resFilter

    except Exception as e:
      CErr.Raise(500,
        f"BigDataOrchestrator.{sys._getframe(0).f_code.co_name}",
        "Error orchestrating data filtering with '%s': %s",
        (pLibName, str(e)),
        e
      )

  # PrintOperationResult
  # --------------------
  # Prints standardized execution metrics, total row count, and a preview of the
  # resulting DataFrame to the console.
  #
  # @param Dict[str, any] pRes         Result dictionary returned by an orchestrator method.
  # @param str            pActionLabel Descriptive action label for console output.
  # @param int            pPreviewRows Number of top rows to display (0 to hide preview).
  # 
  # @throws Exception Standardized ErrorResponse dictionary on failure.
  # @return Dict[str, any] Standardized status dictionary.
  @staticmethod
  def PrintOperationResult(
    pRes: Dict[str, any],
    pActionLabel: str = 'File loaded',
    pPreviewRows: int = 3
  ) -> Dict[str, any]:
    try:
      dfData: any = pRes['data']
      execTime: float = pRes['time']
      libName: str = str(pRes['lib']).upper()

      csl.SectionBreak(0, 0)
      print(f"Executing operation with {libName}...")
      csl.nbsp()
      print(f"{pActionLabel} successfully. Execution time: {execTime:.4f} seconds")
      print(f"Total rows: {len(dfData)}")

      if 0 < pPreviewRows:
        print(f"First {pPreviewRows} rows of the dataset:")
        print(dfData.head(pPreviewRows))

      return {'bOk': True}

    except Exception as e:
      CErr.Raise(
        500,
        f"BigDataOrchestrator.{sys._getframe(0).f_code.co_name}",
        "Error printing operation result: %s",
        (str(e),),
        e
      )