# --coding:utf-8--
# 运行django时报错“django_site” 表不存在,运行此脚本进行生成创建表并插入一条信息.
# 对应两种不同数据库，sqlite与postgresql的不同方式。运行前确认使用的数据库，对应使用相应的函数方法.
import sqlite3
import psycopg2
from cfg import DB_INFO

def edit_sqlite():
    # 连接到数据库
    conn = sqlite3.connect('db.sqlite3')
    # 创建一个游标对象
    cursor = conn.cursor()
    # 执行SQL语句
    cursor.execute("create table IF NOT EXISTS django_site(id integer, domain varchar(100), name varchar(50));")
    cursor.execute("insert into django_site(id, domain, name) values(1, 'htt', 'hta');")

    # 提交事务
    conn.commit()
    # 获取查询结果
    result = cursor.execute("SELECT * FROM django_site").fetchall()
    print(result)
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
def edit_postgresql():
    print('postgresql')

    # 连接到PostgreSQL数据库
    conn = psycopg2.connect(
            dbname=DB_INFO['NAME'],
            user=DB_INFO['USER'],
            password=DB_INFO['PASSWORD'],
            host=DB_INFO['HOST'],
            port=DB_INFO['PORT'],
    )

    # 创建一个cursor对象
    cur = conn.cursor()

    # 创建表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS django_site (
        id integer PRIMARY KEY,
        domain varchar(100),
        name varchar(50) 
    );
    """)

    # 向表中添加一条信息
    cur.execute("INSERT INTO django_site(id, domain, name) VALUES (1, 'htt', 'hta')", )

    # 提交事务
    conn.commit()

    # 关闭cursor和连接
    cur.close()
    conn.close()
if __name__ == '__main__':
    edit_postgresql()
