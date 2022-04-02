import os
import bash,show,parse,ashrcm,exp
import g as gbl
from pathlib import Path
import json
import sys
import subprocess
import color

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
      x = open(fp,"""r+""")
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

class Ash:
    def load_module(name, filename):
        print(filename)
        import importlib
        # If the Loader finds the module name in this list it will use
        # module_name.__file__ instead so we need to delete it here
        if name in sys.modules:
            del sys.modules[name]
        module = __import__(filename)
        locals()[name] = module
        globals()[name] = module
    def execute(c,s=False):
        print(c)

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
                if s == False:

                  print(f"SHELL ERROR: `{e}`")
        return
    def ashrc():
        v = {}
        try:

          if ashsrc().read() in ['',""""""]:
            ashsrc().write("{}")

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
          if """poststart""" not in ashrc:
            ashrc["""poststart"""] = ""
            ashsrc("""d""",ashrc)
            ashrc = json.load(ashsrc())



        except Exception as et:
          print(f"""Failed to load {str(Path.home())}/ashrc.json\nERROR: {et}""")
        prefixer = """~> """
        try:
          prefixer = json.load(ashsrc())["""prefix"""]
        except KeyError:
          prefixer = str("""%path% ~ """)


        return ashrc,prefixer
    def cli():
        started = False
        ashrct,prefixt=Ash.ashrc()
        v = {}
        g = gbl.builtin()
        v,g = Ash.exec("@bash",v,g,ashrct,True)
        while True:
          try:

            ashrc,prefix=Ash.ashrc()



            if started == False:
                poststart = parse.builtin(json.load(ashsrc())["""poststart"""],{},g,"""arg""")
                Ash.execute(poststart,True)
                started = True

            prefix = parse.builtin(prefix,v,g,"""arg""")
            q =  input(prefix)
            v,g = Ash.exec(q,v,g,ashrc)
          except KeyboardInterrupt:
            show.builtin(["""\nPlease type `exit` to exit"""])
          except Exception as e:
            show.builtin([f"""ASH ERROR: `{e}`"""])
    def file(path):
        ashrct,prefixt=Ash.ashrc()
        v = {}
        g = gbl.builtin()
        v,g = Ash.exec(ashrct["poststart"],v,g,ashrct)

        if path.endswith(".ash") == False:
            path += ".ash"
        ashrc,prefix=Ash.ashrc()
        with open(path,"r") as af:
            for q in af.readlines():
                v,g = Ash.exec(q,v,g,ashrc)

    def exec(q,v={},g=gbl.builtin(),ashrc=None,s=False):
        stdir = str(Path.cwd())


        if ashrc == None:
            ashrc,prefix = Ash.ashrc()
        return Ash.eval(v,ashrc,q,stdir,g,s)


    def eval(v,ashrc,q,stdir,g,s):
        home = str(Path.home())

        g = gbl.builtin()
        g["""home"""] = home
        g["""path"""] = str(Path.cwd())

        g["""globals"""] = str(g)


        for c in color.palette:
            g[f"color.{c}"] = color.palette[c]
        try:
          g["username"] = os.getlogin()
        except:
            if os.environ.get('USERNAME') != None:
              g["username"] = os.environ.get('USERNAME')
            elif os.environ.get('USER') != None:
              g["username"] = os.environ.get('USER')
            else:
              g["username"] = "unable to find username"

        ashrc,prefix=Ash.ashrc()

        for gbli in ashrc["""globals"""]:
          g[gbli] = ashrc["""globals"""][gbli]
        g["ashdir"] = stdir

        oq = q


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
        q = q.replace("%20"," ")









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
          g["path"] = str(Path.cwd())
        elif q.startswith("""#"""):
          q = """"""
        elif q.startswith("""@"""):
          # @ will be builtin cmd
          if q.startswith("""@bash""") or q.startswith("""@cmd"""):
            bash.builtin([joiner(aargs)])
          if cmd in ["""@print"""]:
            show.builtin([joiner(aargs)])
          if cmd in ["""@echo"""]:
            Ash.execute("echo " + joiner(aargs),s)
          if cmd in ["""@export""","""@global"""]:
            exp.builtin([ashsrc,arg,joiner(args)])
          if cmd in ["""@ashrc""","""@config"""]:
            ashrcm.builtin([ashsrc,arg,joiner(oq.split(""" """)[2:])])
          if cmd in ["""@reload"""]:
            os.execv(sys.executable, ['python'] + sys.argv,s)
          if cmd in ["@update"]:
            Ash.execute(f"cd {stdir} && git pull",s)

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
            Ash.execute(f"""{f} {joiner(aargs)}""",s)
          else:
            Ash.execute(q,s)
        else:
          endings = """"""
          start = """"""
          if sys.platform.startswith("""win"""):
            endings = [""".bat""",""".ps1""",""".exe""",""".cmd"""]
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
                  Ash.execute(f"""{start}{cmd}{joiner(aargs)}""",s)
                  glfo = True




                elif cmd + ending in lfs:
                  Ash.execute(f"""{start}{cmd}{ending}{joiner(aargs)}""",s)
                  glfo = True
                else:
                  show.builtin([f"""Did you mean `./{cmd}` ?"""])
                  glfo = True
              else:
                pre = """"""
                post = """"""
                if sys.platform.startswith("""win"""):
                  pre = '"'
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
                  ei = i.replace(" ","%20")
                  if found != True:
                    if cmd in slss[i]:
                      Ash.execute(f"""{pre}{ei}/{cmd}{post} {joiner(aargs)}""",s)
                      glfo = True
                      found = True
                    elif cmd + ending in slss[i]:
                      Ash.execute(f"""{pre}{ei}/{cmd}{ending} {post} {joiner(aargs)}""",s)
                      glfo = True
                      found = True
                    elif cmd + """.py""" in slss[i]:

                      pargs = [str(Path.cwd()),"""ash"""]
                      for parg in pargs:
                        aargs.append(parg)
                      pyf = open(f"{ei}/{cmd}.py","r+")
                      pyfc = pyf.read()
                      pyfc = pyfc.replace('"ash-shell"','locals()["ash-shell"]').replace('"ash-shell-path"','locals()["ash-shell-path"]').replace('"is-ash-shell"','locals()["is-ash-shell"]')
                      d = {}
                      for gl in g:
                          d[f"ash-global-{gl}"] = g[gl]
                      for var in v:
                          d[f"ash-local-{var}"] = v[var]
                      d["ash-shell"] = Ash
                      d["ash-shell-path"] = Path.cwd()
                      d["is-ash-shell"] = True
                      d = dict(globals(),**d)
                      exec(pyfc,d,d)
                      glfo = True
                      found = True
          if glfo == False:
            show.builtin([f"""Unable to find `{cmd}`"""])
        return v,g
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        Ash.file(sys.argv[1])
    else:
        Ash.cli()
