import os
from pathlib import Path
from cfg import DB_CFG

pycsw_cfg_file = Path('./pycsw/default.cfg')


def chuli_cfg():
    cnts = open('./pycsw/default-sample.cfg').readlines()

    with open(pycsw_cfg_file, 'w') as fo:

        for cnt in cnts:

            if cnt.startswith('#'):
                continue

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
                    # f'url=https://drr.ikcest.org/csw/'
                    f'url=http://47.104.152.23:6793'
                )
                fo.write('\n')

            else:
                fo.write(cnt)


def chuli_run():
    with open('run_pycsw.sh', 'w') as fo:
        fo.write('cp -r /home/bk/deploy/fangzai/pycsw/pycsw/ogc/api/templates/* pycsw/pycsw/ogc/api/templates/')
        fo.write('\n')
        fo.write(
            f'. ./vpy_csw/bin/activate && export PYCSW_CONFIG={pycsw_cfg_file.resolve()} && cd pycsw && python3 ./pycsw/wsgi_flask.py'
        )


def chuli_port():
    wsfiles = ['pycsw/pycsw/wsgi_flask.py', 'pycsw/pycsw/wsgi.py']
    for wfile in wsfiles:
        cnts = open(wfile).readlines()
        with open(wfile, 'w') as fo:
            for cnt in cnts:
                if '8000' in cnt:
                    cnt = cnt.replace('8000', '6793')
                fo.write(cnt)


if __name__ == '__main__':
    chuli_run()
    chuli_cfg()
    chuli_port()
