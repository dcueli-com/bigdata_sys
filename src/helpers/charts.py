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
# Provides modular, decoupled chart generation functions for data analysing and
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
from typing import Dict
from src.config.ctypes import ChartType

# Custom libraries
# ----------------
import src.helpers.validations as val


# SequentialScatterCht
# --------------------
# Renders sequential scatter plots (Record Index vs Columns across multiple subplots)
#
# @param pd.DataFrame   pDf       The pandas dataframe containing the data.
# @param list           pCols     List of column names to plot.
# @param Dict[str, any] pCfgChart Configuration dictionary for sizing, styling, and fonts.
# @param any            pPlt      Matplotlib pyplot module passed by reference.
# 
# @return Dict[str, any] Result object containing bOk status and error details if applicable.
def SequentialScatterCht(
  pDf: pd.DataFrame, 
  pCols: list,
  pCfgChart: Dict[str, any],
  pPlt: any
)-> Dict[str, any]:
  ncols: int = pCfgChart.get("ncols", 2)
  fig, axes = pPlt.subplots(ncols=ncols, figsize=pCfgChart.get("figsize", (14, 6)))
  
  axesList = [axes] if ncols == 1 else axes
  
  for i, col in enumerate(pCols[:ncols]):
    sns.scatterplot(
      x=pDf.index, 
      y=pd.to_numeric(pDf[col], errors='coerce'), 
      ax=axesList[i], 
      color=pCfgChart.get("color", "steelblue"), 
      alpha=pCfgChart.get("alpha", 0.6), 
      s=pCfgChart.get("size", 30)
    )
    
    axesList[i].set_title(f'{col.replace("_", " ").title()} Scatter Plot', fontsize=pCfgChart.get("fontsize", 12), fontweight=pCfgChart.get("fontweight", "bold"))
    axesList[i].set_xlabel('Record Index')
    axesList[i].set_ylabel(col)
    axesList[i].grid(True, linestyle='--', alpha=0.6)
  
  return {"bOk": True}

# RelationalScatterCht
# --------------------
# Renders relational scatter plots (Column X vs Column Y) with optional diagonal line
#
# @param pd.DataFrame   pDf       The pandas dataframe containing the data.
# @param list           pCols     List of column names to plot.
# @param Dict[str, any] pCfgChart Configuration dictionary for sizing, styling, and fonts.
# @param any            pPlt      Matplotlib pyplot module passed by reference.
# 
# @return Dict[str, any] Result object containing bOk status and error details if applicable.
def RelationalScatterCht(
  pDf: pd.DataFrame, 
  pCols: list,
  pCfgChart: Dict[str, any],
  pPlt: any
)-> Dict[str, any]:
  if 2 > len(pCols): return {
    "bOk": False,
    "err": {
      "code": 400,
      "whre": sys._getframe(0).f_code.co_name,
      "mssg": "Relational scatter plot requires at least two columns [x_col, y_col]."
    }
  }
  
  xCol, yCol = pCols[0], pCols[1]
  fig, axes = pPlt.subplots(figsize=pCfgChart.get("figsize", (8, 8)))
  
  xVals = pd.to_numeric(pDf[xCol], errors='coerce')
  yVals = pd.to_numeric(pDf[yCol], errors='coerce')
  
  sns.scatterplot(
    x=xVals, 
    y=yVals, 
    ax=axes,
    color=pCfgChart.get("color", "steelblue"), 
    alpha=pCfgChart.get("alpha", 0.7),
    edgecolors=pCfgChart.get("edgecolors", "k"),
    s=pCfgChart.get("size", 40)
  )
  
  # Optional diagonal reference line (e.g., 45-degree line for error checks)
  if pCfgChart.get("show_diagonal", False):
    minVal = min(xVals.min(), yVals.min())
    maxVal = max(xVals.max(), yVals.max())
    axes.plot([minVal, maxVal], [minVal, maxVal], color='red', linestyle='--', linewidth=1.5, label=pCfgChart.get("diagonal_label", "Ideal (y = x)"))
    axes.legend()
    
  axes.set_title(
    pCfgChart.get("title", f"{yCol} vs {xCol}"),
    fontsize=pCfgChart.get("fontsize", 12), 
    fontweight=pCfgChart.get("fontweight", "bold")
  )
  axes.set_xlabel(pCfgChart.get("xlabel", xCol))
  axes.set_ylabel(pCfgChart.get("ylabel", yCol))
  axes.grid(True, linestyle='--', alpha=0.6)
  
  return {"bOk": True}

