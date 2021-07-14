import socket
import threading
from time import sleep
import sys
import json
import time
import os
ip = "192.168.1.7"


def send_data(request, start):
    clientSocket = socket.socket()
    clientSocket.connect((ip, request['port']))

    # keep track of connection status
    connected = True
    print("connected to server")

    f = open(request['shard_id'], "rb")
    if not start:
        resume_msg = clientSocket.recv(1024).decode("UTF-8")
        print(resume_msg)
        f.seek(int(resume_msg), 0)

    datas = f.read(1024)

    while datas:
        try:
            clientSocket.send(datas)
            sleep(0.5)
            datas = f.read(1024)
        except socket.error:
            print("disconnected")
            connected = False
            while not connected:
                try:
                    clientSocket = socket.socket()
                    clientSocket.connect((ip, request['port']))            # get from receiver where it has stopped
                    connected = True
                    resume_msg = clientSocket.recv(1024).decode("UTF-8")
                    print(resume_msg)
                    f.seek(int(resume_msg), 0)
                    datas = f.read(1024)
                    print("reconnecting")
                except socket.error:
                    sleep(2)
                    print("sleep")

    f.close()
    clientSocket.close()
    # remove from text file
    data = {}
    with open('connections.txt') as json_file:
        data = json.load(json_file)
    data['connections'].remove(request)
    with open('connections.txt', 'w') as outfile:
        json.dump(data, outfile)

    print("Done sending...")


def receive_data(request):
    clientSocket = socket.socket()
    clientSocket.connect((ip, request['port']))

    connected = True
    f = None

    # if file exists, resume upload, open in append mode, inform sender where it has stopped
    if os.path.isfile(request['shard_id']):
        clientSocket.send(bytes(str(os.path.getsize(request['shard_id'])), "UTF-8"))
        f = open(request['shard_id'], "ab")
        print(f.tell())
    # if file does not exist, start upload
    else:
        f = open(request['shard_id'], "wb")

    while True:
        try:
            datas = clientSocket.recv(1024)
            while datas:
                f.write(datas)
                datas = clientSocket.recv(1024)
            f.close()
            break

        except socket.error:
            # set connection status and recreate socket
            connected = False
            print("connection lost... reconnecting")
            while not connected:
                # attempt to reconnect, otherwise sleep for 2 seconds
                try:
                    clientSocket = socket.socket()
                    clientSocket.connect((ip, request['port']))
                    connected = True
                    f.close()
                    clientSocket.send(bytes(str(os.path.getsize(request['shard_id'])), "UTF-8"))
                    f = open(request['shard_id'], "ab")
                    print("re-connection successful")
                except socket.error:
                    sleep(2)
                    print("sleep")

    clientSocket.close()
    # remove from text file
    data = {}
    with open('connections.txt') as json_file:
        data = json.load(json_file)
    data['connections'].remove(request)
    with open('connections.txt', 'w') as outfile:
        json.dump(data, outfile)

req = { 'type': 'upload',
    'port': int(sys.argv[1]),
    'shard_id': sys.argv[2],
    'auth':'dwwewrew',
    'size':1024}

# uncomplete active connections
try:
    data = {}
    with open('connections.txt') as json_file:
        data = json.load(json_file)
except:
    print("Error in file")
finally:
    for i in range(len(data['connections'])):
        request = dict(data['connections'][i])
        if request['type'] == 'upload':
            send_data(request, False)
        elif request['type'] == 'download':
            receive_data(request)


# add new connection to file
try:
    data = {}
    with open('connections.txt') as json_file:
        data = json.load(json_file)
    data['connections'].append(req)
    with open('connections.txt', 'w') as outfile:
        json.dump(data, outfile)
    # send port to decentorage
except:
    print("Error")

send_data(req, True)