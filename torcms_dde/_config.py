_router_post = {
                'd': 'directory',  # Filter_View

                }

_post_type = {

    'd': '''<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>
        '''.format('Directory'),
}
_check_type = {

    'd': 'Directory',

}
_post_cfg = {

    'd': {
        'router': 'directory',
        'html': '''<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>'''.format('Directory'),
        'checker': '0',  # '10', '100', '1000', '10000'
    }
}
xlsx_src='./torcms_dde/meta.xlsx'