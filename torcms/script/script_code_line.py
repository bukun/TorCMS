import os
import sys


def run_lines():
    fo = open('xx_code_stats.txt', 'w')
    # pwd = os.path.join(os.getcwd(), 'cmi')

    proj_ws = os.path.join(os.getcwd(), 'torcms')
    cnt_num = 0
    for wroot, wdirs, wfiles in os.walk(proj_ws):
        for wfile in wfiles:

            if wfile.endswith('.py'):
                fo.write('\n'  + wfile + '\n')
                infile = os.path.join(wroot, wfile)
                cnts = open(infile).readlines()
                for cnt in cnts:
                    cnt = cnt.rstrip()
                    if len(cnt) > 0:
                        fo.write("{0}: {1}\n".format(str(cnt_num).zfill(5), cnt))
                        cnt_num += 1
                # cnt_num  = cnt_num + len(cnts)
    fo.close()
    print(cnt_num)
