#!/usr/bin/env python


# -------
# imports
# -------

import sys
import xml.etree.ElementTree as ET
def wcdb1_read(r):
  """
  r is reader
  returns root
  """
  instr = r.read()
  assert len(instr) > 0
  root = ET.fromstring(instr)

  return root

def wcdb1_write(root, w):
  """
  w is writer
  takes in root
  writes XML
  """
  outstr = ET.tostring(root)
  assert len(outstr) > 0
  w.write(outstr)
  

def wcdb1_solve(r, w):
  """
  read, print
  r is a reader
  w is a writer
  """
  root = wcdb1_read(r)
  wcdb1_write(root, w)
