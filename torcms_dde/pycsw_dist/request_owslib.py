from pprint import pprint

from owslib.csw import CatalogueServiceWeb

csw = CatalogueServiceWeb('https://drr.ikcest.org/csw')
print(csw.identification.type)

# [print(op.name) for op in csw.operations]

# csw.getdomain('GetRecords.resultType')
# print(csw.results)

from owslib.fes import BBox, PropertyIsEqualTo, PropertyIsLike


def query_by_kw():
    # birds_query = PropertyIsEqualTo('csw:AnyText', '')
    # birds_query = PropertyIsEqualTo('csw:AnyText', '')

    birds_query = PropertyIsLike('csw:AnyText', 'Food')

    # csw.getrecords2(constraints=[birds_query], maxrecords=20, )
    csw.getrecords2(
        constraints=[birds_query],
        maxrecords=20,
        startposition=0,
        distributedsearch=True,
        hopcount=2,
    )
    print(csw.results)
    for key in csw.records:
        rec = csw.records[key]
        print('=' * 40)
        print(rec)
        ops = [x for x in dir(rec) if not x.startswith('__')]
        pprint(ops)
        # for op in ops:
        #     print(f'## {op}:', eval(f'rec.{op}'))
        print(rec.abstract)
        print(rec.accessrights)
        print(rec.alternative)
        print(rec.bbox)
        print(rec.bbox_wgs84)
        print(rec.contributor)
        print(rec.coverage)
        print(rec.created)
        print(rec.creator)
        print(rec.date)
        print(rec.format)
        print(rec.identifier)
        print(rec.identifiers)
        print(rec.ispartof)
        print(rec.issued)
        print(rec.language)
        print(rec.license)
        print(rec.modified)
        print(rec.publisher)
        print(rec.rdf)
        print(rec.references)
        print(rec.relation)
        print(rec.rights)
        print(rec.rightsholder)
        print(rec.source)
        print(rec.spatial)
        print(rec.subjects)
        print(rec.temporal)
        print(rec.title)
        print(rec.type)
        print(rec.uris)
        print(rec.xml)

    # bbox_query = BBox([-141,42,-52,84])
    # csw.getrecords2(constraints=[birds_query, bbox_query])
    #
    # for rec in csw.records:
    #     print(csw.records[rec].title)


def query_by_id():
    '''
    没法使用联邦检索
    '''
    c = csw.getrecordbyid(id=['xh_1_12073'])
    pprint(c.records['xh_1_12073'].title)


if __name__ == '__main__':
    query_by_kw()
