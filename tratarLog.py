  #!/bin/bash
import re
import json

REGEXP_DEFINITIONS = {}
REGEXP_DEFINITIONS["wl11_error"]=(r"####<([\w]{3} [\d]{1,2}, [\d]{4} [\d]{1,2}:[\d]{1,2}:[\d]{1,2}) [^>]+> <Error> <([^>]*)> <([^>]*)> <([^>]*)> <([^>]*)> <<anonymous>> <([^>]*)> <([^>]*)> <([^>]*)> <([^>]*)> <([^>]*)>",
                            11, 
                            {},
                            ["date", "level", "serverid","serverinstance", "threadinfo", "1", "2", "-", "BEA-code", "msg"])
REGEXP_DEFINITIONS["wl11_stuck"]=(r"####<([\w]{3} [\d]{1,2}, [\d]{4} [\d]{1,2}:[\d]{1,2}:[\d]{1,2}) [^>]+> <Error> <([^>]*)> <([^>]*)> <([^>]*)> <([^>]*)> <<WLS Kernel>> <([^>]*)> <([^>]*)> <([^>]*)> <([^>]*)> <([^>]*)> \{([^}]*)[^>]*>",
                            12,
                            {10: "stuck_info"},
                            ["date", "level", "serverid","serverinstance", "threadinfo", "1", "2", "-", "BEA-code", "stuckinfo", "trace"]
                            )
REGEXP_DEFINITIONS["stuck_info"]=(r"[^\]]* ExecuteThread: '([0-9]*)'[^\[]*\[\n([^\n]*)([^\]]*])\", which is more than the configured time \(StuckThreadMaxTime\) of \"([\d]*)\"",
                            4,
                            {},
                            ["thread num", "Call", "Http metainfo", "-"])
                            

class PyLog():
  def __init__(self, inicio_linea="####"):
    self.regexp = {}
    self.id_inicio_linea = inicio_linea
    self.buffer = ""
    self.numLines = 0
    self.result = []

  def tratar(self, filename): 
    for key in self.regexp.keys(): 
      self.tratarTipo(filename, key)
    
  def tratarTipo(self, filename, typo):
    print "Searching for %s in %s" % (`typo`, filename)
    with open(filename) as f:
      lines = f.readlines()
      self.numLines = -1
      for line in lines:  
        buf = self.getLinea(line)
        if buf != "":
          res = self.tratarLinea(typo, buf)
          if res != {}:
            self.result.append(res)
      res = self.tratarLinea(typo, self.buffer)
      if res != {}:
            self.result.append(res)
    f.close()

  def getLinea(self, next):
    aux = ""
    if next.strip().startswith(self.id_inicio_linea):
      aux = self.buffer
      self.buffer = next    
    else:
      self.buffer += next
    return aux

  def tratarLinea(self, id, linea):
    self.numLines += 1
    buffer = {}
    self.tratarLineaRec(id, linea, buffer)
    if buffer != {}:
      self.result.append(buffer)
    return {}

  def tratarLineaRec(self, id, linea, result):
    match = re.search(REGEXP_DEFINITIONS[id][0], linea.strip())
    names = REGEXP_DEFINITIONS[id][3]
    subregex = {}
    if REGEXP_DEFINITIONS[id][2] != {}:
      subregex = REGEXP_DEFINITIONS[id][2]
    if match:
      for i in range(1, REGEXP_DEFINITIONS[id][1]):
        if i in subregex.keys():
          subBuffer = {}
          self.tratarLineaRec(subregex[i], match.group(i), subBuffer)
          result[names[i-1]] = subBuffer
        else:
          result[names[i-1]] = match.group(i)
    
  def addRegexFor(self, name):
    self.regexp[name] = REGEXP_DEFINITIONS[name]
  
  def addRegex(self, name, regexp, length):
    self.regexp[name] = (regexp, length)

class Result:
  def __init__(self):
    self.buffer = []
