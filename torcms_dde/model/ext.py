# -*- coding:utf-8 -*-

import peewee
from playhouse.postgres_ext import BinaryJSONField

from torcms.core.base_model import BaseModel


class Records(BaseModel):
    identifier = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        help_text='主键',
    )
    typename = peewee.CharField(default='', help_text='typename')
    schema = peewee.CharField(default='', help_text='schema')
    mdsource = peewee.CharField(default='', help_text='mdsource')
    insert_date = peewee.CharField(default='', help_text='insert_date')
    xml = peewee.CharField(default='', help_text='xml')
    anytext = peewee.CharField(default='', help_text='anytext')
    language = peewee.CharField(default='', help_text='language')
    type = peewee.CharField(default='', help_text='type')
    title = peewee.CharField(default='', help_text='title')
    title_alternate = peewee.CharField(default='', help_text='title_alternate')
    abstract = peewee.CharField(default='', help_text='abstract')
    keywords = peewee.CharField(default='', help_text='keywords')
    keywordstype = peewee.CharField(default='', help_text='keywordstype')
    parentidentifier = peewee.CharField(default='', help_text='parentidentifier')
    relation = peewee.CharField(default='', help_text='relation')
    time_begin = peewee.CharField(default='', help_text='time_begin')
    time_end = peewee.CharField(default='', help_text='time_end')
    topicategory = peewee.CharField(default='', help_text='topicategory')
    resourcelanguage = peewee.CharField(default='', help_text='resourcelanguage')
    creator = peewee.CharField(default='', help_text='creator')
    publisher = peewee.CharField(default='', help_text='publisher')
    contributor = peewee.CharField(default='', help_text='contributor')
    organization = peewee.CharField(default='', help_text='organization')
    securityconstraints = peewee.CharField(default='', help_text='securityconstraints')
    accessconstraints = peewee.CharField(default='', help_text='accessconstraints')
    otherconstraints = peewee.CharField(default='', help_text='otherconstraints')
    date = peewee.CharField(default='', help_text='date')
    date_revision = peewee.CharField(default='', help_text='date_revision')
    date_creation = peewee.CharField(default='', help_text='date_creation')
    date_publication = peewee.CharField(default='', help_text='date_publication')
    date_modified = peewee.CharField(default='', help_text='date_modified')
    format = peewee.CharField(default='', help_text='format')
    source = peewee.CharField(default='', help_text='source')
    crs = peewee.CharField(default='', help_text='crs')
    geodescode = peewee.CharField(default='', help_text='geodescode')
    denominator = peewee.CharField(default='', help_text='denominator')
    distancevalue = peewee.CharField(default='', help_text='distancevalue')
    distanceuom = peewee.CharField(default='', help_text='distanceuom')
    wkt_geometry = peewee.CharField(default='', help_text='wkt_geometry')
    servicetype = peewee.CharField(default='', help_text='servicetype')
    servicetypeversion = peewee.CharField(default='', help_text='servicetypeversion')
    operation = peewee.CharField(default='', help_text='operation')
    couplingtype = peewee.CharField(default='', help_text='couplingtype')
    operateson = peewee.CharField(default='', help_text='operateson')
    operatesonidentifier = peewee.CharField(
        default='', help_text='operatesonidentifier'
    )
    operatesoname = peewee.CharField(default='', help_text='operatesoname')
    degree = peewee.CharField(default='', help_text='degree')
    classification = peewee.CharField(default='', help_text='classification')
    conditionapplyingtoaccessanduse = peewee.CharField(
        default='', help_text='conditionapplyingtoaccessanduse'
    )
    lineage = peewee.CharField(default='', help_text='lineage')
    responsiblepartyrole = peewee.CharField(
        default='', help_text='responsiblepartyrole'
    )
    specificationtitle = peewee.CharField(default='', help_text='specificationtitle')
    specificationdate = peewee.CharField(default='', help_text='specificationdate')
    specificationdatetype = peewee.CharField(
        default='', help_text='specificationdatetype'
    )
    links = peewee.CharField(default='', help_text='links')
    metadata_type = peewee.CharField(default='', help_text='links')


class RecordsModel:
    def __init__(self):
        super(RecordsModel, self).__init__()

    @staticmethod
    def add_rec(the_data):
        Records.create(
            identifier=the_data['identifier'],
            typename=the_data['typename'],
            schema=the_data['schema'],
            mdsource=the_data['mdsource'],
            insert_date=the_data['insert_date'],
            xml=the_data['xml'],
            anytext=the_data['anytext'],
            language=the_data['language'],
            type=the_data['type'],
            title=the_data['title'],
            title_alternate=the_data['title_alternate'],
            abstract=the_data['abstract'],
            keywords=the_data['keywords'],
            keywordstype=the_data['keywordstype'],
            parentidentifier=the_data['parentidentifier'],
            relation=the_data['relation'],
            time_begin=the_data['time_begin'],
            time_end=the_data['time_end'],
            topicategory=the_data['topicategory'],
            resourcelanguage=the_data['resourcelanguage'],
            creator=the_data['creator'],
            publisher=the_data['publisher'],
            contributor=the_data['contributor'],
            organization=the_data['organization'],
            securityconstraints=the_data['securityconstraints'],
            accessconstraints=the_data['accessconstraints'],
            otherconstraints=the_data['otherconstraints'],
            date=the_data['date'],
            date_revision=the_data['date_revision'],
            date_creation=the_data['date_creation'],
            date_publication=the_data['date_publication'],
            date_modified=the_data['date_modified'],
            format=the_data['format'],
            source=the_data['source'],
            crs=the_data['crs'],
            geodescode=the_data['geodescode'],
            denominator=the_data['denominator'],
            distancevalue=the_data['distancevalue'],
            distanceuom=the_data['distanceuom'],
            wkt_geometry='POLYGON((35.82 25.67, 35.82 44.82, 42.11 44.82, 42.11 25.67, 35.82 25.67))',
            servicetype=the_data['servicetype'],
            servicetypeversion=the_data['servicetypeversion'],
            operation=the_data['operation'],
            couplingtype=the_data['couplingtype'],
            operateson=the_data['operateson'],
            operatesonidentifier=the_data['operatesonidentifier'],
            operatesoname=the_data['operatesoname'],
            degree=the_data['degree'],
            classification=the_data['classification'],
            conditionapplyingtoaccessanduse=the_data['conditionapplyingtoaccessanduse'],
            lineage=the_data['lineage'],
            responsiblepartyrole=the_data['responsiblepartyrole'],
            specificationtitle=the_data['specificationtitle'],
            specificationdate=the_data['specificationdate'],
            specificationdatetype=the_data['specificationdatetype'],
            links=the_data['links'],
            metadata_type='a',
        )
