# =============================================================================
# @version     1.0.0
# @author      dcueli 
# @date        2026-10-22
# @engine      CPython
# @dialect     Python 3.13.7
# @brief       
# Master AI & Big Data
# 26-27_1_1_M-IA_5074_Sistemas de Big Data
# -----------------------------------------------------------------------------
# ctypes.py
# ---------
# Provides custom types for developments.
# =============================================================================
from typing import Literal, TypeAlias

ChartType: TypeAlias = Literal[
  'scatter',
  'histogram',
  'strip',
  'line',
  'bar',
  'difference',
  'quality',
  'duplicated'
]
