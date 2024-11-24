# -*- coding: utf-8 -*-
"""
Dump database of PostgreSQL, with date stamp.
"""
import datetime
import os
import subprocess

try:
    from cfg import DB_INFO
except Exception as err:
    print(repr(err))
    DB_INFO = {
        "db": "",
        "pass": "",
    }

if os.path.exists("tmp"):
    pass
else:
    os.mkdir("tmp")


def run_dump():
    """
    Dump database of PostgreSQL
    """
    print("Dumping ... ")

    current = datetime.datetime.now()
    dstr = "{}{:0>2d}{:0>2d}-{:0>2d}{:0>2d}".format(
        current.year, current.month, current.day, current.hour, current.minute
    )
    cmd = "export PGPASSWORD={p} && pg_dump -h {h} -p {k} -F c -U {n} {n} > ./tmp/xx_pg_{n}_{d}.bak".format(
        n=DB_INFO["NAME"],
        p=DB_INFO["PASSWORD"],
        h=DB_INFO.get("HOST", "localhost"),
        k=DB_INFO.get("PORT", 5432),
        d=dstr,
    )
    subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    run_dump()
