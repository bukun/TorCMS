_router_post = {
                'd': 'metadata',  # Filter_View

                }

_post_type = {

    'd': '''<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>
        '''.format('Metadata'),
}
_check_type = {

    'd': 'Metadata',

}
_post_cfg = {

    'd': {
        'router': 'metadata',
        'html': '''<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>'''.format('DDE'),
        'checker': '0',  # '10', '100', '1000', '10000'
    }
}
xlsx_src='./torcms_dde/meta.xlsx'