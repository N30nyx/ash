def builtin(q,v,g,arg):
  for item in v:
    q = q.replace("${" + item + "}",v[item])
  if arg != "":
    for item in g:
      q = q.replace("%" + item + "%",g[item])
  return q