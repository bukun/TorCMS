


def do_cabpost():
    from model_ent.post_model import MPost as MPostOld
    mpost_old = MPostOld()

    from torcms.model.post_model import MPost

    mpost = MPost()
    post_recs = mpost_old.query_all()
    for post_rec in post_recs:
        # print(post_rec.uid)
        post_data = {
            'title': [post_rec.title],
            'user_name': post_rec.user_name,
            'logo': [post_rec.logo],
            'cnt_md': [post_rec.cnt_md],
            'keywords': [post_rec.keywords],
            'type': 1
        }
        print(post_rec.uid)
        mpost.add_or_update(post_rec.uid, post_data)


def do_tabapp():
    from torcms.model.post_model import MPost

    mpost = MPost()

    from model_ent.infor_model import MInfor
    minfor = MInfor()
    info_recs = minfor.query_all(20000)
    for info_rec in info_recs:
        # print(info_rec.uid)
        post_data = {
            'title': [info_rec.title],
            'user_name': info_rec.user_name,
            'logo': [info_rec.logo],
            'cnt_md': [info_rec.cnt_md],
            'keywords': [info_rec.keywords],
            'type': 2,
            'extinfo': info_rec.extinfo,
        }
        # mpost.insert_data('m' + info_rec.uid, post_data)
        mpost.add_or_update('g' + info_rec.uid, post_data)

        # mpost.update(post_rec.uid, post_data)


def do_cabcatalog():
    from torcms.model.category_model import MCategory
    mcat = MCategory()

    from model_ent.postcatalog_model import MPostCatalog
    mpostcat = MPostCatalog()

    for cat in mpostcat.query_all():

        post_data = {
            'name': [cat.name],
            'slug': [ cat.slug],
            'order': [cat.order],
            'uid': cat.uid,
            'type': 10,
        }

        mcat.insert_data(cat.uid, post_data)
        # mpostcat.update(cat.uid, post_data)

    from model_ent.inforcatalog_model import MInforCatalog

    minfocat = MInforCatalog()
    for cat in minfocat.query_all():
        # print(cat.uid)
        post_data = {
            'name': [cat.name],
            'slug': ['g' + cat.slug],
            'order': [cat.order],
            'uid': cat.uid,
            'type': 20,
        }
        mcat.insert_data(cat.uid, post_data)


def do_app2catalog():
    from torcms.model.post2catalog_model import MPost2Catalog as MPost2Tag
    mpost2tag = MPost2Tag()

    from model_ent.post2catalog_model import MPost2Catalog
    mpost2cat = MPost2Catalog()

    raw_recs = mpost2cat.query_all(limit_num = 200000)
    for raw_rec in raw_recs:
        # print(raw_rec.uid)
        # if raw_rec.catalog.uid.startswith('0'):
        #     uid = 'a' + raw_rec.catalog.uid[1:]
        # else:
        #     uid = 'b' + raw_rec.catalog.uid[1:]
        mpost2tag.add_record(raw_rec.post.uid, raw_rec.catalog.uid, raw_rec.order)


    from model_ent.infor2catalog_model import MInfor2Catalog
    minfo2cat = MInfor2Catalog()

    raw_recs = minfo2cat.query_all(2000000)
    for raw_rec in raw_recs:
        # print(raw_rec.uid)
        # if raw_rec.catalog.uid.startswith('0'):
        #     uid = 'a' + raw_rec.catalog.uid[1:]
        # else:
        #     uid = 'b' + raw_rec.catalog.uid[1:]
        mpost2tag.add_record('g' + raw_rec.post.uid, raw_rec.catalog.uid, raw_rec.order)


def do_post_label():
    from model_ent.label_model import MLabel
    mlabel = MLabel()

    from torcms.model.category_model import MCategory as MPostCatalog
    mcat = MPostCatalog()

    for rec in mlabel.query_all(limit_num=200000):
        post_data = {
            'name': [rec.name],
            'slug': [rec.uid],
            'order': [1],
            'uid': rec.uid,
            'type': 11,
        }
        mcat.insert_data(convert_20d(rec.uid[:4]), post_data
                         )
        pass


