import sys

sys.path.append('./')
from owslib.csw import CatalogueServiceWeb

csw = CatalogueServiceWeb('https://ddemd.deep-time.org/dcsw/csw.py?', version='2.0.2')
# csw = CatalogueServiceWeb('https://ddemd.deep-time.org/dcsw/csw.py?', version='3.0.0')
# csw = CatalogueServiceWeb('http://101.200.190.76:6670/pycsw/pycsw.py?', version='2.0.2')
# csw = CatalogueServiceWeb('http://101.200.190.76:6670/pycsw/pycsw.py?', version='3.0.0')

# csw = CatalogueServiceWeb('http://geodiscover.cgdi.ca/wes/serviceManagerCSW/csw')

print(csw.identification.type)
# 'CSW'
[print(op.name) for op in csw.operations]
# ['GetCapabilities', 'GetRecords', 'GetRecordById', 'DescribeRecord', 'GetDomain']
# Get supported resultType’s:

# csw.getdomain('GetRecords.resultType')
print(
    # csw.results
)
# {'values': ['results', 'validate', 'hits'], 'parameter': 'GetRecords.resultType', 'type': 'csw:DomainValuesType'}

##########

print('x' * 40)


from owslib.fes import BBox, Not, PropertyIsEqualTo, PropertyIsLike, PropertyIsNull

keyw = '青'
# csw = CatalogueServiceWeb('http://csw-drr.osgeo.cn:8827/pycsw/csw.py?')
birds_query_like = PropertyIsLike('dc:title', '%{0}%'.format(keyw))
# birds_query_like = PropertyIsNull('dc:title')
csw.getrecords2(constraints=[birds_query_like], maxrecords=20)
print('-' * 20)
print(csw.results)

for rec in csw.results:
    print('a')
    print(rec)

# cql='dc:title like "%birds%"'

# birds_query = PropertyIsLike('dc:title', '%water%')
# birds_query = PropertyIsLike('dc:title', '%', matchCase= False)
# csw.getrecords2(constraints=[birds_query], maxrecords=20)


# csw.getrecords(constraints=[birds_query])
# csw.getrecords2(cql = cql)

# csw.getrecords( )
# csw.results
# {'matches': 101, 'nextrecord': 21, 'returned': 20}
for rec in csw.records:
    print(csw.records[rec].title)
