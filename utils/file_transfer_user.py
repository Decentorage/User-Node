import socket
from time import sleep
import json
import threading
import os
helper = None
semaphore = threading.Semaphore()


def init_file_transfer_user(helper_obj):
    global helper
    helper = helper_obj


def send_data(request, start):
    client_socket = socket.socket()
    client_socket.connect((request['ip'], request['port']))

    # keep track of connection status
    connected = True
    print("connected to server")
    # TODO: Read from shards directory.
    f = open(request['shard_id'], "rb")
    if not start:
        resume_msg = client_socket.recv(1024).decode("UTF-8")
        print(resume_msg)
        f.seek(int(resume_msg), 0)

    data = f.read(1024)

    while data:
        try:
            client_socket.send(data)
            data = f.read(1024)
        except socket.error:
            print("disconnected")
            connected = False
            while not connected:
                try:
                    client_socket = socket.socket()
                    # get from receiver where it has stopped
                    client_socket.connect((request['ip'], request['port']))
                    connected = True
                    resume_msg = client_socket.recv(1024).decode("UTF-8")
                    print(resume_msg)
                    f.seek(int(resume_msg), 0)
                    data = f.read(1024)
                    print("reconnecting")
                except socket.error:
                    sleep(2)
                    print("sleep")

    client_socket.send(bytes("END", "UTF-8"))
    f.close()
    client_socket.close()
    # remove from text file
    connections = {}
    semaphore.acquire()
    with open(helper.upload_connection_file) as json_file:
        connections = json.load(json_file)
    connections['connections'].remove(request)
    with open(helper.upload_connection_file, 'w') as outfile:
        json.dump(connections, outfile)
    semaphore.release()
    print("Done sending...")


def receive_data(request):
    client_socket = socket.socket()

    client_socket.connect((request['ip'], request['port']))

    connected = True
    f = None

    # if file exists, resume upload, open in append mode, inform sender where it has stopped
    if os.path.isfile(request['shard_id']):
        client_socket.send(bytes(str(os.path.getsize(request['shard_id'])), "UTF-8"))
        f = open(request['shard_id'], "ab")
        print(f.tell())
    # if file does not exist, start upload
    else:
        f = open(request['shard_id'], "wb")

    while True:
        try:
            data = client_socket.recv(1024)
            while data:
                f.write(data)
                data = client_socket.recv(1024)
            f.close()
            break

        except socket.error:
            # set connection status and recreate socket
            connected = False
            print("connection lost... reconnecting")
            while not connected:
                # attempt to reconnect, otherwise sleep for 2 seconds
                try:
                    client_socket = socket.socket()
                    client_socket.connect((request['ip'], request['port']))
                    connected = True
                    f.close()
                    client_socket.send(bytes(str(os.path.getsize(request['shard_id'])), "UTF-8"))
                    f = open(request['shard_id'], "ab")
                    print("re-connection successful")
                except socket.error:
                    sleep(2)
                    print("sleep")

    client_socket.close()
    # remove from text file
    connections = {}
    with open(helper.upload_connection_file) as json_file:
        connections = json.load(json_file)
    connections['connections'].remove(request)
    with open(helper.upload_connection_file, 'w') as outfile:
        json.dump(connections, outfile)


# incomplete active connections
def check_old_connections():
    try:
        connections = {}
        with open(helper.upload_connection_file) as json_file:
            connections = json.load(json_file)

    except:
        print("Error in file")
    finally:
        for i in range(len(connections['connections'])):
            request = dict(connections['connections'][i])
            if request['type'] == 'upload':
                send_data(request, False)
            elif request['type'] == 'download':
                receive_data(request)


# add new connection to file
def add_connection(request):
    try:
        connections = {}
        with open(helper.upload_connection_file) as json_file:
            connections = json.load(json_file)
        connections['connections'].append(request)
        with open(helper.upload_connection_file, 'w') as outfile:
            json.dump(connections, outfile)

    except:
        print("Error")
