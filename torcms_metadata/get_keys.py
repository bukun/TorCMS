
from openpyxl import load_workbook


def get_xlsx():
    xlsx_list = ['./meta_元数据模板20220921.xlsx']
    lists = []
    for xl in xlsx_list:
        wb = load_workbook(xl)
        ws = wb['Sheet1']
        for x in ws.rows:
            if x[0].value:
                field_slug = x[0].value.replace(' ','_').replace('\n','')

                field = x[4].value.replace('\n', '')
                if field not in lists:lists.append({field_slug:field})
    return lists

uuuu = '''
class TabGaoshi(BaseModel):    
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True,help_text='主键', )            
'''
uadd= '''
class TabGaoshi():
    def __init__(self):
        super(TabGaoshi, self).__init__() 
    @staticmethod
    def add_rec(the_data):     
        TabGaoshi.create(       
'''
def echo_schema(fields):
    print(fields)
    print('=' * 40)
    # print(uuuu.strip())
    # for field in fields:
    #     for field_slug,field_val in field.items():
    #
    #         print(f"    {field_slug} = peewee.CharField(default='', help_text='{field_val}')")
    #
    # print('-' * 40)
    # print(uadd.strip())
    # for field in fields:
    #     for field_slug,field_val in field.items():
    #         print(f"            {field_slug} = the_data['{field_slug}'],")
    # print('            )')
    # print('-' * 40)
    #
    # print("view.html")
    # for field in fields:
    #     for field_slug,field_val in field.items():
    #
    #
    #         print(f" {{% if postinfo.extinfo.get('pycsw_{field_slug}') %}}  <div class='row'> <div class='col-sm-4'> <span class='des'> <strong>{{{{ _('{field_val}') }}}} </strong></span> </div><div class='col-sm-8'><span class='val'> {{{{postinfo.extinfo.get('pycsw_{field_slug}','') }}}} </span> </div> </div><div class='bor_bottom'> </div>{{% end %}}")
    #
    # print('            )')
    # print('-' * 40)
    # print("add.html")
    # for field in fields:
    #     for field_slug, field_val in field.items():
    #
    #
    #
    #         print(
    #             f"   <div class='form-group'> <label class='col-sm-2 control-label' for='pycsw_{field_slug}'>{{{{ _('{field_val}') }}}}</label> <div class='col-sm-10'> <input class='form-control' type='text' id='pycsw_{field_slug}' name='pycsw_{field_slug}'></div></div>")
    #
    # print('            )')
    # print('-' * 40)
    # print("edit.html")
    # for field in fields:
    #     for field_slug, field_val in field.items():
    #
    #         print(
    #             f"  <div class='form-group'> <label class='col-sm-2 control-label' for='pycsw_{field_slug}'>{{{{ _('{field_val}') }}}}</label> <div class='col-sm-10'> <input class='form-control' type='text' id='pycsw_{field_slug}' name='pycsw_{field_slug}' value='{{{{ postinfo.extinfo.get('pycsw_{field_slug}','')  }}}}'></div></div>")
    #
    # print('            )')

    # print("index.html")
    # for field in fields:
    #     for field_slug, field_val in field.items():
    #         print(
    #             f"    <th>{field_val}</th> ")
    #
    # print('            )')

    # print("td_value.html")
    # for field in fields:
    #     for field_slug, field_val in field.items():
    #         print(
    #             f"    <td>{{{{postinfo.{field_slug}}}}}</td> ")
    #
    # print('            )')

    print("index.html")
    for field in fields:
        for field_slug, field_val in field.items():
            print(
                f"'tag_{field_slug}',")

    print('            )')


def get_keys():
    lists = get_xlsx()
    echo_schema(lists)

if __name__ == '__main__':
    get_keys()