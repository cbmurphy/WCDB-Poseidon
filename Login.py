#!/usr/bin/env python

# --------
# Login.py
# --------

import _mysql
import getpass

def login () :
  username = getpass.getuser()
  fd = open("/u/z/users/cs327e/" + username + "/.zinfo", 'r')

  for line in fd:
    if line[0:8] == 'database':
      database = line[11:-1]
    if line[0:8] == 'password':
      password = line[11: -1]

  c = _mysql.connect(
      host   = "z",
      user   = username,
      passwd = password,
      db     = database)
  assert str(type(c)) == "<type '_mysql.connection'>"
  return c
