from faker import Faker
from torcms.handlers.user_handler import MUser
from torcms.handlers.permission_handler import MPermission


class Create_Data(object):
    def __init__(self):
        # 选择中文
        fake = Faker('zh_CN')
        # 生成数据改变循环体来控制数据量rang(?)
        self.data_total = [
            [fake.name(), fake.job(), fake.company(), fake.phone_number(), fake.company_email(), fake.address(),
             fake.date_time(tzinfo=None)] for x in range(100)]
        print(self.data_total)

    def deal_postgresql(self):

        for val in self.data_total:
            post_data = {
                'user_name': val[0],
                'user_email': val[4],
                'user_pass': val[0],
            }

            MUser.create_user(post_data)


if __name__ == '__main__':
    data = Create_Data()

    # data.deal_postgresql()
