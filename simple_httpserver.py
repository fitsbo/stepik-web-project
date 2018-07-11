import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8080))
s.listen(10)

while True:
    conn, addr = s.accept()
    path = conn.recv(512).decode('utf8').rstrip("\r\n")
    file = open('/www' + str(path), 'r')
    data = file.read().encode('utf8')
    conn.sendall(data)
    file.close()
    conn.close()