# ResidualsScatterCht
# ------------------
# Renders a residuals scatter plot (Calculated Total vs Difference: Reported - Calculated)
# with a zero-reference line to clearly spot calculation errors and sign flips despite outliers.
#
# @param pd.DataFrame   pDf       The pandas dataframe containing the data.
# @param list           pCols     List of column names to plot.
# @param Dict[str, any] pCfgChart Configuration dictionary for sizing, styling, and fonts.
# @param any            pPlt      Matplotlib pyplot module passed by reference.
# 
# @return Dict[str, any] Result object containing bOk status and error details if applicable.
def ResidualsScatterCht(
  pDf: pd.DataFrame, 
  pCols: list,
  pCfgChart: Dict[str, any],
  pPlt: any
)-> Dict[str, any]:
  if len(pCols) < 2:
    return {
      "bOk": False,
      "err": {
        "code": 400,
        "whre": sys._getframe(0).f_code.co_name,
        "mssg": "Residuals scatter plot requires at least two columns [calc_col, reported_col]."
      }
    }
  
  calcCol, repCol = pCols[0], pCols[1]
  fig, axes = pPlt.subplots(figsize=pCfgChart.get("figsize", (10, 6)))
  
  xVals = pd.to_numeric(pDf[calcCol], errors='coerce')
  yVals = pd.to_numeric(pDf[repCol], errors='coerce')
  
  # Calculate residuals/difference: Reported - Calculated
  residuals = yVals - xVals
  
  sns.scatterplot(
    x=xVals, 
    y=residuals, 
    ax=axes,
    color=pCfgChart.get("color", "steelblue"), 
    alpha=pCfgChart.get("alpha", 0.7),
    edgecolors=pCfgChart.get("edgecolors", "k"),
    s=pCfgChart.get("size", 40)
  )
  
  # Perfect match reference line at Y = 0
  axes.axhline(0, color='red', linestyle='--', linewidth=1.5, label=pCfgChart.get("ref_label", "Ideal (Diff = 0)"))
  axes.legend()
    
  axes.set_title(
    pCfgChart.get("title", "Error Analysis: Residuals (Reported vs Calculated)"),
    fontsize=pCfgChart.get("fontsize", 12), 
    fontweight=pCfgChart.get("fontweight", "bold")
  )
  axes.set_xlabel(pCfgChart.get("xlabel", calcCol))
  axes.set_ylabel(pCfgChart.get("ylabel", "Difference (Reported - Calculated)"))
  axes.grid(True, linestyle='--', alpha=0.6)
  
  return {"bOk": True}

# ScatterCht
# ----------
# Orchestrator for scatter plots: routes to sequential or relational implementation.
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
      
  mode = pCfgChart.get("mode", "seq")
  
  if "seq" == mode:
    return SequentialScatterCht(pDf, pCols, pCfgChart, pPlt)
  elif "rel" == mode:
    return RelationalScatterCht(pDf, pCols, pCfgChart, pPlt)
  elif "res" == mode:
    return ResidualsScatterCht(pDf, pCols, pCfgChart, pPlt)
  else:
    return {
      "bOk": False,
      "err": {
        "code": 400,
        "whre": sys._getframe(0).f_code.co_name,
        "mssg": f"Unknown scatter mode: '{mode}'. Use 'seq' for sequential mode, 'rel' for relational mode or 'res' for residuals mode."
      }
    }

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
    
    axesList[i].set_title(f'{col.replace("_", " ").title()} Distribution', fontsize=pCfgChart.get("fontsize", 12), fontweight=pCfgChart.get("fontweight", "bold"))
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
    
    axesList[i].set_title(f'{col.replace("_", " ").title()} Strip Plot', fontsize=pCfgChart.get("fontsize", 12), fontweight=pCfgChart.get("fontweight", "bold"))
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
  
  if not res['bOk']: return res
      
  ncols: int = pCfgChart.get('ncols', 2)
  fig, axes = pPlt.subplots(ncols=ncols, figsize=pCfgChart.get('figsize', (14, 6)))
  
  # Safe handling in case <ncols> is 1 and axes is not an indexable array
  axesList = [axes] if ncols == 1 else axes
  
  for i, col in enumerate(pCols[:ncols]):
    sns.lineplot(
      x=pDf.index, 
      y=pd.to_numeric(pDf[col], errors='coerce'), 
      ax=axesList[i], 
      color=pCfgChart.get('color', 'steelblue'), 
      alpha=pCfgChart.get('alpha', 0.8), 
      linewidth=pCfgChart.get('linewidth', 1.5)
    )
    
    axesList[i].set_title(
      f'{col.replace('_', ' ').title()} Line Chart', 
      fontsize=pCfgChart.get('fontsize', 12), 
      fontweight=pCfgChart.get('fontweight', 'bold')
    )
    axesList[i].set_xlabel('Record Index')
    axesList[i].set_ylabel(col)
  
  return {"bOk": True}

