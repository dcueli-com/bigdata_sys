# =============================================================================
# @version     1.2.0
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

# Types of chart to use
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

# Data cleaning pipeline steps
CleanStep: TypeAlias = Literal[
  '2_nulls',
  '3_duplicates',
  '4_invalid_numerics',
  '5_dates',
  '6_outliers'
]

# Identified data quality issue categories
IssueType: TypeAlias = Literal[
  'null_critical',
  'null_cantidad',
  'null_precio_unitario',
  'null_total',
  'null_multiple_numeric',
  'duplicate_row',
  'negative_value',
  'zero_value',
  'total_mismatch',
  'invalid_date',
  'outlier_cantidad',
  'outlier_precio_unitario',
  'outlier_both'
]

# Resolution actions applied to affected rows
IssueAction: TypeAlias = Literal[
  'deleted',
  'imputed',
  'corrected'
]