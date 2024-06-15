import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost', int(sys.argv[1])))

print(f'listening on {sys.argv[1]}')

while True:
  data, addr = s.recvfrom(1024)
  print(data)
