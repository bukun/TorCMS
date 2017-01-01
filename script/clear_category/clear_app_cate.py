import sys

foo_dic = {
    '03': '21',
    '05': '22',
    '06': '23',
    '09': '24',
    '25': '25',
    '32': '26',
    '40': '27',
    '88': '28',
    'a0': 'a0',
}

incats = ['0300', '0301', '0302', '0303', '0304', '0305',
          '0500', '0501', '0502', '0503', '0504',
          '0600', '0601', '0602', '0603', '0604',
          '0900', '0901', '0902', '0903', '0904', '0905', '0908',
          '2500', '2501', '2502', '2503', '2504', '2505', '2506', '2507', '2508', '2509', '2510',
          '3200', '3206', '3213', '3221', '3223', '3243', '3290',
          '4000', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4009',
          '8800', '8801', '8802',
          'a000', 'a001', 'a002', 'a003', ]

qian = '''
ALTER TABLE tabapp2catalog DROP CONSTRAINT tabapp2catalog_catalog_id_fkey;
'''

hou = '''
ALTER TABLE tabapp2catalog ADD CONSTRAINT tabapp2catalog_catalog_id_fkey  FOREIGN KEY (catalog_id) REFERENCES tabcatalog(uid) MATCH FULL;
'''
tmpl = '''update tabcatalog set uid = '{0}' where uid = '{1}';
update tabapp2catalog set catalog_id='{0}' where catalog_id='{1}';'''

for cate in incats:
    # if cate.startswith('0'):
    #     outcate = 'a' + cate[1:]
    # elif cate.startswith('1'):
    #     outcate =  'b' + cate[1:]
    # else:
    #     sys.exit(1)
    # print(outcate)

    # incate = cate + ' ' * (4 - len(cate))
    outcate = foo_dic[cate[:2]] + cate[2:]
    # print(outcate)

    out_str = tmpl.format(outcate, cate)
    print(out_str)
