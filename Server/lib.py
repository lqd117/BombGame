import pymssql


class Mssql(object):
    def __init__(self, host: str, user: str, pwd: str, db: str):
        self.conn = pymssql.connect(host=host, user=user, password=pwd, database=db, charset="utf8")
        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "连接数据库失败")

    def ExecQuery(self, sql: str):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        """
        self.cur.execute(sql)
        resList = self.cur.fetchall()
        return resList

    def ExecNonQuery(self, sql: str):
        self.cur.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.close()


def main():
    pass


if __name__ == '__main__':
    main()
