import lib
import random

def findId():
    #注意改host
    ms = lib.mssql(host="39.107.241.25", user="SA", pwd="lqdLQD!!", db="BombGame")
    ls = ms.ExecQuery("select rid from room where created = 0")
    return ls[random.randint(0,len(ls))][0]

def main():

    print(findId())

if __name__ == '__main__':
    main()