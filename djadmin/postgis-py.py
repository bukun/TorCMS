import psycopg2
from cfg import DB_INFO

# 建立数据库连接
con = psycopg2.connect(database='geodjango',
                       user=DB_INFO['USER'],
                       password=DB_INFO['PASSWORD'],
                       host="localhost",
                       port=DB_INFO['PORT'])
# 调用游标对象
cur = con.cursor()
# 用cursor中的execute 使用DDL语句创建一个名为 STUDENT 的表,指定表的字段以及字段类型
cur.execute('''select * from  world_worldborder''')

# 提交更改，增添或者修改数据只会必须要提交才能生效
info = cur.fetchone()
print(info)
con.commit()
con.close()

