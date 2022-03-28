import os
import bash,show,parse,ashrcm,exp
import g as gbl
from pathlib import Path
import json
import sys

# get ~ and .bashrc but for ash

def ashsrc(t=None,d=None):
  
  fs = []
  x = ""
  fp = str(Path.home()) + "/ashrc.json"
  if t == "d":
    x = open(fp,"w")
    json.dump(d,x)
  else:
    for f in os.listdir(str(Path.home())):
      fs.append(f)
    if "ashrc.json" not in fs:
      
      
      x = open(fp,"w+")
      x.fp = fp
    else:
      x = open(fp,"r")
      x.fp = fp
    
    return x

def is_there(p=os.getcwd(),f=None):
  files = []
  for file in os.listdir(p):
    files.append(file)
  if f in files:
    return True
  else:
    return False

def joiner(l):
  if l == []:
    return ""
  s = ""
  for i in l:
    if i == l[0]:
      s += f"{i}"
    else:
      s += f" {i}"
  return s


v = {}
try:

  if ashsrc().read() in ['',""]:
    os.system("echo {} >> " + str(Path.home()) + "/ashrc.json")
      
  ashrc = json.load(ashsrc())
  if "symlinks" not in ashrc:
    ashrc["symlinks"] = []
    ashsrc("d",ashrc)
    ashrc = json.load(ashsrc())
  if "startup" not in ashrc:
    ashrc["startup"] = "echo ASH - Ashes dust to dust"
    ashsrc("d",ashrc)
    ashrc = json.load(ashsrc())
  if "globals" not in ashrc:
    ashrc["globals"] = {}
    ashsrc("d",ashrc)
    ashrc = json.load(ashsrc())
  
  os.system(ashrc["startup"])
except Exception as et:
  print(f"Failed to load {str(Path.home())}/ashrc.json\nERROR: {et}")
prefix = "~"
try:
  prefix = json.load(ashsrc())["prefix"]
except:
  prefix = str(os.getcwd() + " ~ ")
while True:
  try:
    home = str(Path.home())
    
    g = gbl.builtin()
    g["home"] = home
    
    q =  input(prefix)
    q = parse.builtin(q,v,g)
    
    g["globals"] = str(g)
    ashrc = json.load(ashsrc())
    for gbli in ashrc["globals"]:
      g[gbli] = ashrc["globals"][gbli]
    

    
      
      
  
    try:
      cmd = q.split(" ")[0]
    except IndexError:
      cmd = ""
    try:
      arg = q.split(" ")[1]
    except IndexError:
      arg = ""
    try:
      args = q.split(" ")[2:]
    except IndexError:
      args = []
    try:
      aargs = q.split(" ")[1:]
    except IndexError:
      aargs = []
    
    if q.startswith("exit") or q.startswith("quit"):
      if arg == "":
        exit()
      else:
        exit(int(arg))
      
      
    elif q.startswith("#"):
      q = ""
    elif q.startswith("@"):
      # @ will be builtin cmd
      if q.startswith("@bash") or q.startswith("@cmd"):
        bash.builtin([joiner(aargs)])
      if cmd in ["@echo","@print"]:
        show.builtin([joiner(aargs)])
      if cmd in ["@export","@global"]:
        exp.builtin([ashsrc,arg,joiner(args)])
      if cmd in ["@ashrc","@config"]:
        ashrcm.builtin([ashsrc,arg,joiner(args)])
      if cmd in ["@reload"]:
        os.execv(sys.executable, ['python'] + sys.argv)
    elif q.startswith("$"):
      # $ will be var defining
      
      var = cmd.replace("$","",1)
      if arg == "" and var in v:
        show.builtin([v[var]])
      op = arg
      c = joiner(args)
  
  
      exec(f"{var} {op} {c}",{},v)
      v[var] = str(v[var])
    elif q.startswith("%"):
      # % will be for globals
      if q == ("%vars%"):
        show.builtin([v])
      elif q == "%globals%":
        show.builtin([g])
      else:
        if q.replace("%","") in g:
          show.builtin([g[q.replace("%","")]])
    elif q.startswith("./"):
      f = q.replace("./","")
      if sys.platform.startswith("win"):
        os.system(f"{f[0]} {joiner(aargs)}")
      else:
        os.system(q)
    else:
      ending = ""
      start = ""
      if sys.platform.startswith("win"):
        ending = ".bat"
        start = ""
      else:
        ending = ".sh"
        start = "bash "
      lfs = []
      for lf in os.listdir(os.getcwd()):
        lfs.append(lf)
      if cmd in lfs or cmd + ending in lfs:
        if cmd.endswith(ending):
          os.system(f"{start}{cmd}{joiner(aargs)}")
          



        elif cmd + ending in lfs:
          os.system(f"{start}{cmd}{ending}{joiner(aargs)}")
        else:
          show.builtin([f"Did you mean `./{cmd}` ?"])
      else:
        found = False
        slss = {}
        for sls in ashrc["symlinks"]:
          for f in os.listdir(sls):
            slss[sls] = f
        for i in slss:
          if found != True:
            if cmd in slss[i]:
              os.system(f"{i}/{cmd} {joiner(aargs)}")
              found = True
        if found == False:
          show.builtin([f"Unable to find `{cmd}`"])
          
  except Exception as e:
    show.builtin(["ERROR: " + str(e)])