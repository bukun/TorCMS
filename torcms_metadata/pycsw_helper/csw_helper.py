# -*- coding:utf-8 -*-
import peewee
from peewee import SqliteDatabase

try:
    from cfg import CSW_DB
    pycsw_db = SqliteDatabase(CSW_DB)
except:
    pycsw_db = SqliteDatabase('xx_meta.db')


class SPATIAL_REF_SYS(peewee.Model):
    class Meta:
        database = pycsw_db

    '''
    srid INTEGER NOT NULL,
    auth_name TEXT,
    auth_srid INTEGER,
    srtext TEXT,
    PRIMARY KEY (srid)
    '''
    srid = peewee.IntegerField(null=False, primary_key=True)
    auth_name = peewee.TextField(null=True)
    auth_srid = peewee.IntegerField(null=True)
    srtext = peewee.TextField(null=True)


class GEOMETRY_COLUMNS(peewee.Model):
    class Meta:
        database = pycsw_db

    '''
    f_table_catalog TEXT NOT NULL,
    f_table_schema TEXT NOT NULL,
    f_table_name TEXT NOT NULL,
    f_geometry_column TEXT NOT NULL,
    geometry_type INTEGER,
    coord_dimension INTEGER,
    srid INTEGER NOT NULL,
    geometry_format TEXT NOT NULL
    '''
    f_table_catalog = peewee.TextField(null=False)
    f_table_schema = peewee.TextField(null=False)
    f_table_name = peewee.TextField(null=False)
    f_geometry_column = peewee.TextField(null=False)
    geometry_type = peewee.IntegerField(null=True)
    coord_dimension = peewee.IntegerField(null=True)
    srid = peewee.IntegerField(null=False, primary_key=True)
    geometry_format = peewee.TextField(null=False)


class Records(peewee.Model):
    '''
    identifier TEXT NOT NULL,
    typename TEXT NOT NULL,
    schema TEXT NOT NULL,
    mdsource TEXT NOT NULL,
    insert_date TEXT NOT NULL,
    xml TEXT NOT NULL,
    anytext TEXT NOT NULL,
    '''

    class Meta:
        database = pycsw_db

    identifier = peewee.TextField(null=False, index=True, primary_key=True, unique=True)
    typename = peewee.TextField(null=False)
    schema = peewee.TextField(null=False)
    mdsource = peewee.TextField(null=False)
    insert_date = peewee.TextField(null=False)
    xml = peewee.TextField(null=False)
    anytext = peewee.TextField(null=False)
    language = peewee.TextField(null=True, default='')
    type = peewee.TextField(null=True, default='')
    title = peewee.TextField(null=True, default='')
    title_alternate = peewee.TextField(null=True, default='')
    abstract = peewee.TextField(null=True, default='')
    keywords = peewee.TextField(null=True, default='')
    keywordstype = peewee.TextField(null=True, default='')
    parentidentifier = peewee.TextField(null=True, default='')
    relation = peewee.TextField(null=True, default='')
    time_begin = peewee.TextField(null=True, default='')
    time_end = peewee.TextField(null=True, default='')
    topicategory = peewee.TextField(null=True, default='')
    resourcelanguage = peewee.TextField(null=True, default='')
    creator = peewee.TextField(null=True, default='')
    publisher = peewee.TextField(null=True, default='')
    contributor = peewee.TextField(null=True, default='')
    organization = peewee.TextField(null=True, default='')
    securityconstraints = peewee.TextField(null=True, default='')
    accessconstraints = peewee.TextField(null=True, default='')
    otherconstraints = peewee.TextField(null=True, default='')
    date = peewee.TextField(null=True, default='')
    date_revision = peewee.TextField(null=True, default='')
    date_creation = peewee.TextField(null=True, default='')
    date_publication = peewee.TextField(null=True, default='')
    date_modified = peewee.TextField(null=True, default='')
    format = peewee.TextField(null=True, default='')
    source = peewee.TextField(null=True, default='')
    crs = peewee.TextField(null=True, default='')
    geodescode = peewee.TextField(null=True, default='')
    denominator = peewee.TextField(null=True, default='')
    distancevalue = peewee.TextField(null=True, default='')
    distanceuom = peewee.TextField(null=True, default='')
    wkt_geometry = peewee.TextField(null=True, default='')
    servicetype = peewee.TextField(null=True, default='')
    servicetypeversion = peewee.TextField(null=True, default='')
    operation = peewee.TextField(null=True, default='')
    couplingtype = peewee.TextField(null=True, default='')
    operateson = peewee.TextField(null=True, default='')
    operatesonidentifier = peewee.TextField(null=True, default='')
    operatesoname = peewee.TextField(null=True, default='')
    degree = peewee.TextField(null=True, default='')
    classification = peewee.TextField(null=True, default='')
    conditionapplyingtoaccessanduse = peewee.TextField(null=True, default='')
    lineage = peewee.TextField(null=True, default='')
    responsiblepartyrole = peewee.TextField(null=True, default='')
    specificationtitle = peewee.TextField(null=True, default='')
    specificationdate = peewee.TextField(null=True, default='')
    specificationdatetype = peewee.TextField(null=True, default='')
    links = peewee.TextField(null=True, default='')


