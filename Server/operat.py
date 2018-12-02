from lib import Mssql
import random


class Operat(Mssql):
    def __init__(self, HOST: str, USER: str, PWD: str, DB: str):
        super(Operat, self).__init__(HOST, USER, PWD, DB)

    # 创建房间时返回一个可以创建的房间Rid
    def _findCreateRid(self):
        ls = self.ExecQuery("select rid from room where num = 0")
        return int(ls[random.randint(0, len(ls) - 1)][0])

    # 改变某个表某个道具int值,num为变量
    def _changeInt(self, table: str, id: int, name: str, num: int):
        string = 'rid' if table == 'room' else 'id'
        self.ExecNonQuery(
            "update {table} set {name} = {num} where {string} = {id}".format(table=table, name=name, num=num,
                                                                             string=string, id=id))

    # 改变某个表某个道具string值,num为变量
    def _changeStr(self, table: str, id: int, name: str, num: str):
        string = 'rid' if table == 'room' else 'id'
        self.ExecNonQuery(
            "update {table} set {name} = '{num}' where {string} = {id}".format(table=table, name=name, num=num,
                                                                               string=string, id=id))

    # 改变某个id某个状态,num为增量
    def _changePerson(self, id: int, name: str, num: int):
        self.ExecNonQuery(
            "update person set {name} = {name} + {num} where id = {id}".format(name=name, num=num, id=id))

    # 改变某个房间的状态,num为增量
    def _changeRoom(self, rid: int, name: str, num: int):
        self.ExecNonQuery(
            "update room set {name} = {name} + {num} where rid = {rid}".format(name=name, num=num, rid=rid))

    # 展示某个id的所有情况
    def _display(self, id: int):
        ls = self.ExecQuery("select * from person where id = {id}".format(id=id))
        return ls[0]

    # 返回所有已被创建房间的状态
    def _askAllCreatedRoom(self):
        ls = self.ExecQuery("select * from room where num != 0")
        return ls

    # 返回所有在线ID名字
    def _askAllId(self):
        ls = self.ExecQuery("select name from person where live = 1 or rid != 0")
        return ls

    # 删除某个ID记录
    def _deletId(self, id: int):
        self.ExecNonQuery("delete from person where id = {id}".format(id=id))

    # 根据账号密码得到人物ID
    def _getId(self, user: str, pwd: str):
        id = self.ExecQuery(
            "select id from person where person.account = '{user}' and person.pwd = '{pwd}'".format(user=user, pwd=pwd))
        if len(id) == 0: return None
        return int(id[0][0])

    # 创建新的人物
    def _createNewId(self, user: str, pwd: str):
        self.ExecNonQuery("insert into person (name,rid,live,bomb,power,speed,account,pwd) " \
                          "values ('{user}',0,1,0,0,0,'{user}','{pwd}')".format(user=user, pwd=pwd))

    # 查找某个ID在哪个房间
    def _findRid(self, id: int):
        ls = self.ExecQuery("select rid from person where id = {id}".format(id=id))
        return int(ls[0][0])

    # 清空所有房间
    def _clearAllRoom(self):
        self.ExecNonQuery('update room set num = 0,play = 0,map = null,owner = null')
        self.ExecNonQuery('update person set rid = 0')


def main():
    c = Operat("39.107.241.25", "SA", "lqdLQD!!", "BombGame")
    print(c._askAllCreatedRoom())
    pass


if __name__ == '__main__':
    main()
