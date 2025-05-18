'''
script for initialization.
'''


from .autocrud.base_crud import build_dir
from .autocrud.gen_html_file import generate_html_files as run_auto


def run_init(*args):
    '''
    running init.
    '''
    build_dir()
    run_auto()
