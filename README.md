# applied_bigdata
Applied Big Data (Master's Degree in Artificial Intelligence and Big Data | LinkiaFP)

## Project folder structure
```
applied_bigdata/
├── .venv/ [.gitignore]
├── handover/
|   ├── doing/
|   └── temp/
|
├── scripts/
|   └── download_dataset.sh
|
├── src/
|   ├── activities/
|   |   ├── lesson_01/
|   |   |   ├── comparison/
|   |   |   |   ├── notebooks/
|   |   |   |   └── scripts/
|   |   |   |
|   |   |   ├── dataset/ [.gitignore]
|   |   |   |   └── ml-20m/
|   |   |   |
|   |   |   └── mongoplayground/
|   |   |
|   |   ├── lesson_02/
|   |   |   ├── comparison/
|   |   |   |   ├── notebooks/
|   |   |   |   └── scripts/
|   |   |   |
|   |   |   └── dataset/
|   |   |
|   |   └── lesson_03/
|   |   |   ├── dataset/ [.gitignore]
|   |   |   ├── notebooks/
|   |   |   ├── scripts/
|   |   |   └── README.md
|   |   |
|   |   └── lesson_04/
|   |   |   └── README.md
|   |   |
|   |   └── lesson_05/
|   |   |   ├── dataset/ [.gitignore]
|   |   |   ├── notebooks/
|   |   |   ├── scripts/
|   |   |   └── README.md
|   |   |
|   |   ├── reports/ [.gitignore]
|   |   └── temp/
|   | 
|   ├── config/
|   └── lessons/
|       ├── 20260413-02
|       ├── 20260508-06
|       └── 20260511-07
|           ├── checksum
|           ├── data-profiling
|           └── houses-models
|
├── .gitignore
├── LICENSE
└── README.md
```

## Datasets
This proyect use the following datasets
### RA1 > Activities > Mandatory
1. MovieLens 20M, download from <a href="grouplens.org">grouplens.org</a>:  <a href="https://grouplens.org/datasets/movielens/20m/">https://grouplens.org/datasets/movielens/20m/</a><br>
2. Unzip into <code>activities/lesson_01/dataset/</code>

### RA3 > Activities > Mandatory
1. Asteroid Dataset (<a href="https://ssd.jpl.nasa.gov/sbdb_query.cgi"><i>NASA JPL Small Body Search Engine</i></a>), download from <a href="kaggle.com">kaggle.com</a>:  <a href="https://gitlab.com/mirsakhawathossain/pha-ml/-/raw/master/Dataset/dataset.csv">https://gitlab.com/mirsakhawathossain/pha-ml/-/raw/master/Dataset/dataset.csv</a>
2. Unzip into <code>activities/lesson_03/dataset/</code>

## Technical requirements
### Python version
This is not a requirement but this project has been exectued opn Python v3.13, so it is higly recommended exectued it on that Python version
### Libraries
- setuptools (an obsolete library but necessary for the proper execution of the ydata-profiling)
pip install setuptools
- ydata-profiling, pygwalker and pandas (pandas library is necessary for the proper execution of the ydata-profiling)
pip install ydata-profiling pygwalker pandas