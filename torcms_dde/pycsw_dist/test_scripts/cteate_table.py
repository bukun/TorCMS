import os

from torcms.core.tools import get_uuid
from torcms_dde.model.ext import RecordsModel

PYCSW_DB_FIELD = [
    'identifier',
    'typename',
    'schema',
    'mdsource',
    'insert_date',
    'xml',
    'anytext',
    'language',
    'type',
    'title',
    'title_alternate',
    'abstract',
    'keywords',
    'keywordstype',
    'parentidentifier',
    'relation',
    'time_begin',
    'time_end',
    'topicategory',
    'resourcelanguage',
    'creator',
    'publisher',
    'contributor',
    'organization',
    'securityconstraints',
    'accessconstraints',
    'otherconstraints',
    'date',
    'date_revision',
    'date_creation',
    'date_publication',
    'date_modified',
    'format',
    'source',
    'crs',
    'geodescode',
    'denominator',
    'distancevalue',
    'distanceuom',
    'wkt_geometry',
    'servicetype',
    'servicetypeversion',
    'operation',
    'couplingtype',
    'operateson',
    'operatesonidentifier',
    'operatesoname',
    'degree',
    'classification',
    'conditionapplyingtoaccessanduse',
    'lineage',
    'responsiblepartyrole',
    'specificationtitle',
    'specificationdate',
    'specificationdatetype',
    'links',
]

uuuu = '''
class Records(BaseModel):    
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True,help_text='主键', )            
'''
uadd = '''
class RecordsModel():
    def __init__(self):
        super(RecordsModel, self).__init__() 
    @staticmethod
    def add_rec(the_data):     
        Records.create(      
            uid = the_data['uid'] 
'''


def echo_schema(fields):
    print(fields)
    print('=' * 40)
    print(uuuu.strip())

    for field in fields:
        print(f"    {field} = peewee.CharField(default='', help_text='{field}')")
        # print(f"    {field}  CHAR , ")
        # print(f"    info.extinfo.get('dde_{field}'), ")
    print('-' * 40)
    print(uadd.strip())
    for field in fields:
        print(f"            {field} = the_data['{field}'],")
    print('            )')
    print('-' * 40)


def add_test_data(data):
    # print(data)
    RecordsModel.add_rec(data)


if __name__ == '__main__':
    # echo_schema(PYCSW_DB_FIELD)
    data_list = []
    for ii in range(40):
        data = {'uid': 'xx_' + get_uuid()}
        for field in PYCSW_DB_FIELD:
            # print(field)
            data[field] = field.strip() + str(ii)
        # print(data)
        add_test_data(data=data)
