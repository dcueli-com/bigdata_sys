def nbsp(pHowMany: int = 1, pChar: str = " ") -> None:
  for i in range(0, pHowMany):
    print(f"{pChar}")

def LineBreak(pHowMany: int = 1) -> None:
  for i in range(0, pHowMany):
    print(f"+ ")

def SectionBreak(pLnInit: int = 1, pLnEnd: int = 1) -> None:
  LineBreak(pLnInit)
  print(f"+ ---------------------------------------------------------")
  LineBreak(pLnEnd)

def SectionBegin(pTitle: str = "", pLineBreak: int = 1) -> None:
  print(f"+ =========================================================")

  if pTitle:
    print(f"+ {pTitle}")
    
  if pLineBreak:
      LineBreak(pLineBreak)

def SectionEnd(pLineBreak: int = 1) -> None:
  if pLineBreak:
      LineBreak(pLineBreak)
      
  print(f"+ =========================================================")
