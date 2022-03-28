def builtin(q,v,g):
  for item in v:
    q = q.replace("${" + item + "}",v[item])
  for item in g:
    q = q.replace("%" + item + "%",g[item])
  return q