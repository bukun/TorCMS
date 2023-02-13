from pprint import pprint
import copy
from torcms.model.post_model import MPost

recs = MPost.query_all(kind='9', limit=999999)
field_dic = {
    'tag_identifier', 'tag_title', 'tag_title_alternate', 'tag_parentidentifier', 'tag_topicategory',
    'tag_language', 'tag_type', 'tag_format', 'tag_abstract', 'tag_keywords', 'tag_links', 'tag_time_begin',
    'tag_time_end', 'tag_creator', 'tag_publisher', 'tag_contributor', 'tag_organization', 'tag_operateson',
    'tag_anytext', 'tag_typename', 'tag_classification', 'tag_schema', 'tag_mdsource', 'tag_insert_date', 'tag_xml',
    'tag_resourcelanguage', 'tag_keywordstype', 'tag_relation', 'tag_securityconstraints', 'tag_accessconstraints',
    'tag_otherconstraints', 'tag_date', 'tag_date_revision', 'tag_date_creation', 'tag_date_publication',
    'tag_date_modified', 'tag_source', 'tag_crs', 'tag_geodescode', 'tag_denominator', 'tag_distancevalue',
    'tag_distanceuom', 'tag_wkt_geometry', 'tag_servicetype', 'tag_servicetypeversion', 'tag_operation',
    'tag_couplingtype', 'tag_operatesonidentifier', 'tag_operatesoname', 'tag_degree',
    'tag_conditionapplyingtoaccessanduse', 'tag_lineage', 'tag_responsiblepartyrole', 'tag_specificationtitle',
    'tag_specificationdate', 'tag_specificationdatetype'
}
for rec in recs:
    print('=' * 40)
    pprint(rec.extinfo)
    rec_extinfo = copy.deepcopy(rec.extinfo)
    upp = False
    for key in rec.extinfo:
        if key in field_dic:
            # print(key, rec_extinfo[key])
            new_key = str(key).replace('tag_', 'pycsw_')
            if new_key in rec_extinfo:
                pass
            else:
                upp = True
                rec_extinfo[new_key] = rec_extinfo[key]

    if upp:
        pprint(rec_extinfo)
        # pass
        MPost.update_jsonb(rec.uid, rec_extinfo)
