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
# charts.py
# ---------
# Provides modular, decoupled chart generation functions for data auditing and
# diagnostics, adhering strictly to the Single Responsibility Principle and 
# externalized rendering.
# =============================================================================

# REQUIRES
# ========
# System
# ------
import sys

# Third-party libraries
# ----------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# MODULES
# ========
# System modules
# --------------
from typing import Literal, Dict

# Custom libraries
# ----------------
import src.helpers.validations as val

# ScatterCht
# ----------
# Renders sequential scatter plots for specified numeric columns to spot individual anomalies
#
# @param pd.DataFrame   pDf       The pandas dataframe containing the data.
# @param list           pCols     List of column names to plot.
# @param Dict[str, any] pCfgChart Configuration dictionary for sizing, styling, and fonts.
# @param any            pPlt      Matplotlib pyplot module passed by reference.
# 
# @return Dict[str, any] Result object containing bOk status and error details if applicable.
def ScatterCht(
  pDf: pd.DataFrame, 
  pCols: list,
  pCfgChart: Dict[str, any],
  pPlt: any
)-> Dict[str, any]:
  res = val.ValidateParams({
      "pDf": pDf, 
      "pCols": pCols, 
      "pCfgChart": pCfgChart
    }, 
    sys._getframe(0).f_code.co_name
  )
  
  if not res["bOk"]: return res
      
  ncols:int = pCfgChart.get("ncols", 2)
  
  fig, axes = pPlt.subplots(ncols=ncols, figsize=pCfgChart.get("figsize", (14, 6)))
  
  for i, col in enumerate(pCols[:ncols]):
    sns.scatterplot(
      x=pDf.index, 
      y=pd.to_numeric(pDf[col], errors='coerce'), 
      ax=axes[i], 
      color=pCfgChart.get("color", "steelblue"), 
      alpha=pCfgChart.get("alpha", 0.6), 
      s=pCfgChart.get("size", 30)
    )
    
    axes[i].set_title(f'{col.replace("_", " ").title()} Scatter Plot', fontsize=pCfgChart.get("fontS", 12), fontweight=pCfgChart.get("fontW", "bold"))
    axes[i].set_xlabel('Record Index')
    axes[i].set_ylabel(col)
  
  return {"bOk": True}

# HistogramCht
# ------------
# Renders histograms with optional KDE for specified numeric columns to analyze data distribution
#
# @param pd.DataFrame   pDf       The pandas dataframe containing the data.
# @param list           pCols     List of column names to plot.
# @param Dict[str, any] pCfgChart Configuration dictionary for sizing, styling, bins, and fonts.
# @param any            pPlt      Matplotlib pyplot module passed by reference.
# 
# @return Dict[str, any] Result object containing bOk status and error details if applicable.
def HistogramCht(
  pDf: pd.DataFrame, 
  pCols: list,
  pCfgChart: Dict[str, any],
  pPlt: any
)-> Dict[str, any]:
  res = val.ValidateParams({
      "pDf": pDf, 
      "pCols": pCols, 
      "pCfgChart": pCfgChart
    }, 
    sys._getframe(0).f_code.co_name
  )
  if not res["bOk"]: return res
      
  ncols: int = pCfgChart.get("ncols", 2)
  fig, axes = pPlt.subplots(ncols=ncols, figsize=pCfgChart.get("figsize", (14, 6)))
  
  # Safe handling in case <ncols> is 1 and axes is not an indexable array
  axesList = [axes] if ncols == 1 else axes
  
  for i, col in enumerate(pCols[:ncols]):
    sns.histplot(
      x=pd.to_numeric(pDf[col], errors='coerce'), 
      ax=axesList[i], 
      color=pCfgChart.get("color", "steelblue"), 
      bins=pCfgChart.get("bins", 30),
      kde=pCfgChart.get("kde", True),
      alpha=pCfgChart.get("alpha", 0.6)
    )
    
    axesList[i].set_title(f'{col.replace("_", " ").title()} Distribution', fontsize=pCfgChart.get("fontS", 12), fontweight=pCfgChart.get("fontW", "bold"))
    axesList[i].set_xlabel(col)
    axesList[i].set_ylabel("Frequency")
  
  return {"bOk": True}

