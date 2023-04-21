import socket

hostaddress = ("127.0.0.1", 5000)

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(hostaddress)
sk.listen(5)
print("啟動 socket 服務, 等待客戶端連接...")

conn, clientaddress = sk.accept()

data = conn.recv(1024).decode()
print("接收到客戶端 %s 發送來的信息: %s" % (clientaddress, data ))

res = data.upper()

conn.sendall(res.encode())
conn.close()

