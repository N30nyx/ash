def builtin(args):
  import json
  ashsrc = args[0]
  d = json.load(ashsrc())
  k = args[1]
  if k.startswith("!del:"):
    k = k.replace("!del:","")
    del d[k]
  elif k.startswith("!add:"):
    k = k.replace("!add:","")
    v = args[2]
    if v in d[k]:
      d[k].remove(v)
    else:
      d[k].append(v)
  else:
    v = args[2]
    
    
    d[k] = v
  ashsrc("d",d)