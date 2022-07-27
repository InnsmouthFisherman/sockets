import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'

try:
    PORT = int(sys.argv[1])
except Exception as ex:
    print('Usage: python3 main.py <port>\n' + str(ex))
    sys.exit(1)


def main():
    s.bind((HOST, PORT))
    s.listen(10)
    print('RSBF server listening on port {}...'.format(PORT))

    conn, _ = s.accept()

    while True:
        cmd = input('RSBF> ').rstrip()

        if cmd == '':
            continue

        conn.send(bytes(cmd, encoding="utf-8", errors="ignore"))

        if cmd == 'exit':
            s.close()
            sys.exit(0)

        if cmd[:7] == "getfile":
            f = open("FILENAME.txt", "wb")
            while True:
                data = conn.recv(4096)
                print('reading data')
                if not data:
                    print('done')
                    break
                f.write(data)
                print('writing data')
            f.close()
            print('Done sending\n')

        data = conn.recv(4096)
        print(str(data, encoding="utf-8", errors="ignore"))


if __name__ == '__main__':
    main()