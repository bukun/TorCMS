# -*- coding: utf-8 -*-

'''
Generate the diagram for the relation of the templates.
# pydot > graphviz
# graphviz
'''

import os
import sys

try:
    from graphviz import Digraph, Graph

    GRAPH_OBJ = Graph(format='png')
    DOT_OBJ = Digraph()
    DOT_OBJ.format = 'png'
except:
    print('Count not found Graphviz.')
    pass

RELS_UNIQ_ARR = []


def pack_str(instr):
    '''
    remove space in str.
    '''
    return ''.join(instr.strip().split(' '))


def sim_filename(filepath):
    '''
    Get the name of the file.
    '''
    return os.path.splitext(os.path.basename(filepath))[0]


def check_html(html_file, begin):
    '''
    Checking the HTML
    '''
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
            test_fig = False
            for the_line in open(ff_tmpl).readlines():
                if the_line.find(pack_str(html_line)) > 0:
                    test_fig = True

            # fff = sim_filename(ff_tmpl)
            # sss = sim_filename(html_file)

            fff = ff_tmpl[begin:]
            sss = html_file[begin:]

            tmplsig = [fff, sss]

            if tmplsig in RELS_UNIQ_ARR:
                pass
            else:
                RELS_UNIQ_ARR.append(tmplsig)
                DOT_OBJ.edge(fff, sss)
            if test_fig:
                # G.add_edge(ff_tmpl[begin], html_file[begin])
                pass
            else:
                pass
                # print('Error')
                # if sig:


def do_for_dir(inws, begin):
    '''
    do something in the directory.
    '''
    inws = os.path.abspath(inws)
    for wroot, wdirs, wfiles in os.walk(inws):
        for wfile in wfiles:
            if wfile.endswith('.html'):
                if 'autogen' in wroot:
                    continue
                check_html(os.path.abspath(os.path.join(wroot, wfile)), begin)


def run_checkit(srws=None):
    '''
    do check it.
    '''
    begin = len(os.path.abspath('templates')) + 1
    inws = os.path.abspath(os.getcwd())
    if srws:
        do_for_dir(srws[0], begin)
    else:
        do_for_dir(os.path.join(inws, 'templates'), begin)

    DOT_OBJ.render('xxtmpl', view=True)
