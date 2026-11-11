# =============================================================================
# @version     1.0.0
# @author      dcueli
# @date        2026-11-11
# @brief
# Master AI & Big Data
# 26-27_1_1_M-IA_5074_Sistemas de Big Data
# RA3 - Lesson 04
# -----------------------------------------------------------------------------
# cerror.py
# ---------
# Provides the static CErr class to build, format, and raise
# standardized ErrorResponse objects across the application.
# =============================================================================

# REQUIRES
# ========
# System
# ------
# import sys
import importlib

# Custom types
# ------------
import src.config.ctypes as ctp
importlib.reload(ctp)
from src.config.ctypes import ErrorResponse


# CErr
# -----------
# Static helper class for standardized error construction and exception raising.
class CErr:

  # Build
  # -----
  # Builds a standardized ErrorResponse dictionary formatting the message with
  # PHP-style (%s, %d) positional parameters.
  #
  # @param int   pCode   Numeric error status code (e.g., 404, 500, 501).
  # @param str   pWhere  Originating class and method name.
  # @param str   pMssg   Parameterized error message template using %s / %d placeholders.
  # @param tuple pParams Tuple of values to inject into pMssg placeholders.
  # @return ErrorResponse Standardized error dictionary.
  @staticmethod
  def Build(
    pCode: int,
    pWhere: str,
    pMssg: str,
    pParams: tuple = ()
  ) -> ErrorResponse:
    formattedMssg: str = (pMssg % pParams) if pParams else pMssg
    errObj: ErrorResponse = {
      'bOk': False,
      'err': {
        'code': pCode,
        'whre': pWhere,
        'mssg': formattedMssg
      }
    }
    return errObj

  # IsCErr
  # -------------
  # Checks if a caught Exception already wraps a standardized ErrorResponse dictionary.
  #
  # @param Exception pExc Caught exception instance.
  # @return bool True if pExc already contains an ErrorResponse dictionary, False otherwise.
  @staticmethod
  def IsCErr(pExc: Exception) -> bool:
    bIsCustom: bool = (
      0 < len(pExc.args) and
      isinstance(pExc.args[0], dict) and
      'bOk' in pExc.args[0] and
      'err' in pExc.args[0]
    )
    return bIsCustom

  # Raise
  # -----
  # Raises a standardized Exception containing an ErrorResponse object. If pExc is
  # provided and is already a standardized ErrorResponse exception, it re-raises it
  # preserving the original 'whre' and 'code'.
  #
  # @param int            pCode   Numeric error status code (e.g., 404, 500, 501).
  # @param str            pWhere  Originating class and method name.
  # @param str            pMssg   Parameterized error message template using %s / %d.
  # @param tuple          pParams Tuple of values to inject into pMssg placeholders.
  # @param Exception|None pExc    Optional caught exception to inspect before building a new one.
  # @throws Exception Standardized ErrorResponse dictionary wrapped in Exception.
  # @return None
  @staticmethod
  def Raise(
    pCode: int,
    pWhere: str,
    pMssg: str,
    pParams: tuple = (),
    pExc: Exception | None = None
  ) -> None:
    if None is not pExc and CErr.IsCErr(pExc):
      raise pExc

    errObj: ErrorResponse = CErr.Build(pCode, pWhere, pMssg, pParams)
    raise Exception(errObj)