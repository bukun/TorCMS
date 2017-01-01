import sys

incats = ['9',
'12',
'32',
'91',
'92',
'93',
'8',
'33',
'90',
'37',
'25',
'4',
'0100',
'99',
'11',
'89',
'10',
'36',
'34',
'13',
'5',
'3',
'1',
'88',
'7',
'31',
'30',
'35',
'15',
'20',
'22',]

qian  = '''
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

    incate = cate + ' ' * (4 - len(cate))
    outcate = '01' + cate.zfill(2) if len(cate) < 4 else cate
    # print(outcate)

    out_str = tmpl.format(outcate, incate)
    print(out_str)