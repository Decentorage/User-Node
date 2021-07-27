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


def send_data(request, start, ui, progress_bar):
    context = zmq.Context()
    client_socket = context.socket(zmq.PAIR)
    client_socket.connect("tcp://" + request['ip'] + ":" + str(request['port']))
    print("Connected to host", "tcp://" + request['ip'] + ":" + str(request['port']))
    frame = client_socket.recv()
    frame = pickle.loads(frame)

    print("Received start frame")
    # keep track of sending status
    success = True
    f = open(request['shard_id'], "rb")
    if not start:
        resume_frame = client_socket.recv()
        resume_frame = pickle.loads(resume_frame)
        resume_msg = resume_frame["data"]
        print(resume_msg)
        f.seek(resume_msg, 0)

    print("chunk size:", helper.send_chunk_size)
    data = f.read(helper.send_chunk_size)
    client_socket.RCVTIMEO = helper.receive_timeout
    print("Start sending data to host")
    while data:
        try:
            data_frame = {"type": "data", "data": data}
            data_frame = pickle.dumps(data_frame)
            client_socket.send(data_frame)
            ack_frame = client_socket.recv()
            data = f.read(helper.send_chunk_size)
            progress_bar(helper.send_chunk_size)
        except:
            print("Connection Lost")
            sleep(5)
            connected = False
            try:
                print("trying to reconnect")
                client_socket.close()
                client_socket = context.socket(zmq.PAIR)
                client_socket.connect("tcp://" + request['ip'] + ":" + str(request['port']))
                client_socket.RCVTIMEO = helper.disconnect_timeout
                print("connected to", "tcp://" + request['ip'] + ":" + str(request['port']))

                # received start frame, reconnected to host
                print("waiting to receive start frame")
                start_frame = client_socket.recv()
                start_frame = pickle.loads(start_frame)
                print(start_frame["type"], "Reconnected Successfully")

                # get from host where it has received
                resume_frame = client_socket.recv()
                resume_frame = pickle.loads(resume_frame)
                resume_msg = resume_frame["data"]
                print(resume_msg)
                f.seek(resume_msg, 0)
                client_socket.RCVTIMEO = helper.receive_timeout

                data = f.read(helper.send_chunk_size)
                progress_bar(helper.send_chunk_size)
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
    transfer_obj = helper.read_transfer_file()
    transfer_obj['segments'][request['segment_number']]['shards'][request['shard_index']]['done_uploading'] = True
    helper.save_transfer_file(transfer_obj)
    shard_done_uploading(request["shard_id"], audits, ui)

    # remove from text file
    with open(helper.upload_connection_file) as json_file:
        connections = json.load(json_file)
    connections['connections'].remove(request)
    with open(helper.upload_connection_file, 'w') as outfile:
        json.dump(connections, outfile)
    semaphore.release()
    print("Done uploading")


def receive_data(request, progress_bar):

    context = zmq.Context()
    client_socket = context.socket(zmq.PAIR)
    client_socket.connect("tcp://" + request['ip'] + ":" + str(request['port']))
    print("Connected to host", "tcp://" + request['ip'] + ":" + str(request['port']))
    # receive start frame
    frame = client_socket.recv()
    frame = pickle.loads(frame)
    print("recieved start frame")

    connected = True
    f = None

    # if file exists, resume upload, open in append mode, inform sender where it has stopped
    if os.path.isfile(os.path.join(helper.shards_directory_path, request['shard_id'])):
        print("resume")
        file_size = os.path.getsize(os.path.join(helper.shards_directory_path, request['shard_id']))
        resume_frame = {"type": "resume", "data": file_size}
        resume_frame = pickle.dumps(resume_frame)
        client_socket.send(resume_frame)

        f = open(os.path.join(helper.shards_directory_path, request['shard_id']), "ab")
        print("Resume download from ", f.tell())

    # if file does not exist, start download
    else:
        print("Starting download")
        f = open(os.path.join(helper.shards_directory_path, request['shard_id']), "wb")

    client_socket.RCVTIMEO = helper.receive_timeout
    while True:
        try:
            frame = client_socket.recv()
            frame = pickle.loads(frame)
            print(frame["type"])
            if frame["type"] == "data":
                data = frame["data"]
                f.write(data)
                print("received frame ", frame["type"])
                progress_bar(helper.send_chunk_size, "download")
                print("sending ack frame")
                ack_frame = {"type": "ACK"}
                ack_frame = pickle.dumps(ack_frame)
                client_socket.send(ack_frame)
                print("sent ack")

            elif frame["type"] == "END":
                f.close()
                print("Download complete")
                break

        except:
            print("Disconnected")
            sleep(5)

            connected = False
            #try:
            client_socket.close()
            client_socket = context.socket(zmq.PAIR)
            client_socket.connect("tcp://" + request['ip'] + ":" + str(request['port']))
            client_socket.RCVTIMEO = helper.disconnect_timeout

            # received start frame, reconnected to host
            start_frame = client_socket.recv()
            start_frame = pickle.loads(start_frame)
            print("Reconnected Successfully")

            # send host where it has received
            f.close()
            file_size = os.path.getsize(os.path.join(helper.shards_directory_path, request['shard_id']))
            resume_frame = {"type": "resume", "data": file_size}
            resume_frame = pickle.dumps(resume_frame)
            client_socket.send(resume_frame)
            print("Resume download from ", file_size)

            f = open(os.path.join(helper.shards_directory_path, request['shard_id']), "ab")
            client_socket.RCVTIMEO = helper.receive_timeout

            #except:
            # print("Unable to reconnect, terminating connection")
            #break

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
def check_old_connections(ui, progress_bar):
    print("Checking old connections")
    try:
        connections = {}
        with open(helper.upload_connection_file) as json_file:
            connections = json.load(json_file)

    except:
        print("Error in file")
    finally:
        for i in range(len(connections['connections'])):
            request = dict(connections['connections'][i])
            print("Reconnecting host", request['ip'], request["port"])
            if request['type'] == 'upload':
                send_data(request, False, ui, progress_bar)
            elif request['type'] == 'download':
                receive_data(request, progress_bar)


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