# BarCht
# ------
# Renders a horizontal bar chart showing the percentage of missing values per column.
#
# @param pd.DataFrame   pDf       The pandas dataframe containing the data.
# @param list           pCols     List of column names to analyze.
# @param Dict[str, any] pCfgChart Configuration dictionary for sizing, styling, and fonts.
# @param any            pPlt      Matplotlib pyplot module passed by reference.
# 
# @return Dict[str, any] Result object containing bOk status and error details if applicable.
def BarCht(
  pDf: pd.DataFrame, 
  pCols: list,
  pCfgChart: Dict[str, any],
  pPlt: any
)-> Dict[str, any]:
  res = val.ValidateParams({"pDf": pDf, "pCols": pCols, "pCfgChart": pCfgChart}, sys._getframe(0).f_code.co_name)
  if not res["bOk"]: return res
      
  totalRows:int = len(pDf)
  if 0 == totalRows: return {
    "bOk": False,
    "err": {
      "code": 400,
      "whre": sys._getframe(0).f_code.co_name,
      "mssg": "DataFrame is empty, cannot compute missing values percentage."
    }
  }

  # Calculate missing percentages for the selected columns
  missingPercentages = (pDf[pCols].isnull().sum() / totalRows) * 100
  sortedData = missingPercentages.sort_values(ascending=True)
  
  # Fixed height
  # fig, axes = pPlt.subplots(figsize=pCfgChart.get("figsize", (10, 5)))
  # Dynamic height
  # Calculate height as per columns number (min 4 inch min)
  numCols: int = len(sortedData)
  figsize = (pCfgChart.get("figsize", (10, 5))[0], max(4.0, numCols * 0.4) )
  fig, axes = pPlt.subplots(figsize=figsize)
  
  # Explicit numeric positions to prevent gaps and alignment issues
  yPos = range(len(sortedData))  
  
  # Plot horizontal bars
  bars = axes.barh(
    yPos, 
    sortedData.values, 
    color=pCfgChart.get("color", "steelblue"),
    alpha=pCfgChart.get("alpha", 0.8)
  )

  # Conditionally render text labels based on configuration parameters
  if pCfgChart.get("show_values", True):
    textCfg = pCfgChart.get("text_cfg", {})
    for bar in bars:
      width = bar.get_width()
      axes.text(
        width + textCfg.get("offset", 1.5), 
        bar.get_y() + bar.get_height() / 2, 
        f"{width:.2f}%", 
        va=textCfg.get("va", "center"), 
        ha=textCfg.get("ha", "left"), 
        fontsize=textCfg.get("fontsize", 10), 
        color=textCfg.get("color", "black")
      )

  # Set explicit ticks and labels
  axes.set_yticks(yPos)
  axes.set_yticklabels(sortedData.index)
  axes.set_title(
    pCfgChart.get("title", "Horizontal Bar Chart"),
    fontsize=pCfgChart.get("fontsize", 12), 
    fontweight=pCfgChart.get("fontweight", "bold")
  )
  axes.set_xlabel(pCfgChart.get("xlabel", "Value"))
  axes.set_ylabel(pCfgChart.get("ylabel", "Column"))

  # Fixed X Limit
  # axes.set_xlim(0, 100)
  # Dynamic X Limit
  # X limit is adapted to max value found (min until 100 for percentages)
  maxVal = max(sortedData.values) if numCols > 0 else 0
  upperLimit = max(100.0, maxVal * 1.15)
  axes.set_xlim(0, upperLimit)
  
  # Add grid lines behind bars for readability
  axes.xaxis.grid(True, linestyle='--', alpha=0.6)
  axes.set_axisbelow(True)
  
  return {"bOk": True}

