import os
from pathlib import Path
from cfg import DB_CFG

# Headless， 提供服务
pycsw_cfg_svr = Path('./zz_pycsw_drr/default_svr.cfg')

# 独立站点，通过Web页面查看
pycsw_cfg_portal = Path('./zz_pycsw_drr/default_portal.cfg')

pycsw_cfg_wdc = Path('./zz_pycsw_wdc/default_wdc.cfg')


def chuli_cfg_svr():
    cnts = open('./zz_pycsw_drr/default-sample.cfg').readlines()

    with open(pycsw_cfg_svr, 'w') as fo:

        for cnt in cnts:

            if 'home=' in cnt:
                fo.write(
                    f'home={pycsw_cfg_svr.parent.resolve()}' + '\n'
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
            elif cnt.startswith('table='):
                fo.write(
                    f'table=records_drr'
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


def chuli_cfg_wdc():
    cnts = open(pycsw_cfg_svr).readlines()
    with open(pycsw_cfg_wdc, 'w') as fo:
        for cnt in cnts:
            if cnt.startswith('url='):
                fo.write(
                    f'url=http://47.104.152.23:6795'
                )
                fo.write('\n')
            elif 'home=' in cnt:
                fo.write(
                    f'home={pycsw_cfg_wdc.resolve()}' + '\n'
                )
            elif cnt.startswith('table='):
                fo.write(
                    f'table=records_wdc'
                )
                fo.write('\n')
            else:
                fo.write(cnt)


def chuli_run():
    for wfile in [pycsw_cfg_wdc, pycsw_cfg_svr, pycsw_cfg_portal]:
        with open(f'xx_run_{wfile.stem}.sh', 'w') as fo:
            fo.write(
                'cp -r /home/bk/deploy/fangzai/pycsw/pycsw/ogc/api/templates/* ./zz_pycsw/pycsw/ogc/api/templates/')
            fo.write('\n')
            fo.write(
f'''. ~/usr/vpy_csw/bin/activate \\
    && export PYCSW_CONFIG={wfile.resolve()} \\
    && cd {wfile.parent.resolve()} \\
    && python3 ./pycsw/wsgi_flask.py'''
            )


def chuli_port():
    wfile = './zz_pycsw_drr/pycsw/wsgi.py'
    cnts = open(wfile).readlines()
    with open(wfile, 'w') as fo:
        for cnt in cnts:
            if '8000' in cnt:
                cnt = cnt.replace('8000', '6793')
            fo.write(cnt)

    wfile = './zz_pycsw_drr/pycsw/wsgi_flask.py'
    cnts = open(wfile).readlines()
    with open(wfile, 'w') as fo:
        for cnt in cnts:
            if '8000' in cnt:
                cnt = cnt.replace('8000', '6794')
            fo.write(cnt)


def chuli_init():
    init_file = 'xx_run_init.sh'
    with open(init_file, 'w') as fo:
        fo.write(
            '''
. ~/usr/vpy_csw/bin/activate && cd zz_pycsw_drr && pycsw-admin.py setup-db -c default_svr.cfg
. ~/usr/vpy_csw/bin/activate && cd zz_pycsw_wdc && pycsw-admin.py setup-db -c default_wdc.cfg            
            '''
        )


if __name__ == '__main__':
    chuli_run()
    chuli_cfg_svr()
    chuli_cfg_portal()
    chuli_cfg_wdc()
    chuli_port()
    chuli_init()
