'''
使用psycopg2连接。
'''

from cfg import PostGIS_CFG
import psycopg2


class PGINFO():

    def __init__(self):
        self.conn = psycopg2.connect(
            database=PostGIS_CFG['db'],
            user=PostGIS_CFG['user'],
            password=PostGIS_CFG['pass'],
            host=PostGIS_CFG['host'], port="5432"
        )

    def query_meta(self, fea_name):
        sql_str = f'select rid, (ST_Metadata(rast)).* from {fea_name}'
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        for cur in cursor:
            print(cur)

    def stats(self, fea_name):
        sql_str = f"""
        WITH stats AS ( SELECT (ST_SummaryStats(rast, 1)).* FROM xx_tmp
        WHERE rid = 1
        )
        SELECT count, sum, round(mean::numeric, 2) AS mean,
        round(stddev::numeric, 2) AS stddev, min, max FROM stats;
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        for cur in cursor:
            print(cur)

    def histogram(self, fea_name):
        sql_str = f"""
    WITH hist AS (
        SELECT  (ST_Histogram(rast, 1)).*   FROM xx_tmp
        WHERE rid = 1   )
    SELECT  round(min::numeric, 2) AS min,  round(max::numeric, 2) AS max,
        count,  round(percent::numeric, 2) AS percent
    FROM hist ORDER BY min;
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        for cur in cursor:
            print(cur)

    def quantile(self, fea_name):
        sql_str = f"""
        SELECT  (ST_Quantile(rast, 1)).*
    FROM xx_tmp
    WHERE rid = 1;
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        for cur in cursor:
            print(cur)

    def value_count(self, fea_name):
        sql_str = f"""
            SELECT (ST_ValueCount(rast, 1)).* FROM xx_tmp
    WHERE rid = 1 ORDER BY count DESC, value LIMIT 10;
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        for cur in cursor:
            print(cur)


if __name__ == '__main__':
    pginfo = PGINFO()
    pginfo.query_meta('xx_tmp')
    pginfo.stats('xx_tmp')
    pginfo.histogram('xx_tmp')
    pginfo.quantile('xx_tmp')
    pginfo.value_count('xx_tmp')
