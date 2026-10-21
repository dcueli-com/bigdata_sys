# =============================================================================
# @version     1.0.0
# @author      dcueli 
# @date        2026-10-06
# @engine      MySQL
# @dialect     ANSI SQL
# @brief       
# Master AI & Big Data
# 26-27_1_1_M-IA_5074_Sistemas de Big Data
# RA1/2/5
# -----------------------------------------------------------------------------
# validations.py
# --------------
# Overall, this file is a functions collection to validate things
# =============================================================================

# REQUIRES
# ========
# Third-party libraries
# ----------------------
import pandas as pd

# MODULES
# ========
# System modules
# --------------
from typing import Dict

# ValidateParams
# ------------------
# Validates a dictionary of parameters, checking for null, None, or empty values.
# 
# @param dict pParams Dictionary with parameter names as keys and their values.
# @param str pFuncName Name of the calling function for error reporting.
# @return dict Result object with bOk status and error details if validation fails.
def ValidateParams(pParams: Dict[str, any], pFuncName: str) -> Dict[str, any]:
  res: Dict[str, any] = {
    "bOk": False,
    "err": {
      "code": 400,
      "whre": pFuncName,
      "mssg": ""
    }
  }
  
  for paramName, paramValue in pParams.items():
    try:
      if paramValue is None or "" == paramValue or 0 == len(paramValue):
        res["err"]["mssg"] = f"+ Error[{pFuncName}]: No data parameter received in {paramName}; exiting"
        return res
      
    except (TypeError, ValueError):
      pass      

  return {"bOk": True} 
