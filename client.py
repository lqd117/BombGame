import socket

target_host = '127.0.0.1'
target_port = 12345

#建立一个socket对象,AF_INET说明将使用标准的IPv4地址或主机名，SOCK_STREAM说明是一个TCP客户端
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#连接到服务器
client.connect((target_ip, target_port))

#发送数据
client.send("i am TCP client")

#接收数据
response = client.recv(4096)

print response