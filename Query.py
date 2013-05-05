#!/usr/bin/env python

# --------
# Query.py
# --------

def query (c, s) :
    assert str(type(c)) == "<type '_mysql.connection'>"
    assert type(s)      is str
    c.query(s)
    r = c.use_result()
    if r is None :
        return None
    assert str(type(r)) == "<type '_mysql.result'>"
    t = r.fetch_row(maxrows = 0)
    assert type(t) is tuple
    return t
