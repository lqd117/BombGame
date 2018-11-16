from socketserver import BaseRequestHandler, TCPServer

#指定接收消息的客户端ip列表
target_clients = ["10.4.76.188"]

class EchoHandler(BaseRequestHandler):
    def handle(self):
        for target_client in target_clients:
            if target_client in self.client_address:
                print('Got connection from', self.client_address)
                msg = self.request.recv(8192)
                if not msg:
                    break
                ret_msg = bytes("自动回复：消息已收到！", encoding = "gbk")
                self.request.send(ret_msg)
                print(str(msg, encoding = "gbk"))
                break

if __name__ == '__main__':
    from threading import Thread
    NWORKERS = 16
    #绑定socket服务端所在ip和端口号
    serv = TCPServer(('', 20000), EchoHandler)
    for n in range(NWORKERS):
        t = Thread(target=serv.serve_forever)
        t.daemon = True
        t.start()
    serv.serve_forever()