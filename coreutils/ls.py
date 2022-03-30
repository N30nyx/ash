import os
import sys
# comment
def execute(c):
    import subprocess
    process = None
    try:
        bashCommand = c
        bc = bashCommand.split()
        nc = []
        for item in bc:
            item = item.replace("%20"," ")
            nc.append(item)
        process = subprocess.run(c.replace("%20"," "), check=True,text=True)
        o = process.stdout
        if o != None:
            print(o)
    except Exception as e:
        if str(e).endswith("1.") == False:

            print(f"SHELL ERROR: `{e}`")
    return
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
cwd = sys.argv[-2]
ash = sys.argv[-1]
h = sys.argv[1]
if h == "ash":
    h = None
tp = ""
files = []
folders = []
misc = []
if h != None and h not in ["-h","--hidden"]:
    cwd = h
for file in os.listdir(cwd):
  if h in ["-h","--hidden"]:
    if os.path.isfile(cwd + "/" + file):
      files.append(file)
    elif os.path.isdir(cwd + "/" + file):
      folders.append(file)
    else:
      misc.append(file)
  else:
    if file.startswith(".") == False:
      if os.path.isfile(cwd + "/" + file):
        files.append(file)
      elif os.path.isdir(cwd + "/" + file):
        folders.append(file)
      else:
        misc.append(file)
files = sorted(files, key=str.casefold)
folders = sorted(folders, key=str.casefold)
misc = sorted(misc, key=str.casefold)
for f in files:
  tp += f"{f} "
for fo in folders:
  tp += f"{color.GREEN}{fo}{color.END} "
for m in misc:
  tp += f"{color.RED}{m}{color.END} "
execute("echo " + tp)
