import socket
import time

target_host = '127.0.0.1'
target_port = 40000

#建立一个socket对象,AF_INET说明将使用标准的IPv4地址或主机名，SOCK_STREAM说明是一个TCP客户端
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1)

#连接到服务器
client.connect((target_host, target_port))


tot = 0
while(1):
    tot = tot + 1
    string = input()
    client.send(string.encode())
    print(client.recv(4096).decode('utf-8'))



