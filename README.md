# bigdata_sys
Big Data systems (Master's Degree in Artificial Intelligence and Big Data | LinkiaFP)

## Project folder structure
```
bigdata_sys/
├── .venv/ [.gitignore]
├── handover/
|   ├── doing/
|   ├── done/
|   └── temp/
|
├── scripts/
|   └── download_dataset.sh
|
├── src/
|   ├── activities/
|   |   ├── RA1/
|   |   |   ├── lesson_01/
|   |   |   |   ├── data/
|   |   |   |   ├── notebooks/
|   |   |   |   └── scripts/
|   |   ├── lesson_02/
|   |   |
|   |   ├── reports/ [.gitignore]
|   |   └── temp/
|   | 
|   ├── config/
|   └── lessons/
|
├── .gitignore
├── LICENSE
└── README.md [this MD file]
```

## Data
This proyect use the following data
### RA1 > Activities > Mandatory
Random text on <a href="./src/activities/RA1/lesson_01/data/chiquito-ipsum.txt">Chiquito Ipsum</a><br>
Random text on <a href=".src/activities/RA1/lesson_01/data/la_core_web_md-3.9.5-py3-none-any.whl">Latin model</a><br>

## Technical requirements
### Python version
This is not a requirement but this project has been exectued opn Python v3.13, so it is higly recommended exectued it on that Python version
### Libraries
- setuptools (an obsolete library but necessary for the proper execution of the ydata-profiling)
pip install setuptools
- ydata-profiling, pygwalker and pandas (pandas library is necessary for the proper execution of the ydata-profiling)
pip install ydata-profiling pygwalker pandas
### Dependencies
- pip install ipykernel spacy
- python -m spacy download es_core_news_sm
#### la_core_web_md-3.9.5-py3-none-any.whl
- pip install src/activities/RA1/lesson_01/data/
#### Download chiquito-ipsum.txt
Download chiquito-ipsum.txt text file from for the proper scripts execution 