def do_app_label():
    from model_ent.infor2label_model import MInforLabel
    mlabel = MInforLabel()

    from torcms.model.category_model import MCategory
    mcat = MCategory()

    for rec in mlabel.query_all(limit_num=200000):
        post_data = {
            'name': [rec.name],
            'slug': [rec.uid],
            'order': [1],
            'uid': rec.uid,
            'type': 21,
        }
        mcat.insert_data(convert_20d(rec.uid), post_data
                         )


def do_post2label():
    from model_ent.label_model import MPost2Label
    mlabel = MPost2Label()

    from torcms.model.post2catalog_model import MPost2Catalog
    mcat = MPost2Catalog()

    for rec in mlabel.query_all(limit_num=200000):
        mcat.add_record(rec.app.uid, convert_20d(rec.tag.uid))


def do_app2label():
    from model_ent.infor2label_model import MInfor2Label
    mlabel = MInfor2Label()

    from torcms.model.post2catalog_model import MPost2Catalog
    mcat = MPost2Catalog()

    for rec in mlabel.query_all(limit_num=200000):
        # print(rec.app.uid)
        mcat.add_record('g' + rec.app.uid, convert_20d(rec.tag.uid))


def convert_20d(instr):
    redic = {
        '0': 'g',
        '1': 'h',
        '2': 'i',
        '3': 'j',
        '4': 'k',
        '5': 'l',
        '6': 'm',
        '7': 'n',
        '8': 'o',
        '9': 'p',
        'a': 'q',
        'b': 'r',
        'c': 's',
        'd': 't',
        'e': 'u',
        'f': 'v'
    }
    addic = {
        '0': 'w',
        '1': 'w',
        '2': 'w',
        '3': 'w',
        '4': 'x',
        '5': 'x',
        '6': 'x',
        '7': 'x',
        '8': 'y',
        '9': 'y',
        'a': 'y',
        'b': 'y',
        'c': 'z',
        'd': 'z',
        'e': 'z',
        'f': 'z'
    }

    outstr = redic[instr[0]] + redic[instr[1]] + redic[instr[2]]  + redic[instr[3]]
    return  outstr

def do_member():
    from model_ent.user_model import MUser as OldUser

    mraw_user = OldUser()

    from torcms.model.user_model import MUser

    muser = MUser()

    for uu in mraw_user.query_all(limit_num=200000):
        data_dic = {

        }
        muser.insert_data()


def do_wiki():
    # from torcms.model.wiki_model import MWiki
    # mwiki = MWiki()
    #
    # from torcms.model.page_model import MPage
    # mpage = MPage()

    from model_ent.wiki_model import MWiki as OldWiki
    from model_ent.page_model import MPage as OldPage
    oldwiki = OldWiki()
    oldpage = OldPage()

    print('got it')

    abc = oldwiki.query_all(limit_num=2000)
    print(abc.count())

    ded = oldpage.query_all()
    print(ded.count())
    for rec in oldwiki.query_all(limit_num=20000):
        post_data = {
        "uid":  rec.uid,
        "title": rec.title,
        "date": rec.date,
        "time_create":  rec.time_create,
        "user_name": rec.user_name,
        "time_update":  rec.time_update,
        "view_count": rec.view_count,
        "cnt_md": rec.cnt_md,
        "cnt_html": rec.cnt_html,
        "type": 1,
        }
        print(rec.title)
        # mwiki.insert_data(post_data)


    print('QED')



if __name__ == '__main__':
    # do_cabpost()
    # do_tabapp()
    # do_cabcatalog()
    # do_app2catalog()
    # do_post_label()
    # do_app_label()
    # do_post2label()
    # do_app2label()
    do_wiki()