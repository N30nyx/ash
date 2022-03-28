def builtin(args):
  import json
  ashsrc = args[0]
  d = json.load(ashsrc())
  k = args[1]
  v = args[2]
  if k in d["globals"]:
    print(f"removed {k} from globals")
    del d["globals"][k]
  else:
  
    
    
    d["globals"][k] = v
  ashsrc("d",d)