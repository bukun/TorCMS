

import os
from pathlib import Path
from cfg import DB_CFG

# Headless， 提供服务
pycsw_cfg_svr = Path('./pycsw/default.cfg')

# 独立站点，通过Web页面查看
pycsw_cfg_portal = Path('./pycsw/default_portal.cfg')


def chuli_cfg_svr():
    cnts = open('./pycsw/default-sample.cfg').readlines()

    with open(pycsw_cfg_svr, 'w') as fo:

        for cnt in cnts:

            if 'home=' in cnt:
                fo.write(
                    'home=' + os.path.join(os.getcwd(), 'pycsw') + '\n'
                )

            elif 'database=sqlite' in cnt:
                fo.write(
                    # f'database=sqlite:///{os.getcwd()}/cite.db'
                    'database=postgresql://{}:{}@localhost'.format(
                        DB_CFG['db'],
                        DB_CFG['pass']
                    )
                )
                fo.write('\n')
            elif cnt.startswith('url='):
                fo.write(
                    f'url=https://drr.ikcest.org/csw'
                    # f'url=http://47.104.152.23:6793'
                )
                fo.write('\n')
            elif 'federatedcatalogues' in cnt:
                # 联合检索。此处配置外部资源，不需要再添加本pycsw服务
                fo.write(
                    'federatedcatalogues=https://csw.deep-time.org/csw,http://geocatalog.webservice-energy.org/geonetwork/srv/eng/csw'
                )
                fo.write('\n')

            else:
                if cnt.startswith('#'):
                    continue
                fo.write(cnt)


def chuli_cfg_portal():

    cnts = open(pycsw_cfg_svr).readlines()
    with open(pycsw_cfg_portal, 'w') as fo:
        for cnt in cnts:
            if cnt.startswith('url='):
                fo.write(
                    f'url=http://47.104.152.23:6794'
                )
                fo.write('\n')
            else:
                fo.write(cnt)


def chuli_run():
    with open('run_pycsw_portal.sh', 'w') as fo:
        fo.write('cp -r /home/bk/deploy/fangzai/pycsw/pycsw/ogc/api/templates/* pycsw/pycsw/ogc/api/templates/')
        fo.write('\n')
        fo.write(
            f'. ./vpy_csw/bin/activate && export PYCSW_CONFIG={pycsw_cfg_portal.resolve()} && cd pycsw && python3 ./pycsw/wsgi_flask.py'
        )

    with open('run_pycsw_svr.sh', 'w') as fo:
        fo.write(
            f'. ./vpy_csw/bin/activate && export PYCSW_CONFIG={pycsw_cfg_svr.resolve()} && cd pycsw && python3 ./pycsw/wsgi.py'
        )


def chuli_port():
    wfile = 'pycsw/pycsw/wsgi.py'
    cnts = open(wfile).readlines()
    with open(wfile, 'w') as fo:
        for cnt in cnts:
            if '8000' in cnt:
                cnt = cnt.replace('8000', '6793')
            fo.write(cnt)

    wfile = 'pycsw/pycsw/wsgi_flask.py'
    cnts = open(wfile).readlines()
    with open(wfile, 'w') as fo:
        for cnt in cnts:
            if '8000' in cnt:
                cnt = cnt.replace('8000', '6794')
            fo.write(cnt)


if __name__ == '__main__':
    chuli_run()
    chuli_cfg_svr()
    chuli_cfg_portal()
    chuli_port()