# DifferenceCht
# -------------
# Plot the differences between two values.
#
# @param pd.DataFrame       pDf The dataframe containing the data.
# @param list               pCols The reported and calculated column names.
# @param Dict               pCfgChart The chart configuration.
# @param matplotlib.pyplot  pPlt The pyplot module.
# 
# @return Dict[str, any] Result of the chart generation.
def DifferenceCht(
    pDf: pd.DataFrame,
    pCols: list,
    pCfgChart: Dict[str, any],
    pPlt
) -> Dict[str, any]:
  res = val.ValidateParams({"pDf": pDf, "pCols": pCols, "pCfgChart": pCfgChart}, sys._getframe(0).f_code.co_name)
  if not res["bOk"]: return res


  # Calculate the differences
  reported, calculated = pCols
  differences = pDf[reported] - pDf[calculated]

  # Create the chart
  fig, axes = pPlt.subplots(figsize=pCfgChart.get('figsize', (12, 6) ) )

  sns.barplot(
    x=pDf.index,
    y=differences,
    color=pCfgChart.get('color', 'steelblue'),
    ax=axes
  )

  axes.axhline(0, color='red', linestyle='--', linewidth=1)

  axes.set_title(pCfgChart.get('title', 'Default title'))
  axes.set_xlabel(pCfgChart.get('xlabel', 'Row index'))
  axes.set_ylabel(pCfgChart.get('ylabel', 'Reported - calculated'))

  # Optional symmetric logarithmic scale
  if 'symlog' == pCfgChart.get('yscale'):
    axes.set_yscale('symlog', linthresh=pCfgChart.get('linthresh', 100))

  axes.tick_params(axis='x', rotation=90)
  axes.grid(axis='y', alpha=0.3)

  return {"bOk": True}

# QualitySummaryCht
# -----------------
# Generate a 100% stacked bar chart summarizing data quality.
#
# @param <pd.DataFrame> [pDf]   The pandas dataframe containing the sales data
# @param <list[dict]>   [pCols] The validation results to represent. 
#   Example of data format it must to receive:
#   [{
#     'category': Name of column to compare,
#     'total': Total rows (this should be total rows of dataset),
#     'valid': (Total rows) - (Total rows with errors in category),
#     'errors': Total rows with invalid values (this should be calculated previously),
#   }]
# @param <Dict[str, any]> [pCfgChart] The chart configuration
#   Example of data format it must to receive:
#   {
#     'figsize': (X Width, Y Height),
#     'title': 'Text for the title of the chart',
#     'xlabel': 'Label for X axis',
#     'ylabel': 'Label for Y axis',
#     ...
#     'AnyProp': Any value,
#   }
# @param <matplotlib.pyplot> [pPlt] The pyplot module
# 
# @return Dict[str, any]
def QualityCht(
  pDf: pd.DataFrame,
  pCols: list,
  pCfgChart: Dict[str, any],
  pPlt
) -> Dict[str, any]:
  try:
    categories = [item['category'] for item in pCols]
    validPct = [
      item['valid'] / item['total'] * 100 if item['total'] else 0
      for item in pCols
    ]
    errorsPct = [
      item['errors'] / item['total'] * 100 if item['total'] else 0
      for item in pCols
    ]

    fig, axes = pPlt.subplots(figsize=pCfgChart.get('figsize', (10, 6) ) )

    # axes.bar(categories, validPct, label='Valid records')
    # axes.bar(categories, errorsPct, bottom=validPct, label='Invalid records')
    
    barsValid = axes.bar(categories, validPct, label='Valid records')
    barsErrors = axes.bar(categories, errorsPct, bottom=validPct, label='Invalid records')
    # Show percentages inside each bar segment
    axes.bar_label(barsValid,
      labels=[f'{pct:.1f}%' for pct in validPct],
      label_type='center',
      color='white',
      fontweight=pCfgChart.get('fontweight', 'normal'),
      fontsize=pCfgChart.get('fontsize', 9)
    )
    axes.bar_label(barsErrors,
      labels=[f'{pct:.1f}%' for pct in errorsPct],
      label_type='center',
      color='white',
      fontweight=pCfgChart.get('fontweight', 'normal'),
      fontsize=pCfgChart.get('fontsize', 9)
    )    

    axes.set_title(pCfgChart.get('title', 'Default title'))
    axes.set_xlabel(pCfgChart.get('xlabel', 'Default text for X label'))
    axes.set_ylabel(pCfgChart.get('ylabel', 'Default text for Y label'))
    axes.set_ylim(0, 100)
    axes.legend()
    axes.grid(axis='y', alpha=0.3)

    return {'bOk': True}

  except Exception as e:
    return {
      'bOk': False,
      'err': {
        'code': 500,
        'whre': sys._getframe(0).f_code.co_name,
        'mssg': str(e)
      }
    }

