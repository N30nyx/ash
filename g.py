import os
def builtin(args=[]):
  globals = {
    "path": str(os.getcwd())
  }
  return globals