class MRecords(object):

    def delete(self, del_id):
        entry = Records.delete().where(Records.identifier == del_id)
        entry.execute()
        return True

    def add_or_update(self, postdata, force=False):
        uid = postdata['identifier']
        if self.get_by_uid(uid):
            if force:
                print('To Del ..................')
                self.delete(uid)
            else:
                return
        self.add(postdata)

    def add(self, postdata):
        '''
        命令行更新的
        '''
        Records.create(
            identifier=postdata["identifier"],
            typename=postdata["typename"],
            schema=postdata["schema"],
            mdsource=postdata["mdsource"],
            insert_date=postdata["insert_date"],
            xml=postdata["xml"],
            anytext=postdata["anytext"],
            language=postdata["language"],
            type=postdata["type"],
            title=postdata["title"],
            title_alternate=postdata["title_alternate"],
            abstract=postdata["abstract"],
            keywords=postdata["keywords"],
            keywordstype=postdata["keywordstype"],
            parentidentifier=postdata["parentidentifier"],
            relation=postdata["relation"],
            time_begin=postdata["time_begin"],
            time_end=postdata["time_end"],
            topicategory=postdata["topicategory"],
            resourcelanguage=postdata["resourcelanguage"],
            creator=postdata["creator"],
            publisher=postdata["publisher"],
            contributor=postdata["contributor"],
            organization=postdata["organization"],
            securityconstraints=postdata["securityconstraints"],
            accessconstraints=postdata["accessconstraints"],
            otherconstraints=postdata["otherconstraints"],
            date=postdata["date"],
            date_revision=postdata["date_revision"],
            date_creation=postdata["date_creation"],
            date_publication=postdata["date_publication"],
            date_modified=postdata["date_modified"],
            format=postdata["format"],
            source=postdata["source"],
            crs=postdata["crs"],
            geodescode=postdata["geodescode"],
            denominator=postdata["denominator"],
            distancevalue=postdata["distancevalue"],
            distanceuom=postdata["distanceuom"],
            wkt_geometry=postdata["wkt_geometry"],
            servicetype=postdata["servicetype"],
            servicetypeversion=postdata["servicetypeversion"],
            operation=postdata["operation"],
            couplingtype=postdata["couplingtype"],
            operateson=postdata["operateson"],
            operatesonidentifier=postdata["operatesonidentifier"],
            operatesoname=postdata["operatesoname"],
            degree=postdata["degree"],
            classification=postdata["classification"],
            conditionapplyingtoaccessanduse=postdata["conditionapplyingtoaccessanduse"],
            lineage=postdata["lineage"],
            responsiblepartyrole=postdata["responsiblepartyrole"],
            specificationtitle=postdata["specificationtitle"],
            specificationdate=postdata["specificationdate"],
            specificationdatetype=postdata["specificationdatetype"],
            links=postdata["links"],
        )
        return postdata["identifier"]

    def get_by_uid(self, sig):
        try:
            return Records.get(identifier=sig)
        except:
            return False


def init_table():
    GEOMETRY_COLUMNS.create_table()
    Records.create_table()
    SPATIAL_REF_SYS.create_table()

    '''
    'public', 'public', 'records', 'wkt_geometry', 3, 2, 4326, 'WKT'
    '''
    if GEOMETRY_COLUMNS.select().where(GEOMETRY_COLUMNS.srid == 4326):
        pass
    else:
        GEOMETRY_COLUMNS.create(
            f_table_catalog='public',
            f_table_schema='public',
            f_table_name='records',
            f_geometry_column='wkt_geometry',
            geometry_type=3,
            coord_dimension=2,
            srid=4326,
            geometry_format='WKT')
    '''
    4326,'EPSG',4326,
    'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'
    '''
    if SPATIAL_REF_SYS.select().where(SPATIAL_REF_SYS.srid == 4326):
        pass
    else:
        SPATIAL_REF_SYS.create(
            srid=4326,
            auth_name='EPSG',
            auth_srid=4326,
            srtext='GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'
        )


init_table()
