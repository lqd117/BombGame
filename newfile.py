import socket,sys,select
import threading,time

target_host = '39.107.241.25'
target_port = 40000

#建立一个socket对象,AF_INET说明将使用标准的IPv4地址或主机名，SOCK_STREAM说明是一个TCP客户端
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#连接到服务器
client.connect((target_host, target_port))

flag = 0
id = 0

def handle_udp():
    global client,id,flag
    length = 0
    while 1:
        client.send(('askStart'+';' + str(id)).encode())
        temp = client.recv(4096).decode('utf-8')
        if temp == 'YES':
            break
        time.sleep(1)
    print('----------------------------')
    flag = 1
    while 1 < 4*60*60:
        temp = 'askData' + ';' + str(id) +';'+str(length)
        client.send(temp.encode())
        string = client.recv(4096).decode('utf-8')
        arr = string.split(':')
        if arr[0] != 'N':
            print(arr[0].split('#'))
            length = int(arr[1])
    flag = 0
global udp_handle
udp_handle = threading.Thread(target=handle_udp)
#udp_handle.start()


def main():
    global udp_handle,client,flag,id
    string = input()
    client.sendall(string.encode())
    id = client.recv(1024).decode('utf-8')
    print(id)
    udp_handle.start()
    while 1:
        string = input()
        if flag == 1:
            string = "gaming;"+ str(id) + ";" + string
        if string == "startGame":
            string = string + ";" + str(id)
        client.send(string.encode())
        print(client.recv(1024).decode('utf-8'))


if __name__ == '__main__':
    main()
