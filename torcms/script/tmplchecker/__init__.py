# -*- coding: utf-8 -*-

# pydot > graphviz
# graphviz

import os
import sys

try:
    from graphviz import Digraph, Graph

    g = Graph(format='png')
    dot = Digraph()
    dot.format = 'png'
except:
    pass

rels_uniq_arr = []


def pack_str(instr):
    return ''.join(instr.strip().split(' '))


def sim_filename(filepath):
    return os.path.splitext(os.path.split(filepath)[1])[0]


def check_html(html_file, begin):
    # uu  = Template(open(html_file).read())
    # vv = {'static_url': str}
    # print(uu.generate(**vv))
    sig = False
    # print('-' * 10)
    # print(html_file)
    for html_line in open(html_file).readlines():

        # uu = x.find('{% extends')
        uuu = pack_str(html_line).find('%extends')
        # print(pack_str(x))
        if uuu > 0:
            f_tmpl = html_line.strip().split()[-2].strip('"')
            curpath, curfile = os.path.split(html_file)
            ff_tmpl = os.path.abspath(os.path.join(curpath, f_tmpl))
            if os.path.isfile(ff_tmpl):
                # print(os.path.abspath(ff_tmpl))
                pass
            else:
                print(html_file)
                print(ff_tmpl)
                print('Error, tmpl not find.')
                # continue
                sys.exit(1)
            sig = True
        if sig:
            pass
        else:
            continue
        vvv = pack_str(html_line).find('%block')
        if vvv > 0:
            tt = pack_str(html_line)

            test_fig = False
            for yy in open(ff_tmpl).readlines():
                if yy.find(tt) > 0:
                    test_fig = True

            # fff = sim_filename(ff_tmpl)
            # sss = sim_filename(html_file)

            fff = ff_tmpl[begin:]
            sss = html_file[begin:]

            tmplsig = [fff, sss]

            if tmplsig in rels_uniq_arr:
                pass
            else:
                rels_uniq_arr.append(tmplsig)
                dot.edge(fff, sss)
            if test_fig:
                # G.add_edge(ff_tmpl[begin], html_file[begin])
                pass
            else:
                pass
                # print('Error')
                # if sig:


def do_for_dir(inws, begin):
    inws = os.path.abspath(inws)
    for wroot, wdirs, wfiles in os.walk(inws):
        for wfile in wfiles:
            if wfile.endswith('.html'):
                if 'autogen' in wroot:
                    continue
                check_html(os.path.abspath(os.path.join(wroot, wfile)), begin)


def run_checkit(srws=None):
    begin = len(os.path.abspath('templates')) + 1
    inws = os.path.abspath(os.getcwd())
    if srws:
        do_for_dir(srws[0], begin)
    else:
        do_for_dir(os.path.join(inws, 'templates'), begin)

    dot.render('xxtmpl', view=True)
