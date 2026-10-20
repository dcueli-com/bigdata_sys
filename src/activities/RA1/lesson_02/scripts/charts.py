# REQUIRES
# ========
# Third-party libraries
# ----------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# MODULES
# ========
# System modules
# --------------
from typing import Literal

from typing import Literal
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ScatterCht
# ----------
# Renders sequential scatter plots for price and quantity to spot individual anomalies.
#
# @param pd.DataFrame pPf The pandas dataframe containing the sales data.
# @return None
def ScatterCht(pPf: pd.DataFrame) -> None:
  qtySeries: pd.Series = pd.to_numeric(pPf['cantidad'], errors='coerce')
  prcSeries: pd.Series = pd.to_numeric(pPf['precio_unitario'], errors='coerce')
  
  fig, axes = plt.subplots(ncols=2, figsize=(14, 6))
  
  sns.scatterplot(x=pPf.index, y=prcSeries, ax=axes[0], color='steelblue', alpha=0.6, s=30)
  axes[0].set_title('Unit Price Scatter Plot', fontsize=12, fontweight='bold')
  axes[0].set_xlabel('Record Index')
  axes[0].set_ylabel('Unit Price (€)')
  
  sns.scatterplot(x=pPf.index, y=qtySeries, ax=axes[1], color='darkorange', alpha=0.6, s=30)
  axes[1].set_title('Quantity Scatter Plot', fontsize=12, fontweight='bold')
  axes[1].set_xlabel('Record Index')
  axes[1].set_ylabel('Quantity (Units)')
      
  plt.tight_layout()
  plt.show()


# HistogramCht
# ------------
# Renders linear histograms with a focused range to examine distribution and frequency.
#
# @param pd.DataFrame pPf The pandas dataframe containing the sales data.
# @return None
def HistogramCht(pPf: pd.DataFrame) -> None:
  qtySeries: pd.Series = pd.to_numeric(pPf['cantidad'], errors='coerce')
  prcSeries: pd.Series = pd.to_numeric(pPf['precio_unitario'], errors='coerce')

  prcFiltered = prcSeries[prcSeries <= 500]
  qtyFiltered = qtySeries[qtySeries <= 100]

  fig, axes = plt.subplots(ncols=2, figsize=(14, 6))

  sns.histplot(x=prcFiltered, ax=axes[0], color='steelblue', bins=30, kde=False)
  axes[0].set_title('Unit Price Histogram (< 500 €)', fontsize=12, fontweight='bold')
  axes[0].set_xlabel('Unit Price (€)')
  axes[0].set_ylabel('Frequency (Sales Count)')

  sns.histplot(x=qtyFiltered, ax=axes[1], color='darkorange', bins=30, kde=False)
  axes[1].set_title('Quantity Histogram (< 100 Units)', fontsize=12, fontweight='bold')
  axes[1].set_xlabel('Quantity (Units)')
  axes[1].set_ylabel('Frequency (Sales Count)')

  plt.tight_layout()
  plt.show()

# StripCht
# --------
# Renders strip plots to show data points distribution with jitter.
#
# @param pd.DataFrame pPf The pandas dataframe containing the sales data.
# @return None
def StripCht(pPf: pd.DataFrame) -> None:
  qtySeries: pd.Series = pd.to_numeric(pPf['cantidad'], errors='coerce')
  prcSeries: pd.Series = pd.to_numeric(pPf['precio_unitario'], errors='coerce')

  fig, axes = plt.subplots(ncols=2, figsize=(14, 6))

  sns.stripplot(y=prcSeries, ax=axes[0], color='steelblue', jitter=0.2, alpha=0.7)
  axes[0].set_title('Unit Price Strip Plot', fontsize=12, fontweight='bold')
  axes[0].set_ylabel('Unit Price (€)')

  sns.stripplot(y=qtySeries, ax=axes[1], color='darkorange', jitter=0.2, alpha=0.7)
  axes[1].set_title('Quantity Strip Plot', fontsize=12, fontweight='bold')
  axes[1].set_ylabel('Quantity (Units)')

  plt.tight_layout()
  plt.show()

# LineCht
# -------
# Renders sequential line plots where outliers stand out as sharp vertical spikes.
#
# @param pd.DataFrame pPf The pandas dataframe containing the sales data.
# @return None
def LineCht(pPf: pd.DataFrame) -> None:
  qtySeries: pd.Series = pd.to_numeric(pPf['cantidad'], errors='coerce')
  prcSeries: pd.Series = pd.to_numeric(pPf['precio_unitario'], errors='coerce')

  fig, axes = plt.subplots(ncols=2, figsize=(14, 6))

  sns.lineplot(x=pPf.index, y=prcSeries, ax=axes[0], color='steelblue', linewidth=1, marker='o', markersize=3)
  axes[0].set_title('Unit Price Line Plot (Outlier Spikes)', fontsize=12, fontweight='bold')
  axes[0].set_xlabel('Record Index')
  axes[0].set_ylabel('Unit Price (€)')

  sns.lineplot(x=pPf.index, y=qtySeries, ax=axes[1], color='darkorange', linewidth=1, marker='o', markersize=3)
  axes[1].set_title('Quantity Line Plot (Outlier Spikes)', fontsize=12, fontweight='bold')
  axes[1].set_xlabel('Record Index')
  axes[1].set_ylabel('Quantity (Units)')

  plt.tight_layout()
  plt.show()

# PlotSalesAnalytics
# ------------------
# Orchestrator function that routes the request to the specific chart generator 
# based on the selected pChartType parameter.
#
# @param pd.DataFrame pPf The pandas dataframe containing the sales data.
# @param Literal['scatter', 'hist', 'strip', 'line'] pChartType The chart type to render.
# @return None
def PlotSalesAnalytics(
  pPf: pd.DataFrame, 
  pChartType: Literal['scatter', 'hist', 'strip', 'line'] = 'line'
) -> None:
  sns.set_theme(style="whitegrid")
  
  if pChartType == 'scatter':
    ScatterCht(pPf)
  elif pChartType == 'hist':
    HistogramCht(pPf)
  elif pChartType == 'strip':
    StripCht(pPf)
  elif pChartType == 'line':
    LineCht(pPf)
  else:
      raise ValueError(f"Unsupported chart type: '{pChartType}'. Use 'scatter', 'hist', 'strip', or 'line'.")

# MissingValuesCht
# ----------------
# Renders a binary heatmap to visualize the presence and distribution of null/missing values.
#
# @param pd.DataFrame pPf The pandas dataframe containing the sales data.
# @return None
def MissingValuesCht(pPf: pd.DataFrame) -> None:
  fig, ax = plt.subplots(figsize=(12, 6))
  
  # Heatmap of null values (True/1 if missing, False/0 if present)
  sns.heatmap(pPf.isnull(), cbar=False, cmap='viridis', ax=ax)
  
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
# @param pd.DataFrame pPf The pandas dataframe containing the sales data.
# @return None
def TotalsDiscrepancyCht(pPf: pd.DataFrame) -> None:
  # Temporary copy to compute theoretical totals
  dfTemp = pPf.copy()
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
