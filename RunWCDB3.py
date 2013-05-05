#!/usr/bin/env python


# -------
# imports
# -------

import sys

from WCDB3 import wcdb3_solve

# ----
# main
# ----

file_names = sys.stdin.readlines();
rlist = []
for file_name in file_names:
  rlist.append(open(file_name.strip(), 'r'))
wcdb3_solve(rlist, sys.stdout, True)
for r in rlist:
  r.close()
