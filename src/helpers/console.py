import sys, time

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

def SectionErrEndAndExit(pErr: str | dict[str, any], pInitT: float | None = None) -> None:
  nbsp()
  SectionBreak(0,0)
  if isinstance(pErr, str):
    print(f"Error: {pErr}")
  elif isinstance(pErr, dict):
    print(f"Error({pErr['err']['code']}): In {pErr['err']['whre']}:\n{pErr['err']['mssg']}")

  SectionBreak(0,0)
  tEnd: float = time.time()
  if (not pInitT):
    print(f"+ Time: {tEnd:.4f} seconds")
  else:    
    print(f"+ EXECUTION TERMINATE and EXIT in: {tEnd - pInitT:.4f} seconds")
  SectionEnd(0)
  sys.exit()