# StripCht
# --------
# Renders strip plots for specified numeric columns to visualize distribution and individual data points.
#
# @param pd.DataFrame   pDf       The pandas dataframe containing the data.
# @param list           pCols     List of column names to plot.
# @param Dict[str, any] pCfgChart Configuration dictionary for sizing, styling, and fonts.
# @param any            pPlt      Matplotlib pyplot module passed by reference.
# 
# @return Dict[str, any] Result object containing bOk status and error details if applicable.
def StripCht(
  pDf: pd.DataFrame, 
  pCols: list,
  pCfgChart: Dict[str, any],
  pPlt: any
)-> Dict[str, any]:
  res = val.ValidateParams({"pDf": pDf, "pCols": pCols, "pCfgChart": pCfgChart}, sys._getframe(0).f_code.co_name)
  if not res["bOk"]: return res
      
  ncols: int = pCfgChart.get("ncols", 2)
  fig, axes = pPlt.subplots(ncols=ncols, figsize=pCfgChart.get("figsize", (14, 6)))
  
  # Safe handling in case ncols is 1 and axes is not an indexable array
  axesList = [axes] if ncols == 1 else axes
  
  for i, col in enumerate(pCols[:ncols]):
    sns.stripplot(
      y=pd.to_numeric(pDf[col], errors='coerce'), 
      ax=axesList[i], 
      color=pCfgChart.get("color", "steelblue"), 
      jitter=pCfgChart.get("jitter", 0.2),
      alpha=pCfgChart.get("alpha", 0.6),
      size=pCfgChart.get("size", 5)
    )
    
    axesList[i].set_title(f'{col.replace("_", " ").title()} Strip Plot', fontsize=pCfgChart.get("fontS", 12), fontweight=pCfgChart.get("fontW", "bold"))
    axesList[i].set_ylabel(col)
  
  return {"bOk": True}#

# LineCht
# -------
# Renders sequential line charts for specified numeric columns to track trends over time or index.
#
# @param pd.DataFrame   pDf       The pandas dataframe containing the data.
# @param list           pCols     List of column names to plot.
# @param Dict[str, any] pCfgChart Configuration dictionary for sizing, styling, and fonts.
# @param any            pPlt      Matplotlib pyplot module passed by reference.
# 
# @return Dict[str, any] Result object containing bOk status and error details if applicable.
def LineCht(
  pDf: pd.DataFrame, 
  pCols: list,
  pCfgChart: Dict[str, any],
  pPlt: any
)-> Dict[str, any]:
  res = val.ValidateParams({
      "pDf": pDf, 
      "pCols": pCols, 
      "pCfgChart": pCfgChart
    }, 
    sys._getframe(0).f_code.co_name
  )
  
  if not res["bOk"]: return res
      
  ncols: int = pCfgChart.get("ncols", 2)
  fig, axes = pPlt.subplots(ncols=ncols, figsize=pCfgChart.get("figsize", (14, 6)))
  
  # Safe handling in case <ncols> is 1 and axes is not an indexable array
  axesList = [axes] if ncols == 1 else axes
  
  for i, col in enumerate(pCols[:ncols]):
    sns.lineplot(
      x=pDf.index, 
      y=pd.to_numeric(pDf[col], errors='coerce'), 
      ax=axesList[i], 
      color=pCfgChart.get("color", "steelblue"), 
      alpha=pCfgChart.get("alpha", 0.8), 
      linewidth=pCfgChart.get("linewidth", 1.5)
    )
    
    axesList[i].set_title(f'{col.replace("_", " ").title()} Line Chart', fontsize=pCfgChart.get("fontS", 12), fontweight=pCfgChart.get("fontW", "bold"))
    axesList[i].set_xlabel('Record Index')
    axesList[i].set_ylabel(col)
  
  return {"bOk": True}

# PlotSalesAnalytics
# ------------------
# Orchestrator function that routes the request to the specific chart generator 
# based on the selected pChartType parameter.
#
# @param pd.DataFrame pDf The pandas dataframe containing the sales data.
# @param Literal['scatter', 'hist', 'strip', 'line'] pChartType The chart type to render.
# 
# @return None
def PlotSalesAnalytics(
  pDf: pd.DataFrame,
  pCols: list,
  pCfgChart: Dict[str, any],
  pChartType: Literal['scatter', 'hist', 'strip', 'line'] = 'scatter'
) -> Dict[str, any]:
  res: Dict[str, any] = { "bOk": True }
  
  sns.set_theme(style='whitegrid')
  
  if 'scatter' == pChartType:
    res = ScatterCht(pDf, pCols, pCfgChart, plt)
  elif 'hist' == pChartType:
    res = HistogramCht(pDf, pCols, pCfgChart, plt)
  elif 'strip' == pChartType:
    res = StripCht(pDf, pCols, pCfgChart, plt)
  elif 'line' == pChartType:
    res = LineCht(pDf, pCols, pCfgChart, plt)
  else:
    raise ValueError({
      "bOk": True,
      "err": {
        "code": 404,
        "whre": sys._getframe(0).f_code.co_name,
        "mssg": f"Unsupported chart type: '{pChartType}'. Use 'scatter', 'hist', 'strip', or 'line'."
      }
    })

  if not res["bOk"]: 
    raise ValueError(res)
  
  plt.tight_layout()
  plt.show()
  

