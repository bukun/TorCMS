from owslib.csw import CatalogueServiceWeb
csw = CatalogueServiceWeb('https://drr.ikcest.org/csw')
print(csw.identification.type)

[print(op.name) for op in csw.operations]

# csw.getdomain('GetRecords.resultType')
# print(csw.results)

from owslib.fes import PropertyIsEqualTo, PropertyIsLike, BBox

# birds_query = PropertyIsEqualTo('csw:AnyText', '')
# birds_query = PropertyIsEqualTo('csw:AnyText', '')

birds_query = PropertyIsLike('csw:AnyText', '%data%')

csw.getrecords2(constraints=[birds_query], maxrecords=20, distributedsearch=True, hopcount=2)
print(csw.results)
for rec in csw.records:
    print(csw.records[rec].title)