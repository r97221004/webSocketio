import socket

serveraddress = ("127.0.0.1", 5000)

sk = socket.socket()
sk.connect(serveraddress)

sss = "abc"
sk.sendall(sss.encode())

answer = sk.recv(1024).decode()
print(f"收到伺服器的應答: {answer}")

sk.close()
