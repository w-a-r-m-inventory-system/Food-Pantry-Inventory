import socket
from sys import argv

def test_socket(ip,port):
        s = socket.socket()

        try:
            s.settimeout(3)
            s.connect((ip,port))
        except socket.error as msg:
            s.close()
            print(f'could not open {ip}:{port}')
            return(1)
        else:
            s.close()
            print(f'{ip}:{port} is OK')
            return(0)

if __name__ == '__main__':
    host = argv[1]
    port = int(argv[2])
    print(f"testing {host} {port}")
    status = test_socket(host, port)
    exit(status)