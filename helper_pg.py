from cfg import DB_INFO
import psycopg2

# 连接数据库的参数

dbname = DB_INFO['NAME']
user = DB_INFO['USER']
password = DB_INFO['PASSWORD']
host = DB_INFO['HOST']
port = 5432

# 连接字符串
conn_string = f"host={host} port={port} dbname={dbname} user={user} password={password}"

# 建立连接
conn = psycopg2.connect(conn_string)

# 创建cursor对象
cursor = conn.cursor()
cursor.execute('select * from tabpost')
print(cursor)
tal_struct = cursor.description
for  col in tal_struct:
    print(col.name, col.type_code, col.table_column)
    pass

tab_header = [desc[0] for desc in tal_struct]
#  select * from information_schema.columns  where table_schema='table_schema' and table_name='tabpost'

print(tab_header)
cursor.execute('''
select * from information_schema.columns  where  table_name='tabpost'
''')

for rec in cursor.fetchall():
    print(rec)

cursor.close()
conn.close()