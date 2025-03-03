'''
列出没有 "_en_" 文件的uid
保存在 xx_data_uid.txt 文件中
'''

import os
import pathlib


def test_get_meta():
    meta_base = './static/dataset_list'
    if os.path.exists(meta_base):
        pass
    else:
        return False
    results = []
    existing_data = []

    for wroot, wdirs, wfiles in os.walk(meta_base):
        for wdir in wdirs:
            if wdir.startswith('dataset'):
                sig = str(wdir)[-6:]

                ds_base = pathlib.Path(os.path.join(wroot, wdir))

                for uu in ds_base.iterdir():
                    if (
                        uu.name.startswith('meta')
                        and uu.name.endswith('.xlsx')
                        and '_en_' in uu.name
                    ):
                        existing_data.append(sig)
                    else:
                        continue
                results.append(sig)

    for data_uid in existing_data:
        if data_uid in results:
            results.remove(data_uid)

    # return results
    assert results


#
# if __name__ == '__main__':
#     output = get_meta()
#
#     f = open('./xx_data_uid.txt', 'w')
#     f.write(str(output))
#     f.close()
