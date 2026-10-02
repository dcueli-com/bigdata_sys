from pyspark.sql import SparkSession

import pandas as pd
import polars as pl
import time

datasetPath = '../dataset/ml-20m/ratings.csv'

# ====================================================================================================
# BEGIN :: Pandas
# ----------------------------------------------------------------------------------------------------
timeInit  = time.time()
df_target = pd.read_csv(datasetPath)
timeEnd   = time.time()

print(f"+ =======================================================================")
print(f"+ ")
print(f"+ Loaded <ratings.csv> dataset")
print(f"+ Time to load the dataset with Pandas: {timeEnd - timeInit:.4f} seconds")
print(f"+ ")
print(f"+ =======================================================================")

print(df_target.head())

# ----------------------------------------------------------------------------------------------------
# END :: Pandas
# ====================================================================================================
# BEGIN :: Polars
# ----------------------------------------------------------------------------------------------------

timeInit = time.time()
df_target = pl.read_csv(datasetPath)
timeEnd = time.time()

print(f"+ =======================================================================")
print(f"+ ")
print(f"+ Loaded <ratings.csv> dataset")
print(f"+ Time to load the dataset with Polars: {timeEnd - timeInit:.4f} seconds")
print(f"+ ")
print(f"+ =======================================================================")

print(df_target.head())

# ----------------------------------------------------------------------------------------------------
# END :: Polars
# ====================================================================================================
# BEGIN :: PySpark
# ----------------------------------------------------------------------------------------------------

# Spark no hace nada hasta que lee el archivo, el dataset en este caso está en 
# 'data/ratings.csv'. Cuando escribimos df = spark.read.csv(...), la sesión 
# de Spark <spark> no lee el archivo de realmente, sino que anota el plan 
# de lo que tiene que hacer.
# 
# Es decir, cuando pedimos un resultado con un 'show()' o un 'count()', la 
# sesión revisa lo anotado y optimiza el camino más rápido. 
# 
# Creamos la sesión de Spark
spark = SparkSession.builder \
  .appName("ComprLibs") \
  .master("local[*]") \
  .config("spark.driver.memory", "64g") \
  .getOrCreate()

# Cargamos el dataset (lazyload)
df_target = spark.read.csv(
  datasetPath, 
  header=True, 
  inferSchema=True
)

# Obligamos a Spark a leer el archivo contando las filas
df_target.count()
timeEnd = time.time()

print(f"+ =======================================================================")
print(f"+ ")
print(f"+ Loaded <ratings.csv> dataset")
print(f"+ Time to load the dataset with PySpark: {timeEnd - timeInit:.4f} seconds")
print(f"+ ")
print(f"+ =======================================================================")

df_target.show(5)

# ----------------------------------------------------------------------------------------------------
# END :: PySpark
# ====================================================================================================