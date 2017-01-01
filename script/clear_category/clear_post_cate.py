import sys

incats = ['8   ',
'48  ',
'9   ',
'33  ',
'60  ',
'0500',
'50  ',
'0502',
'0100',
'10  ',
'89  ',
'0300',
'67  ',
'0900',
'68  ',
'5   ',
'65  ',
'7   ',
'88  ',
'75  ',
'14  ',
'0501',
'0700',
'66  ',
'70  ',]

outcats = []
for incat in incats:
    incat = incat.strip()
    if len(incat) < 4:
        oo = '02' + incat.strip().zfill(2)
    else:
        oo = incat
    outcats.append(oo)
outcats.sort()
print(outcats)


qian  = '''
ALTER TABLE cabpost2catalog DROP CONSTRAINT cabpost2catalog_catalog_id_fkey;
'''

hou = '''
ALTER TABLE cabpost2catalog ADD CONSTRAINT cabpost2catalog_catalog_id_fkey FOREIGN KEY (catalog_id) REFERENCES cabcatalog(uid) MATCH FULL;
'''
tmpl = '''update cabcatalog set uid = '{0}' where uid = '{1}';
update cabpost2catalog set catalog_id='{0}' where catalog_id='{1}';'''

for cate in incats:
    # if cate.startswith('0'):
    #     outcate = 'a' + cate[1:]
    # elif cate.startswith('1'):
    #     outcate =  'b' + cate[1:]
    # else:
    #     sys.exit(1)
    # print(outcate)

    incate = cate.strip()
    outcate = '02' + incate.zfill(2) if len(incate) < 4 else incate
    # print(outcate)

    out_str = tmpl.format(outcate, cate)
    print(out_str)