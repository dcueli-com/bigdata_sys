def nbsp(pHowMany: int = 1, pChar: str = " ") -> None:
  for i in range(0, pHowMany):
    print(f"{pChar}")

def LineBreak(pHowMany: int = 1) -> None:
  for i in range(0, pHowMany):
    print(f"+ ")

def SectionBreak() -> None:
  LineBreak(1)
  print(f"+ ---------------------------------------------------------")
  LineBreak(1)

def SectionEnd() -> None:
  LineBreak(1)
  print(f"+ =========================================================")
