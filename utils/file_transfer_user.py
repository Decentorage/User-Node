import socket
from time import sleep
import json
import os
settings = None


def init_file_transfer_user(settings_obj):
    global settings
    settings = settings_obj


def send_data(request, ip, start):
    client_socket = socket.socket()
    client_socket.connect((ip, request['port']))

    # keep track of connection status
    connected = True
    print("connected to server")

    f = open(request['shard_id'], "rb")
    if not start:
        resume_msg = client_socket.recv(1024).decode("UTF-8")
        print(resume_msg)
        f.seek(int(resume_msg), 0)

    data2 = f.read(1024)

    while data2:
        try:
            client_socket.send(data2)
            sleep(0.5)
            data2 = f.read(1024)
        except socket.error:
            print("disconnected")
            connected = False
            while not connected:
                try:
                    client_socket = socket.socket()
                    client_socket.connect((ip, request['port']))            # get from receiver where it has stopped
                    connected = True
                    resume_msg = client_socket.recv(1024).decode("UTF-8")
                    print(resume_msg)
                    f.seek(int(resume_msg), 0)
                    data2 = f.read(1024)
                    print("reconnecting")
                except socket.error:
                    sleep(2)
                    print("sleep")

    f.close()
    client_socket.close()
    # remove from text file
    data = {}
    with open(settings.upload_connection_file) as json_file:
        data = json.load(json_file)
    data['connections'].remove(request)
    with open(settings.upload_connection_file, 'w') as outfile:
        json.dump(data, outfile)

    print("Done sending...")


def receive_data(request, ip):
    client_socket = socket.socket()
    client_socket.connect((ip, request['port']))

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
            data2 = client_socket.recv(1024)
            while data2:
                f.write(data2)
                data2 = client_socket.recv(1024)
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
                    client_socket.connect((ip, request['port']))
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
    data = {}
    with open(settings.upload_connection_file) as json_file:
        data = json.load(json_file)
    data['connections'].remove(request)
    with open(settings.upload_connection_file, 'w') as outfile:
        json.dump(data, outfile)


# incomplete active connections
def check_old_connections():
    try:
        data = {}
        with open(settings.upload_connection_file) as json_file:
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
def add_connection(request):
    try:
        data = {}
        with open(settings.upload_connection_file) as json_file:
            data = json.load(json_file)
        data['connections'].append(request)
        with open(settings.upload_connection_file, 'w') as outfile:
            json.dump(data, outfile)

    except:
        print("Error")

#=================================================================
# req = { 'type': 'upload',
#    'port': int(2000),
#    'shard_id': '',
#    'auth':'dwwewrew',
#    'size':1024}

#send_data(req, True)
