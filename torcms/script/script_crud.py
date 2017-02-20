# -*- coding: utf-8

from torcms.script.autocrud import gen_listinfo_html, gen_add_edit_view_html, gen_list_select_html


def run_auto(*args):
    gen_add_edit_view_html.gen_add_edit_view_tmpl()
    gen_listinfo_html.run_gen_listinfo()
    gen_list_select_html.do_list()
