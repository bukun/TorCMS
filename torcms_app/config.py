_router_post = {'1': 'post',
                '9': 'info',  # Filter_View
                'm': 'map',
                }

_post_type = {
    '1': '''<span style="color:green;" class="glyphicon glyphicon-list-alt">[{0}]</span>
        '''.format('Document'),
    '9': '''<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>
        '''.format('Data'),
}
_check_type = {
    '1': 'Document',
    '9': 'Data',

}
_post_cfg = {
    '1': {
        'router': 'post',
        'html': '''<span style="color:green;" class="glyphicon glyphicon-list-alt">[{0}]</span>'''.format('Document'),
        'checker': '1',
    },
    '9': {
        'router': 'info',
        'html': '''<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>'''.format('Data'),
        'checker': '10',  # '10', '100', '1000', '10000'
    }
}
