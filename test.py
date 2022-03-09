from http import server
from multiprocessing.connection import wait
import socket
import sys
import threading
from time import sleep
from requests import get

socket_list = []
# server side application


def fn_server():
    # creating socket in TCP IPv4
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allows to reuse socket
    # needed to avoid errors
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # binding socket
    IP = socket.gethostname()
    Port = int(sys.argv[1])
    server_socket.bind((IP, Port))
    # put it in listen mode
    server_socket.listen(5)

    thread_list = []
    # creating clietns dictionary
    clients = {}

    def recv(name, s):
        while True:
            try:
                response = s.recv(4096)
                print(response.decode())
            except:
                s.close()

    while True:
        # we recive address and client's socket
        clientsocket, addr = server_socket.accept()
        # print clients address
        print(f'\nConnection from: {addr} has been established')
        print("Please provide your input: ")

        msg = 'Welcome to the server'
        if clientsocket not in socket_list:
            # adding client to a client list if we dont have him already
            socket_list.append(clientsocket)
            # creating thread for client messg reciver
            t = threading.Thread(target=recv, args=(
                "RecvThread", clientsocket))
            t.start()
            # adding thread to a thread list
            thread_list.append(t)


# client side application
client_socket_list = []


def fn_client(IP, port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = "127.0.0.1"
    s.connect((IP, int(port)))
    client_socket_list.append(s)

    def recv(name, s):
        while True:
            try:
                response = s.recv(4096)
                print(response.decode())
            except:
                s.close()

    t = threading.Thread(target=recv, args=("RecvThread", s))
    t.start()


def send(sock):
    try:
        text = input("Your message: ")
        sock.send(text.encode())
    except:
        pass
        sock.close()


def terminate(connection):
    comb_socket_list = client_socket_list + socket_list
    comb_socket_list[connection].close()
    if connection in client_socket_list:
        client_socket_list.remove(comb_socket_list[connection])
    else:
        socket_list.remove(comb_socket_list[connection])
    comb_socket_list.pop(connection)


def checkConnection():
    while(True):
        comb_socket_list = client_socket_list + socket_list
        for sock in comb_socket_list:
            print(sock.fileno())
        sleep(5)

# where the actual program begins


def main():
    if(sys.argv[1]):
        server_thread = threading.Thread(target=fn_server)
        server_thread.start()
    else:
        print("Please specify port")

    sleep(0.2)

    connectionCheck_thread = threading.Thread(target=checkConnection)
    connectionCheck_thread.start()

    while(True):
        inp = input("Please provide your input: ")
        if(inp == "help"):
            print("1) myip - provides information about your external ip")
            print("2) myport - provides information about your server port")
            print("3) connect  <destination>  <port>")
            print("4) list - provides information about connected clients to you")
            print(
                "5) terminate  <connection  id.>  - terminates connection with the provided client")
            print("6) send  <connection id.>  <message> - sends message to the client")
            print("7) exit - close the application")
        elif(inp == "1"):
            ip = get('https://api.ipify.org').content.decode('utf8')
            print("Your ip is: " + ip)
        elif(inp == "2"):
            print(sys.argv[1])
        elif(inp == "3"):
            ip = input("Enter ip: ")
            port = int(input("Enter port: "))
            fn_client(ip, port)
        elif(inp == "4"):
            print("#\tIP\t\tPort")
            i = 0
            for j in range(len(client_socket_list)):
                csl = client_socket_list[j].getsockname()
                print(str(i) + ")\t" + str(csl[0]) + "\t" + str(csl[1]))
                i += 1
            for j in range(len(socket_list)):
                csl = socket_list[j].getpeername()
                print(str(i) + ")\t" + str(csl[0]) + "\t" + str(csl[1]))
                i += 1
        elif(inp == "5"):
            terminate(int(input("Enter which connection to terminate: ")))
        elif(inp == "6"):
            comb_socket_list = client_socket_list + socket_list
            num = int(input("Enter socket number: "))
            send(comb_socket_list[num])
        elif(inp == "7"):
            exit()
        else:
            print("Wrong input, for help type \"help\"")


main()
