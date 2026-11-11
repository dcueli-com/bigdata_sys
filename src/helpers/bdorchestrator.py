# =============================================================================
# @version     1.0.0
# @author      dcueli
# @date        2026-11-11
# @brief
# Master AI & Big Data
# 26-27_1_1_M-IA_5074_Sistemas de Big Data
# RA3 - Lesson 04
# -----------------------------------------------------------------------------
# bdorchestrator.py
# -----------------
# Provides static engine classes (PandasEngine, PolarsEngine) and the central
# BigDataOrchestrator class to execute and benchmark dataset operations.
# =============================================================================

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
from src.config.ctypes import BigDataLib, ErrorResponse

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

# PolarsEngine Class
# ------------------
# Static class implementing dataset operations using the Polars library.
class PolarsEngine:

  # LoadDataset
  # -----------
  # Loads a CSV dataset into a Polars DataFrame.
  #
  # @param str pFilePath Path to the source CSV file.
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
  # @throws Exception Standardized ErrorResponse dictionary on failure.
  # @return Dict[str, any] Standardized response dictionary with 'bOk', 'data', 'time', and 'lib'.
  @staticmethod
  def LoadDataset(
    pLibName: BigDataLib,
    pFilePath: str,
    pPrintResult: bool = True,
    pPreviewRows: int = 3
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
        BigDataOrchestrator.PrintOperationResult(resLoad, 'File loaded', pPreviewRows)

      return resLoad

    except Exception as e:
      CErr.Raise(
        500,
        f"BigDataOrchestrator.{sys._getframe(0).f_code.co_name}",
        "Error orchestrating dataset load with '%s': %s",
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