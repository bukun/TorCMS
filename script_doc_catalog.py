import yaml
import json

from torcms.model.mcatalog import MCatalog

mcat  = MCatalog()

f = open('./database/meta/doc_catalog.yaml')
out_dic = yaml.load(f)
print(out_dic)
vv = json.dumps(out_dic, indent=2)

porder = 0
sorder = 0
for key in out_dic:

    if key.endswith('00'):
        uid = key[1:]
        print(uid)
        cur_dic = out_dic[key]
        porder = cur_dic['order']
        cat_dic = {
            'uid': uid,
            'slug': [cur_dic['slug']],
            'name': [cur_dic['name']],
            'count': [0],
            'order':[porder * 100],
        }

        mcat.insert_data(uid, cat_dic)
    else:
        sub_arr = out_dic[key]
        pid = key[1:3]

        for sub_dic in sub_arr:
            print('x' * 10)
            print(sub_dic)
            # cur_dic = sub_dic
            porder = out_dic['z' + pid + '00']['order']
        
            for key in sub_dic:
                
                uid = key[1:]


                cur_dic = sub_dic[key]

                sorder = cur_dic['order']
                cat_dic = {
                    'uid': uid,
                    'slug': [cur_dic['slug']],
                    'name': [cur_dic['name']],
                    'count': [0],
                    'order': [porder *100 +sorder],
                }

                mcat.insert_data( pid + uid, cat_dic)