# MissingValuesCht
# ----------------
# Renders a binary heatmap to visualize the presence and distribution of null/missing values.
#
# @param pd.DataFrame pDf The pandas dataframe containing the sales data.
# @return None
def MissingValuesCht(pDf: pd.DataFrame) -> None:
  fig, ax = plt.subplots(figsize=(12, 6))
  
  # Heatmap of null values (True/1 if missing, False/0 if present)
  sns.heatmap(pDf.isnull(), cbar=False, cmap='viridis', ax=ax)
  
  ax.set_title('Missing Values Heatmap (Null Distribution)', fontsize=12, fontweight='bold')
  ax.set_xlabel('Dataset Columns')
  ax.set_ylabel('Record Index')
  
  plt.tight_layout()
  plt.show()

# TotalsDiscrepancyCht
# --------------------
# Renders a scatter plot comparing reported totals vs calculated totals (Price * Quantity).
# Highlights discrepancies where values deviate from the 45-degree perfect match line.
#
# @param pd.DataFrame pDf The pandas dataframe containing the sales data.
# @return None
def TotalsDiscrepancyCht(pDf: pd.DataFrame) -> None:
  # Temporary copy to compute theoretical totals
  dfTemp = pDf.copy()
  dfTemp['precio_num'] = pd.to_numeric(dfTemp['precio_unitario'], errors='coerce')
  dfTemp['cantidad_num'] = pd.to_numeric(dfTemp['cantidad'], errors='coerce')
  dfTemp['total_num'] = pd.to_numeric(dfTemp['total'], errors='coerce')
  dfTemp['calculated_total'] = dfTemp['precio_num'] * dfTemp['cantidad_num']
  
  fig, ax = plt.subplots(figsize=(8, 8))
  
  sns.scatterplot(
    x='calculated_total', 
    y='total_num', 
    data=dfTemp, 
    ax=ax, 
    color='crimson', 
    alpha=0.6, 
    s=40
  )
  
  # Reference diagonal line for perfect match (y = x)
  maxVal = max(dfTemp['calculated_total'].max(), dfTemp['total_num'].max()) if not dfTemp['calculated_total'].dropna().empty else 100
  ax.plot([0, maxVal], [0, maxVal], color='black', linestyle='--', linewidth=1.5, label='Perfect Match (y=x)')
  
  ax.set_title('Totals Discrepancy Analysis (Reported vs Calculated)', fontsize=12, fontweight='bold')
  ax.set_xlabel('Calculated Total (Price × Quantity) (€)')
  ax.set_ylabel('Reported Total (€)')
  ax.legend()
  
  plt.tight_layout()
  plt.show()

# AnomaliesSummaryCht
# -------------------
# Renders a categorical bar plot summarizing the volume of errors found across audit categories.
#
# @param dict pErrorsDict Dictionary containing category names as keys and error counts as values.
# @return None
def AnomaliesSummaryCht(pErrorsDict: dict) -> None:
  categories = list(pErrorsDict.keys())
  counts = list(pErrorsDict.values())
  
  fig, ax = plt.subplots(figsize=(10, 5))
  
  sns.barplot(x=categories, y=counts, ax=ax, palette='mako')
  
  ax.set_title('Audit Anomalies Summary by Category', fontsize=12, fontweight='bold')
  ax.set_xlabel('Anomaly Category')
  ax.set_ylabel('Number of Invalid Records')
  
  # Annotate numeric values on top of each bar
  for p in ax.patches:
    ax.annotate(
      f'{int(p.get_height())}', 
      (p.get_x() + p.get_width() / 2., p.get_height()), 
      ha='center', va='center', 
      xytext=(0, 5), 
      textcoords='offset points',
      fontweight='bold'
    )
      
  plt.tight_layout()
  plt.show()
