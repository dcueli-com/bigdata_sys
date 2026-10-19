# REQUIRES
# ========
import time
import spacy

# from spacy import displacy, Language
from spacy import displacy
from pathlib import Path

# PATHS
# =====
# CURRENT FILE PATH
CURR_EXECERCISES_FILES_PATH = Path(__file__).resolve()
DATA_DIR = CURR_EXECERCISES_FILES_PATH.parent.parent / "data"

# HELPERS FUNCTIONS
# =================
def LineBreak(pHowMany: int = 1):
  for i in range(0, pHowMany):
    print(f"+ ")

def SectionBreak():
  LineBreak(1)
  print(f"+ ---------------------------------------------------------")
  LineBreak(1)
  
# CUSTOM FUNCTIONS
# ================
# 
# ProcessTextWithModel
# --------------------
# Process a spaCy Doc object to extract and display Named Entities (NER),
# highlighting proper names (PER/PERSON) and displaying complete entity metadata.
# 
# @param spacy.tokens.doc.Doc $pDoc Processed spaCy document instance.
# @param string $pLang Language model label for display header output.
# @return void
def ProcessTextWithModel(pDoc: spacy.language, pLang: str = "Not defined"):
  tInit = time.time()
  
  # Extract and fiter just persons/Names (PER label) from the text
  print(f"+ =========================================================")
  print(f"+ LANGUAGE MODEL: -{pLang}-")
  print(f"+ Persons proper names extracted from the text (PER label):")
  print(f"+ ---------------------------------------------------------")
  LineBreak(1)

  for entity in pDoc.ents:
    if entity.label_ in ('PER', 'PERSON'):
      print(f"Proper name: {entity.text}")
    # if entity.label_ == "PER":
    #   print(f"Proper name: {entity.text}")

  LineBreak(1)
  print(f"+ All detected entities (for comparison):")
  print(f"+ ---------------------------------------")
  for entity in pDoc.ents:
    print(f"Text: {entity.text:<25} | Type/Label: {entity.label_}")

  tEnd = time.time()
  print(f"+ Time to load: {tEnd - tInit:.4f} seconds")
  print(f"+ =========================================================")

# (n)atural (l)anguage (p)rocessing (NLP) models for different languages
# Spanish
nlpES = spacy.load("es_core_news_sm")
# Latin
nlpLA = spacy.load("la_core_web_md")

# IMPORT SOURCE TEXT
# ==================
# Read file with text
rndTextPath = DATA_DIR / "chiquito-ipsum.txt"
# Text to analyze
text = ""

with open(rndTextPath, "r", encoding="utf-8") as f:
  text = f.read()
  
# PROCESSING TEXT
# ===============
docES = nlpES(text)
docLA = nlpLA(text)

# Process text with model
ProcessTextWithModel(docES, "Spanish")
# Process text with model
ProcessTextWithModel(docLA, "Latin")

# PROCESSING TEXT IN HYBRID or INTERSECTION (ESPAÑOL + LATIN)
# ===========================================================
tInit = time.time()

# Extract person entities
perEntitiesES = set([entity.text for entity in docES.ents if entity.label_ == "PER"])
perEntitiesLA = set([entity.text for entity in docLA.ents if entity.label_ == "PERSON"])
# Intersection of both sets to find confirmed person names detected by BOTH models (Consensus)
consensusPersons = perEntitiesES.intersection(perEntitiesLA)

# DISPLAY COMPARATIVE CONSENSUS RESULTS
# =====================================
print(f"+ =================================================")
print(f"+ HYBRID or INTERSECTION (Spanish  &  Latin MODELS)")
print(f"+ Confirmed proper names (Detected by BOTH models):")
print(f"+ -------------------------------------------------")
LineBreak(1)

for name in consensusPersons:
  print(f"Confirmed Name: {name}")

LineBreak(1)
print(f"+ Summary metrics:")
print(f"+ ---------------------------------------------------------")
print(f"Spanish model candidate count : {len(perEntitiesES)}")
print(f"Latin model candidate count   : {len(perEntitiesLA)}")
print(f"Consensus candidates count    : {len(consensusPersons)}")

tEnd = time.time()
LineBreak(1)
print(f"+ Time to evaluate consensus: {tEnd - tInit:.4f} seconds")
print(f"+ =========================================================")