# DuplicatedValuesCht
# -------------------
# Plot a summary of unique and duplicated rows.
#
# @param <pd.DataFrame>   [pDf] Data source
# @param <list>           [pCols] Results returned by CheckDuplicatedValues
# @param <Dict[str, any]> [pCfgChart] Chart configuration
# @param <module>         [pPlt] Matplotlib pyplot module
# 
# @return dict Chart execution status
def DuplicatedCht(
  pDf: pd.DataFrame,
  pCols: list,
  pCfgChart: Dict[str, any],
  pPlt: any
) -> Dict[str, any]:
  res = val.ValidateParams({"pDf": pDf, "pCols": pCols, "pCfgChart": pCfgChart}, sys._getframe(0).f_code.co_name)
  if not res['bOk']: return res

  fig, axes = pPlt.subplots(figsize=pCfgChart.get('figsize', (10, 5)))

  sortedData = pDf.set_index(pCols[0])[pCols[1]].sort_values()
  yPos = range(len(sortedData))

  bars = axes.barh(
    yPos,
    sortedData.values,
    color=pCfgChart.get('color', 'steelblue'),
    alpha=pCfgChart.get('alpha', 0.8)
  )

  if pCfgChart.get('show_values', True):
      axes.bar_label( bars,
      fmt='%d',
      label_type='center',
      color='white',
      fontweight=pCfgChart.get('fontweight', 'normal'),
      fontsize=pCfgChart.get('fontsize', 9),
    )

  axes.set_yticks(yPos)
  axes.set_yticklabels(sortedData.index)
  axes.set_title(pCfgChart.get('title', 'Summary of duplicated rows'))
  axes.set_xlabel(pCfgChart.get('xlabel', 'Number of records'))
  axes.set_ylabel(pCfgChart.get('ylabel', None))

  axes.xaxis.grid(True, linestyle='--', alpha=0.6)
  axes.set_axisbelow(True)

  return {'bOk': True}

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
  pCols: list,
  pCfgChart: Dict[str, any],
  # pChartType: Literal['scatter', 'hist', 'strip', 'line', 'bar', 'diff', 'qty', 'dupl'] = 'scatter',
  pChartType: ChartType = 'scatter',
  pDf: pd.DataFrame = None
) -> Dict[str, any]:
  try:
    res: Dict[str, any] = { "bOk": True }
    
    sns.set_theme(style='whitegrid')
    
    # if 'scatter' == pChartType:
    #   res = ScatterCht(pDf, pCols, pCfgChart, plt)
    # elif 'hist' == pChartType:
    #   res = HistogramCht(pDf, pCols, pCfgChart, plt)
    # elif 'strip' == pChartType:
    #   res = StripCht(pDf, pCols, pCfgChart, plt)
    # elif 'line' == pChartType:
    #   res = LineCht(pDf, pCols, pCfgChart, plt)
    # elif 'bar' == pChartType:
    #   res = BarCht(pDf, pCols, pCfgChart, plt)
    # elif 'diff' == pChartType:
    #   res = DifferenceCht(pDf, pCols, pCfgChart, plt)
    # elif 'qty' == pChartType:
    #   res = QualityCht(pDf, pCols, pCfgChart, plt)
    # elif 'dupl' == pChartType:
    #   res = DuplicatedCht(pDf, pCols, pCfgChart, plt)
    # else:
    #   raise Exception(f"Unsupported chart type: '{pChartType}'. Use 'scatter', 'hist', 'strip', or 'line'.")

    chartFunction:str = globals().get(f"{pChartType.capitalize()}Cht")

    if callable(chartFunction):
      res = chartFunction(pDf, pCols, pCfgChart, plt)
    else:
      raise Exception(f"Unsupported chart type: <'{pChartType}'>.")

    if not res["bOk"]: 
      raise Exception(res)
    
    plt.tight_layout()
    plt.show()
    
    return res
  except Exception as e:
    return {
      "bOk": False,
      "err": {
        "code": 500,
        "whre": sys._getframe(0).f_code.co_name,
        "mssg": e.args[0]
      }
    }
  