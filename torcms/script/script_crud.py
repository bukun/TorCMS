from .autocrud import gen_dics_from_xls
from .autocrud import gen_add_edit_view_html
from .autocrud import gen_listinfo_html
from .autocrud import gen_list_select_html

def run_crud():
    gen_dics_from_xls.gen_html_dic()
    gen_dics_from_xls.gen_array_crud()
    gen_dics_from_xls.build_dir()
    gen_add_edit_view_html.gen_add_edit_view_tmpl()
    gen_listinfo_html.run_gen_listinfo()
    gen_list_select_html.do_list()
