# -*- encoding:utf-8 -*-

'''
自动生成根据进行转换的APP
'''
import os

import yaml

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_js(uu):
    ulist = uu['p']
    tmp_arr = []
    for u in ulist:
        # (p, desc) = u.split(':')
        # p,desc = u.enumerate()
        # p = u.key

        for p in u.keys():
            # p = u.keys()
            # desc = u[p]
            desc = u[p]
            tmp_str = '''var {0} =  parseFloat($('#{0}').val())'''.format(p)
            tmp_arr.append(tmp_str)

    return ';\n'.join(tmp_arr)


def get_momo(uu):
    # for key in uu.keys():
    tpl_str = '''<div  class="form-group">
        <label for="{0}" class="col-sm-2 control-label">{0}—{1}</label>
        <div class="col-sm-8">
        <input class="form-control" id="{0}" type="text" name="{0}" placeholder="{0}">
        </div></div>
        '''
    ulist = uu['p']
    tmp_arr = []
    # (p, desc) = uu['res1'].split(':')
    # tmp_arr.append(tpl_str.format(p, desc))
    for u in ulist:
        # (p, desc) = u.split(':')
        for p in u.keys():
            desc = u[p]
            tmp_str = tpl_str.format(p, desc)
            tmp_arr.append(tmp_str)

    return ''.join(tmp_arr)


def get_res_desc(uu):
    # for key in uu.keys():
    tpl_str = '''{0}—{1}'''

    # (p, desc) = uu['res1'].split(':')
    return ''  # tpl_str.format(p, desc)


def get_fun_p(uu):
    tpl_str = '''{0} = float(self.get_argument('{0}'))'''
    ulist = uu['p']
    tmp_arr = []
    for u in ulist:
        (p, desc) = u.split(':')
        tmp_arr.append(' ' * 12 + tpl_str.format(p.strip()))
    return '\n'.join(tmp_arr)


def get_result(uu):
    res_tpl = '''<div class="form-group"><label for="nnnn" class="col-sm-2 control-label">zzzz</label>
    <div class="col-sm-10"><input class="form-control" name="nnnn" id="nnnn" type="text" readonly></div></div>
'''
    res_str = ''
    for vv in uu['res']:
        # print(vv)
        # mm, nn = vv.split(':')
        for mm in vv.keys():
            nn = vv[mm]
            res_tmp_str = res_tpl.replace('zzzz', nn)
            res_tmp_str = res_tmp_str.replace('nnnn', mm)
            res_str += res_tmp_str
    return res_str


def get_show_json(uu):
    res_tpl = '''$("#aaaa").val(bbbb);
'''
    res_str = ''
    for vv in uu['res']:
        # print(vv)
        for mm in vv.keys():
            nn = vv[mm]
            # mm, nn = vv.split(':')
            res_tmp_str = res_tpl.replace('aaaa', mm)
            res_tmp_str = res_tmp_str.replace('bbbb', 'result["{0}"]'.format(mm))
            res_str += res_tmp_str
    return res_str


def get_calc_it(uu):
    equa_tpl = '''
        bbbb = ffff
            '''
    do_equa_str = ''
    # for vv, ww in zip(uu['py'], uu['res']):
    for xx in uu['res']:
        for key in xx.keys():
            val = xx[key]

            res_tmp_str = equa_tpl.replace('ffff', uu[key])
            # mm, nn = ww.split(':')
            res_tmp_str = res_tmp_str.replace('bbbb', key)
            # print(res_tmp_str)
            do_equa_str += res_tmp_str
            do_equa_str += ';'

    # 添加输出字典
    out_dic = '''        '''
    for ww in uu['res']:
        # mm, nn = ww.split(':')
        for mm in ww.keys():
            nn = ww[mm]
            tmp_str = '$("#{0}").val({0}) ; '.format(mm)
            out_dic += tmp_str
    # out_dic += '}'
    do_equa_str += out_dic
    return do_equa_str


