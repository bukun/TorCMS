
安装了后在导出数据库时显示没有权限，需要下面的命令进行授权：

    GRANT USAGE ON SCHEMA public TO <user>;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO <user>;


##　安装　zhcfg

    Create extension zhparser;
    create text search configuration zhcfg(parser=zhparser);
    alter text search configuration zhcfg add mapping for n,v,a,i,e,j,l with simple;

##  全文检索

    sudo apt install postgresql-14-rum
    # PostgreSQL RUM access method

    # 管理员用户
    create extension rum;
    create table rum_test(c1 tsvector);
    CREATE INDEX rumidx ON rum_test USING rum (c1 rum_tsvector_ops);


    alter table tabpost add column tscontent tsvector;
    CREATE INDEX ON tabpost USING rum (tscontent rum_tsvector_ops);



要实现检索 ，入库时

    update tabpost set tscontent=to_tsvector(cnt_md);

中文：

    update tabpost set tscontent=to_tsvector('zhcfg', cnt_md);

检索： 

    select * from tabpost where  tscontent @@ '重要知识点';
    select * from rum_test where  c1 @@ to_tsquery('zhcfg', '重要知识点');
