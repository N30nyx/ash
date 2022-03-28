import os
import bash,show,parse
import g as gbl


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

prefix = str(os.getcwd() + " ~ ")
v = {}
while True:
  
  g = gbl.builtin()
  g["globals"] = str(g)
  q =  input(prefix)
  q = parse.builtin(q,v,g)

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
    
    
  if q.startswith("#"):
    q = ""
  if q.startswith("@"):
    # @ will be builtin cmd
    if q.startswith("@bash") or q.startswith("@cmd"):
      bash.builtin([joiner(aargs)])
    if cmd in ["@echo","@print"]:
      show.builtin([joiner(aargs)])
  if q.startswith("$"):
    # $ will be var defining
    
    var = cmd.replace("$","",1)
    op = arg
    c = joiner(args)
    locel = {}
    exec(f"{var} {op} {c}",{},locel)
    v[var] = str(locel[var])
  if q.startswith("%"):
    # % will be for globals
    if q.startswith("%vars%"):
      show.builtin([v])
    if q.startswith("%globals%"):
      show.builtin([g])