def get_rule(equa):
    tpl_rule = '''dddd: {    required: true,  number: true    },
        '''
    rule_str = ''

    for uu in equa['p']:
        # aa, bb = uu.split(':')
        for aa in uu.keys():
            bb = uu[aa]
            # tmp_str = tpl_input.replace('aaaa', aa)
            # tmp_str = tmp_str.replace('bbbb', bb)
            # inputs_str += tmp_str

            # jsinput_str += tpl_input_js.replace('dddd', aa)
            rule_str += tpl_rule.replace('dddd', aa)
            # message_str += tpl_message.replace('dddd', aa)
    return rule_str


def get_message(equa):
    tpl_message = '''dddd: {required: "<span class='red'>请输入变量的值</span>",
     number: "<span class='red'>变量必须为数字</span>" },
    '''

    message_str = ''
    for uu in equa['p']:
        # aa, bb = uu.split(':')

        for aa in uu.keys():
            bb = uu[aa]

            message_str += tpl_message.replace('dddd', aa)
    return message_str


def gen_out(sig, uuin, out_dir_sig):
    result_dir = './templates/jshtml/1_auto/{0}'.format(out_dir_sig)
    if os.path.exists(result_dir):
        pass
    else:
        os.makedirs(result_dir)
    uu = uuin
    uu['type'] = 2
    uu['html_path'] = 'autogen_python_equation/{0}'.format(sig)
    uu['sig'] = sig

    out_str = ''
    with open(os.path.join(dir_path, './tpl_html.html')) as fi:
        cnts = fi.read()
        cnts = cnts.replace('uuuu', uu['sig'])
        # cnts = cnts.replace('vvvv', uu['latex'])
        cnts = cnts.replace('xxxx', uu['title'])
        cnts = cnts.replace('yyyy', get_js(uu))
        cnts = cnts.replace('zzzz', get_momo(uu))
        cnts = cnts.replace('rrrr', get_result(uu))
        # cnts = cnts.replace('cccc', get_res_desc(uu))
        cnts = cnts.replace('mmmm', get_show_json(uu))
        cnts = cnts.replace('bbbb', uu['title'])
        cnts = cnts.replace('ssss', get_rule(uu))
        cnts = cnts.replace('tttt', get_message(uu))

        cnts = cnts.replace('resres', get_calc_it(uu))

        out_str = cnts

    with open(
        './templates/jshtml/1_auto/{0}/{1}.html'.format(out_dir_sig, sig), 'w'
    ) as fo:
        fo.write(out_str)

    out_str2 = ''
    with open(os.path.join(dir_path, './tpl_html_js.html')) as fi:
        cnts = fi.read()
        cnts = cnts.replace('uuuu', uu['sig'])
        # cnts = cnts.replace('vvvv', uu['latex'])
        cnts = cnts.replace('xxxx', uu['title'])
        cnts = cnts.replace('yyyy', get_js(uu))
        cnts = cnts.replace('zzzz', get_momo(uu))
        cnts = cnts.replace('rrrr', get_result(uu))
        # cnts = cnts.replace('cccc', get_res_desc(uu))
        cnts = cnts.replace('mmmm', get_show_json(uu))
        cnts = cnts.replace('bbbb', uu['title'])
        cnts = cnts.replace('ssss', get_rule(uu))
        cnts = cnts.replace('tttt', get_message(uu))

        cnts = cnts.replace('resres', get_calc_it(uu))
        out_str2 = cnts

    with open(
        './templates/jshtml/1_auto/{0}/{1}_js.html'.format(out_dir_sig, sig), 'w'
    ) as fo:
        fo.write(out_str2)


def run_gen_formula():
    # tpl_run = open('./tpl_run.py').read()
    out_dir_sig = 'formula'
    inws = 'out'
    print(os.path.abspath('out'))
    for wroot, wdirs, wfiles in os.walk(inws):
        for wfile in wfiles:
            if wfile.endswith('.yaml'):
                print(wfile)
                tsig = wfile[:-5].split('_')[-1]
                if tsig.startswith('s'):
                    yaml_file = os.path.join(wroot, wfile)
                    s = yaml.load(open(yaml_file))

                    gen_out(tsig[1:], s, out_dir_sig)


if __name__ == '__main__':
    run_gen_formula()
