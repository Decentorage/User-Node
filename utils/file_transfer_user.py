import socket
from time import sleep
import json
import os
import zmq
import pickle
from .audits import generate_audits
from .decentorage import shard_done_uploading
helper = None
semaphore = None


def init_file_transfer_user(helper_obj, semaphore_obj):
    global helper, semaphore
    helper = helper_obj
    semaphore = semaphore_obj


def send_data(request, start, ui):
    context = zmq.Context()
    client_socket = context.socket(zmq.PAIR)
    client_socket.connect("tcp://" + request['ip'] + ":" + str(request['port']))

    frame = client_socket.recv()
    frame = pickle.loads(frame)

    # keep track of sending status
    success = True
    print("Connected to server")
    f = open(request['shard_id'], "rb")
    if not start:
        resume_frame = client_socket.recv()
        resume_frame = pickle.loads(resume_frame)
        resume_msg = resume_frame["data"]
        print(resume_msg)
        f.seek(resume_msg, 0)

    data = f.read(1024)
    client_socket.RCVTIMEO = 1000
    while data:
        try:
            data_frame = {"type": "data", "data": data}
            data_frame = pickle.dumps(data_frame)
            client_socket.send(data_frame)
            ack_frame = client_socket.recv()
            data = f.read(1024)

        except:
            print("Disconnected")
            sleep(5)
            connected = False
            try:
                client_socket = context.socket(zmq.PAIR)
                client_socket.connect("tcp://" + request['ip'] + ":" + str(request['port']))
                client_socket.RCVTIMEO = 1000*60*60

                # received start frame, reconnected to host
                start_frame = client_socket.recv()
                start_frame = pickle.loads(frame)
                print("Reconnected Successfully")

                # get from host where it has received
                resume_frame = client_socket.recv()
                resume_frame = pickle.loads(resume_frame)
                resume_msg = resume_frame["data"]
                print(resume_msg)
                f.seek(resume_msg, 0)
                client_socket.RCVTIMEO = 1000

                data = f.read(1024)
            except:
                print("Unable to reconnect, terminating connection")
                success = False
                break

    if success:
        end_frame = {"type": "END"}
        end_frame = pickle.dumps(end_frame)
        client_socket.send(end_frame)
        print("sending end connection to port", request['ip'], request['port'])

    f.close()
    client_socket.close()

    connections = {}
    semaphore.acquire()

    # Generate audits
    audits = generate_audits(request["shard_id"])
    print("Segment#", request['segment_number'], "Shard#", request['shard_index'], "--------audits generated.--------")
    transfer_obj = read_transfer_file()
    transfer_obj['segments'][request['segment_number']]['shards'][request['shard_index']]['done_uploading'] = True
    save_transfer_file(transfer_obj)
    shard_done_uploading(request["shard_id"], audits, ui)

    # remove from text file
    with open(helper.upload_connection_file) as json_file:
        connections = json.load(json_file)
    connections['connections'].remove(request)
    with open(helper.upload_connection_file, 'w') as outfile:
        json.dump(connections, outfile)
    semaphore.release()
    print("Done uploading")


def receive_data(request):

    context = zmq.Context()
    client_socket = context.socket(zmq.PAIR)
    client_socket.connect("tcp://" + request['ip'] + ":" + str(request['port']))

    # receive start frame
    frame = client_socket.recv()
    frame = pickle.loads(frame)

    connected = True
    f = None

    # if file exists, resume upload, open in append mode, inform sender where it has stopped
    if os.path.isfile(request['shard_id']):
        file_size = os.path.getsize(request['shard_id'])
        resume_frame = {"type": "resume", "data": file_size}
        resume_frame = pickle.dumps(resume_frame)
        client_socket.send(resume_frame)

        f = open(request['shard_id'], "ab")
        print("Resume download from ", f.tell())

    # if file does not exist, start download
    else:
        print("Starting download")
        f = open(request['shard_id'], "wb")

    client_socket.RCVTIMEO = 1000
    while True:
        try:
            frame = client_socket.recv()
            frame = pickle.loads(frame)

            if frame["type"] == "data":
                # ack_frame = {"type": "ACK"}
                # ack_frame = pickle.dumps(ack_frame)
                # client_socket.send(ack_frame)
                data = frame["data"]
                f.write(data)

            elif frame["type"] == "END":
                f.close()
                print("Download complete")
                break

        except:
            print("Disconnected")
            sleep(5)

            connected = False
            try:
                client_socket = context.socket(zmq.PAIR)
                client_socket.connect("tcp://" + request['ip'] + ":" + str(request['port']))
                client_socket.RCVTIMEO = 1000 * 60 * 60

                # received start frame, reconnected to host
                start_frame = client_socket.recv()
                start_frame = pickle.loads(frame)
                print("Reconnected Successfully")

                # send host where it has received
                f.close()
                file_size = os.path.getsize(request['shard_id'])
                resume_frame = {"type": "resume", "data": file_size}
                resume_frame = pickle.dumps(resume_frame)
                client_socket.send(resume_frame)
                print("Resume download from ", file_size)

                f = open(request['shard_id'], "ab")
                client_socket.RCVTIMEO = 1000

            except:
                print("Unable to reconnect, terminating connection")
                break

    client_socket.close()
    f.close()
    # remove from text file
    connections = {}
    with open(helper.upload_connection_file) as json_file:
        connections = json.load(json_file)
    connections['connections'].remove(request)
    with open(helper.upload_connection_file, 'w') as outfile:
        json.dump(connections, outfile)


# incomplete active connections
def check_old_connections(ui):
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
                send_data(request, False, ui)
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


def read_transfer_file():
    if not os.path.exists(helper.transfer_file):
        raise Exception('Cache file deleted')
    else:
        outfile = open(helper.transfer_file, 'r')
        transfer_obj = json.load(outfile)
        return transfer_obj


def save_transfer_file(transfer_obj):
    if not os.path.exists(helper.transfer_file):
        raise Exception('Cache file deleted')
    else:
        outfile = open(helper.transfer_file, 'w')
        json.dump(transfer_obj, outfile)