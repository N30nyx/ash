import os
import bash,show,parse,ashrcm,exp
import g as gbl
from pathlib import Path
import json
import sys

# get ~ and .bashrc but for ash

def ashsrc(t=None,d=None):
  
  fs = []
  x = """"""
  fp = str(Path.home()) + """/ashrc.json"""
  if t == """d""":
    x = open(fp,"""w""")
    json.dump(d,x)
  else:
    for f in os.listdir(str(Path.home())):
      fs.append(f)
    if """ashrc.json""" not in fs:
      
      
      x = open(fp,"""w+""")
      x.fp = fp
    else:
      x = open(fp,"""r""")
      x.fp = fp
    
    return x

def is_there(p=Path.cwd(),f=None):
  files = []
  for file in os.listdir(p):
    files.append(file)
  if f in files:
    return True
  else:
    return False

def joiner(l):
  if l == []:
    return """"""
  s = """"""
  for i in l:
    if i == l[0]:
      s += f"""{i}"""
    else:
      s += f""" {i}"""
  return s


v = {}
try:

  if ashsrc().read() in ['',""""""]:
    os.system("""echo {} >> """ + str(Path.home()) + """/ashrc.json""")
      
  ashrc = json.load(ashsrc())
  if """symlinks""" not in ashrc:
    ashrc["""symlinks"""] = []
    ashsrc("""d""",ashrc)
    ashrc = json.load(ashsrc())
  if """startup""" not in ashrc:
    ashrc["""startup"""] = """echo ASH - Ashes dust to dust"""
    ashsrc("""d""",ashrc)
    ashrc = json.load(ashsrc())
  if """globals""" not in ashrc:
    ashrc["""globals"""] = {}
    ashsrc("""d""",ashrc)
    ashrc = json.load(ashsrc())
  
  os.system(ashrc["""startup"""])
except Exception as et:
  print(f"""Failed to load {str(Path.home())}/ashrc.json\nERROR: {et}""")
prefixer = """~> """
try:
  prefixer = json.load(ashsrc())["""prefix"""]
except KeyError:
  prefixer = str("""%path% ~ """)
stdir = str(Path.cwd())
while True:
  try:
    home = str(Path.home())
    
    g = gbl.builtin()
    g["""home"""] = home
    g["""path"""] = str(Path.cwd())


    prefix = parse.builtin(prefixer,v,g,"""arg""")
    q =  input(prefix)
    try:
      cmd = q.split(""" """)[0]
    except IndexError:
      cmd = """"""
    try:
      arg = q.split(""" """)[1]
    except IndexError:
      arg = """"""
    try:
      args = q.split(""" """)[2:]
    except IndexError:
      args = []
    try:
      aargs = q.split(""" """)[1:]
    except IndexError:
      aargs = []
    q = parse.builtin(q,v,g,arg)
    try:
      cmd = q.split(""" """)[0]
    except IndexError:
      cmd = """"""
    try:
      arg = q.split(""" """)[1]
    except IndexError:
      arg = """"""
    try:
      args = q.split(""" """)[2:]
    except IndexError:
      args = []
    try:
      aargs = q.split(""" """)[1:]
    except IndexError:
      aargs = []  
    g["""globals"""] = str(g)
    ashrc = json.load(ashsrc())
    for gbli in ashrc["""globals"""]:
      g[gbli] = ashrc["""globals"""][gbli]
    

    
      
      
  

    
    if q.startswith("""exit""") or q.startswith("""quit"""):
      os.chdir(stdir)
      if arg == """""":
        exit()
      else:
        exit(int(arg))
    elif q == "" or q == '':
      ok = "frenchbabyseal"
      
    elif cmd in ["""cd"""]:
      os.chdir(arg)
    elif q.startswith("""#"""):
      q = """"""
    elif q.startswith("""@"""):
      # @ will be builtin cmd
      if q.startswith("""@bash""") or q.startswith("""@cmd"""):
        bash.builtin([joiner(aargs)])
      if cmd in ["""@echo""","""@print"""]:
        show.builtin([joiner(aargs)])
      if cmd in ["""@export""","""@global"""]:
        exp.builtin([ashsrc,arg,joiner(args)])
      if cmd in ["""@ashrc""","""@config"""]:
        ashrcm.builtin([ashsrc,arg,joiner(args)])
      if cmd in ["""@reload"""]:
        os.execv(sys.executable, ['python'] + sys.argv)

    elif q.startswith("""$"""):
      # $ will be var defining
      
      var = cmd.replace("""$""","""""",1)
      if arg == """""" and var in v:
        show.builtin([v[var]])
      op = arg
      c = joiner(args)
  
  
      exec(f"""{var} {op} {c}""",{},v)
      v[var] = str(v[var])
    elif q.startswith("""%"""):
      # % will be for globals
      if q == ("""%vars%"""):
        show.builtin([v])
      elif q == ("""%ashrc%"""):
        show.builtin([ashrc])
      elif q == """%globals%""":
        show.builtin([g])
      else:
        if q.replace("""%""","""""") in g:
          show.builtin([g[q.replace("""%""","""""")]])
    elif q.startswith("""./"""):
      f = cmd.replace("""./""","""""")
      if sys.platform.startswith("""win"""):
        os.system(f"""{f} {joiner(aargs)}""")
      else:
        os.system(q)
    else:
      endings = """"""
      start = """"""
      if sys.platform.startswith("""win"""):
        endings = [""".bat""",""".ps1""",""".exe"""]
        start = """"""
      else:
        endings = [""".sh"""]
        start = """bash """
      lfs = []
      for lf in os.listdir(os.getcwd()):
        lfs.append(lf)
      glfo = False
      for ending in endings:
        if glfo != True:
          if cmd in lfs or cmd + ending in lfs:
            if cmd.endswith(ending):
              os.system(f"""{start}{cmd}{joiner(aargs)}""")
              glfo = True
              
    
    
    
            elif cmd + ending in lfs:
              os.system(f"""{start}{cmd}{ending}{joiner(aargs)}""")
              glfo = True
            else:
              show.builtin([f"""Did you mean `./{cmd}` ?"""])
              glfo = True
          else:
            pre = """"""
            post = """"""
            if sys.platform.startswith("""win"""):
              pre = 'cmd /c "'
              post = '"'
            else:
              pre = """"""
              post = """"""
            found = False
            slss = {}
            for sls in ashrc["""symlinks"""]:
              slss[sls] = []
              for f in os.listdir(sls):
                slss[sls].append(f)
            for i in slss:
              if found != True:
                if cmd in slss[i]:
                  os.system(f"""{pre}{i}/{cmd}{post} {joiner(aargs)}""")
                  glfo = True
                  found = True
                elif cmd + ending in slss[i]:
                  os.system(f"""{pre}{i}/{cmd}{ending} {post} {joiner(aargs)}""")
                  glfo = True
                  found = True
                elif cmd + """.py""" in slss[i]:
                  pargs = [str(Path.cwd()),"""ash"""]
                  for parg in pargs:
                    aargs.append(parg)
                  os.system(f"""python3 {i}/{cmd}.py {joiner(aargs)}""")
                  glfo = True
                  found = True
      if glfo == False:
        show.builtin([f"""Unable to find `{cmd}`"""])

  except KeyboardInterrupt:
    show.builtin(["""\nPlease type `exit` to exit"""])
  except Exception as e:
    show.builtin(["""ERROR: """ + str(e)])