# -*- coding: utf-8

import torcms.script.autocrud.base_crud
from torcms.script.autocrud.gen_dics import gen_dics_from_xls, gen_crud_from_xls
from torcms.script.autocrud.gen_html import gen_add_edit_view_html, gen_list_select_html, gen_listinfo_html


def run_crud0():
    gen_dics_from_xls.gen_html_dic()
    gen_crud_from_xls.gen_array_crud()
    torcms.script.autocrud.base_crud.build_dir()


def run_crud1():
    gen_add_edit_view_html.gen_add_edit_view_tmpl()
    gen_listinfo_html.run_gen_listinfo()
    gen_list_select_html.do_list()
