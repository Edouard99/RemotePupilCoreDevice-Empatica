from cProfile import label
import socket
import _thread
import sys
import time
import os
import csv
import zmq
import msgpack
ctx = zmq.Context()
import os



subject_number="Subject_0"
level="Medium"
device_number=0
try :
    subject_number=sys.argv[1]
    level=sys.argv[2]
    device_number=sys.argv[3]
except Exception:
    None
write_permission_empatica=False
write_permission_pupil_size=False
write_permission_pupil_gaze=False
write_permission_pupil_blink=False

pupil_offset=0
dicperm={'E4_Bvp' : False,'E4_Acc' : False,'E4_Gsr' : False,'E4_Temperature' : False,'E4_Tag' : True}
file_pupil=os.path.join(os.getcwd(),subject_number,level,'pupil.csv')
file_gaze=os.path.join(os.getcwd(),subject_number,level,'gaze.csv')
file_blink=os.path.join(os.getcwd(),subject_number,level,'blink.csv')
file_empatica=os.path.join(os.getcwd(),subject_number,level,'empatica.csv')
last_line=None
device="" #Name of empatica device
print("device name : {} \n".format(device))

List_subscribe=["device_subscribe bvp ON \r\n","device_subscribe gsr ON \r\n","device_subscribe acc ON \r\n","device_subscribe tmp ON \r\n","device_subscribe tag ON \r\n"]
label2d=["id","topic","method","norm_pos_0","norm_pos_1","diameter","confidence","timestamp","ellipse_axe_0","ellipse_axe_1","ellipse_angle","ellipse_center_0","ellipse_center_1"]
label3d=["id","topic","method","norm_pos_0","norm_pos_1","diameter","confidence","timestamp","ellipse_axe_0","ellipse_axe_1","ellipse_angle","ellipse_center_0","ellipse_center_1"
        "sphere_center_0","sphere_center_1","sphere_center_2","sphere_axes_0","sphere_axes_1","sphere_radius","projected_sphere_center_0",
        "projected_sphere_center_1","projected_sphere_axes_0","projected_sphere_axes_1","projected_sphere_angle","circle_3d_center_0","circle_3d_center_1",
        "circle_3d_center_2","circle_3d_normal_0","circle_3d_normal_1","circle_3d_normal_2","circle_3d_radius","diameter_3d",
        "location",'model_confidence','theta','phi']
keys3d=[b'id', b'topic', b'method', b'norm_pos', b'diameter', b'confidence', b'timestamp',b'ellipse', b'sphere', b'projected_sphere', b'circle_3d',
         b'diameter_3d', b'location', b'model_confidence', b'theta', b'phi']
keys2d=[b'id', b'topic', b'method', b'norm_pos', b'diameter', b'confidence', b'timestamp', b'ellipse']

keysgaze=[b'timestamp',b'confidence', b'norm_pos',
        b'gaze_point_3d',b'eye_centers_3d', b'gaze_normals_3d',  
         b'topic',  ]
labelgaze=['timestamp','confidence','norm_pos_x','norm_pos_y',
            'gaze_point_3d_x','gaze_point_3d_y','gaze_point_3d_z',
            'eye_center0_3d_x','eye_center0_3d_y','eye_center0_3d_z',
            'eye_center1_3d_x','eye_center1_3d_y','eye_center1_3d_z',
            'gaze_normal0_x','gaze_normal0_y','gaze_normal0_z',
            'gaze_normal1_x','gaze_normal1_y','gaze_normal1_z',
            'topic']
label_blink=["topic","type","confidence","timestamp","record"]

def dict_to_list_pupil(dict):
    L=[]
    if '2d' in dict[b"topic"].decode("utf-8"):
        for key in keys2d:
            data= dict[key]
            if key ==b'norm_pos':
                L.append(data[0])
                L.append(data[1])
            elif key == b'ellipse':
                L.append(data[b'axes'][0])
                L.append(data[b'axes'][1])
                L.append(data[b'angle'])
                L.append(data[b'center'][0])
                L.append(data[b'center'][1])
            else:
                if isinstance(data, bytes):
                    data=data.decode("utf-8")
                L.append(data)
    if '3d' in dict[b"topic"].decode("utf-8"):
        for key in keys3d:
            data= dict[key]
            if key ==b'norm_pos':
                L.append(data[0])
                L.append(data[1])
            elif key == b'ellipse':
                L.append(data[b'axes'][0])
                L.append(data[b'axes'][1])
                L.append(data[b'angle'])
                L.append(data[b'center'][0])
                L.append(data[b'center'][1])
            elif key ==b'location':
                L.append(data[0])
                L.append(data[1])
            elif key ==b'circle_3d':
                L.append(data[b'center'][0])
                L.append(data[b'center'][1])
                L.append(data[b'center'][2])
                L.append(data[b'normal'][0])
                L.append(data[b'normal'][1])
                L.append(data[b'normal'][2])
                L.append(data[b'radius'])
            elif key ==b'sphere':
                L.append(data[b'center'][0])
                L.append(data[b'center'][1])
                L.append(data[b'center'][2])
                L.append(data[b'radius'])
            elif key ==b'projected_sphere':
                L.append(data[b'center'][0])
                L.append(data[b'center'][1])
                L.append(data[b'axes'][0])
                L.append(data[b'axes'][1])
                L.append(data[b'angle'])
            else:
                if isinstance(data, bytes):
                    data=data.decode("utf-8")
                L.append(data)
    return L

def dict_to_gaze(dict):
    L=[]
    for key in keysgaze:
        data= dict[key]
        if key ==b'eye_centers_3d' or key==b'gaze_normals_3d':
            L.append(data[b'0'][0])
            L.append(data[b'0'][1])
            L.append(data[b'0'][2])
            L.append(data[b'1'][0])
            L.append(data[b'1'][1])
            L.append(data[b'1'][2])
        elif key== b'gaze_point_3d':
            L.append(data[0])
            L.append(data[1])
            L.append(data[2])
        elif key== b'norm_pos':
            L.append(data[0])
            L.append(data[1])
        else :
            L.append(data)
    return L

def dict_to_list_blink(dict):
    L=[]
    for key in dict.keys():
        if key!=b'base_data':
            data=dict[key]
            if isinstance(data, bytes):
                data=data.decode("utf-8")
            L.append(data)
    return L

def check_full_line(line):
    if "E4_Acc" in line:
        return True
    elif "E4_Bvp" in line:
        return True
    elif "E4_Gsr" in line:
        return True
    elif "E4_Temperature" in line:
        return True
    elif "E4_Tag" in line:
        return True
    else :
        return False

def write_firstpkg_first_line(line,f):
    f.write(line)
    f.write("\n")

def write_casual_line(line,f):
    f.write(line)
    f.write("\n")

def write_complete_first_line(line,liste,f):
    f.write("\n")
    f.write(line)
    if len(liste)!=1:
        f.write("\n")


    

def recv_empatica_data(record_time,*args):
    global write_permission_empatica
    global dicperm
    global last_line
    notif=True
    "Receive data from other clients connected to server"
    first_pkg=True
    with open(file_empatica, 'w') as f:
        while True:
            try:
                recv_data = client_socket.recv(4096)  
                recv_data_dec=recv_data.decode('ascii',errors='ignore')          
            except Exception:
                #Handle the case when server process terminates
                print("Server closed connection, thread exiting.")
                _thread.interrupt_main()
                break
            if not recv_data:
                    # Recv with no data, server closed connection
                    print("Server closed connection, thread exiting.")
                    _thread.interrupt_main()
                    break
            else:
                if record==True:
                    if "E4" in recv_data_dec:
                        if notif==True:
                            print("---Receiving data from Empatica---")
                            notif=False
                        liste=recv_data_dec.splitlines()
                        first =liste[0]
                        if first_pkg==False:
                            if check_full_line(first)==True:
                                if write_permission_empatica==False:
                                    tstamp=float(first.split()[1].replace(',','.'))
                                    topic=first.split()[0]
                                    if dicperm[topic]==False:
                                        dicperm[topic]=tstamp>=record_time
                                        write_permission_empatica=dicperm["E4_Bvp"]*dicperm["E4_Acc"]*dicperm["E4_Gsr"]*dicperm["E4_Temperature"]
                                    if dicperm[topic]==True:
                                        write_complete_first_line(first,liste,f)
                                else :
                                    write_complete_first_line(first,liste,f)
                            else :
                                if write_permission_empatica==False:
                                    completed_line=last_line+first
                                    tstamp=float(completed_line.split()[1].replace(',','.'))
                                    topic=completed_line.split()[0]
                                    if dicperm[topic]==False:
                                        dicperm[topic]=tstamp>=record_time
                                        write_permission_empatica=dicperm["E4_Bvp"]*dicperm["E4_Acc"]*dicperm["E4_Gsr"]*dicperm["E4_Temperature"]
                                    if dicperm[topic]==True:
                                        write_casual_line(first,f)

                                #MISS
                        else :
                            if check_full_line(first)==False:
                                first=last_line+first
                                liste[0]=first
                            if check_full_line(first)==False:
                                liste=liste[1:]
                            first=liste[0]
                            tstamp=float(first.split()[1].replace(',','.'))
                            topic=first.split()[0]
                            if dicperm[topic]==False:
                                dicperm[topic]=tstamp>=record_time
                                write_permission_empatica=dicperm["E4_Bvp"]*dicperm["E4_Acc"]*dicperm["E4_Gsr"]*dicperm["E4_Temperature"]
                            if dicperm[topic]==True:
                                write_firstpkg_first_line(first,f)
                                first_pkg=False
                        for ligne in liste[1:-1]:
                            if write_permission_empatica==False:
                                tstamp=float(ligne.split()[1].replace(',','.'))
                                topic=ligne.split()[0]
                                if dicperm[topic]==False:
                                    dicperm[topic]=tstamp>=record_time
                                    write_permission_empatica=dicperm["E4_Bvp"]*dicperm["E4_Acc"]*dicperm["E4_Gsr"]*dicperm["E4_Temperature"]
                                if dicperm[topic]==True:
                                    write_casual_line(ligne,f)
                                    if first_pkg==True:
                                        first_pkg=False
                            else :
                                write_casual_line(ligne,f)
                        if len(liste)>=2:
                            if first_pkg==False:
                                last_line=liste[-1]
                                f.write(last_line)
                            if first_pkg==True:
                                last_line=liste[-1]
                        f.flush()
                else :
                    continue


def recv_pupil_data(time_record,*args):
    notif=True
    global write_permission_pupil_size
    with open(file_pupil, 'w', newline='') as f:   
        writer = csv.writer(f)
        writer.writerow(label3d)
        while True:
            topic, payload = subscriber.recv_multipart()
            message = msgpack.loads(payload)
            if "pupil" in topic.decode("utf-8"):
                if notif==True:
                        print("---Receiving data from Pupil---")
                        notif=False
                if write_permission_pupil_size==False:
                    if float(message[b'timestamp'])-pupil_offset>=time_record:
                        list_payload=dict_to_list_pupil(message)
                        writer.writerow(list_payload)
                        write_permission_pupil_size=True
                else :
                    list_payload=dict_to_list_pupil(message)
                    writer.writerow(list_payload)
            f.flush()

def recv_blink_data(time_record,*args):
    global write_permission_pupil_blink
    with open(file_blink, 'w', newline='') as f2:   
        writer2 = csv.writer(f2)
        writer2.writerow(label_blink)
        while True:
            topic, payload = subscriber2.recv_multipart()
            message = msgpack.loads(payload)
            if "blink" in topic.decode("utf-8"):
                if write_permission_pupil_blink==False:
                    if float(message[b'timestamp'])-pupil_offset>=time_record:
                        list_payload2=dict_to_list_blink(message)
                        writer2.writerow(list_payload2)
                        write_permission_pupil_blink=True
                else :
                    list_payload=dict_to_list_blink(message)
                    writer2.writerow(list_payload)
            f2.flush()

def recv_gaze_data(time_record,*args):
    global write_permission_pupil_gaze
    with open(file_gaze, 'w', newline='') as f3:   
        writer3 = csv.writer(f3)
        writer3.writerow(labelgaze)
        while True:
            topic, payload = subscriber3.recv_multipart()
            message = msgpack.loads(payload)
            if write_permission_pupil_gaze==False:
                if float(message[b'timestamp'])-pupil_offset>=time_record:
                    list_payload3=dict_to_gaze(message)
                    writer3.writerow(list_payload3)
                    write_permission_pupil_gaze=True
                else :
                    list_payload=dict_to_gaze(message)
                    writer3.writerow(list_payload)
            f3.flush()

def request_pupil_time(socket):
    socket.send_string("t")
    pupil_time = socket.recv()
    return float(pupil_time)


def measure_clock_offset(socket, clock_function):
    local_time_before = clock_function()
    pupil_time = request_pupil_time(socket)
    local_time_after = clock_function()

    local_time = (local_time_before + local_time_after) / 2.0
    clock_offset = pupil_time - local_time
    return clock_offset

def measure_clock_offset_stable(socket, clock_function, nsamples=10):
    assert nsamples > 0, "Requires at least one sample"
    offsets = [measure_clock_offset(socket, clock_function) for x in range(nsamples)]
    return sum(offsets) / len(offsets)  # mean offset

def get_clock_pupil(socket):
    local_clock=time.time
    number_of_measurements = 10
    stable_offset_mean = measure_clock_offset_stable(
        socket, clock_function=local_clock, nsamples=number_of_measurements
    )
    print(
        f"Mean clock offset ({number_of_measurements} measurements): "
        f"{stable_offset_mean} seconds"
    )

    # 5. Infer pupil clock time from "local" clock measurement
    local_time = local_clock()
    pupil_time_calculated_locally = local_time + stable_offset_mean
    return(stable_offset_mean)

"""EMPATICA"""

print("----------start----------",end='\n')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 28000))
record =False
login_msg=f"device_connect {device} \r\n"
client_socket.send(login_msg.encode('UTF-8'))
time.sleep(0.2)
ans = client_socket.recv(4096)  
ans_dec=ans.decode('ascii',errors='ignore')
if "R device_connect OK" not in ans_dec:
    print("Connection with Empatica failed")
else :
    print("Connected to Empatica")
    for msg in List_subscribe:
        client_socket.send(msg.encode('UTF-8'))
        time.sleep(0.1)
        ans = client_socket.recv(4096)  


    print("Empatica Ready for record ...\n")

    """PUPIL"""
    pupil_remote = ctx.socket(zmq.REQ)
    ip_pupil = 'localhost'  # If you talk to a different machine use its IP.
    port_pupil = 50020  # The port defaults to 50020. Set in Pupil Capture GUI.
    pupil_remote.connect(f'tcp://{ip_pupil}:{port_pupil}')
    
    # Request 'SUB_PORT' for reading data
    pupil_remote.send_string('SUB_PORT')
    sub_port = pupil_remote.recv_string()
    # Request 'PUB_PORT' for writing data
    pupil_remote.send_string('PUB_PORT')
    pub_port = pupil_remote.recv_string()
    pupil_offset=get_clock_pupil(pupil_remote) #offset for synchronization

    #subscription :
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect(f'tcp://{ip_pupil}:{sub_port}')
    subscriber.subscribe('pupil.')
    subscriber2 = ctx.socket(zmq.SUB)
    subscriber2.connect(f'tcp://{ip_pupil}:{sub_port}')
    subscriber2.subscribe('blink')
    subscriber3 = ctx.socket(zmq.SUB)
    subscriber3.connect(f'tcp://{ip_pupil}:{sub_port}')
    subscriber3.subscribe('gaze.3d.01.')
    time.sleep(0.2)


    print("Pupil ready for record...\n")
    print("To start a recording type : record ")
    while True:
        user_entry = str(input())
        if user_entry=="record":
            record=True
            record_time=time.time()
            break
    _thread.start_new_thread(recv_gaze_data,(record_time,1))
    _thread.start_new_thread(recv_empatica_data,(record_time,1))
    _thread.start_new_thread(recv_pupil_data,(record_time,1))
    _thread.start_new_thread(recv_blink_data,(record_time,1))
    print(record_time)
    print(record_time+pupil_offset)
    print("recording in progress ... type : end_rec to end")
    try:
        while 1:
            user_entry=str(input())
            if user_entry=="end_rec":
                print("end of recording")
                print ("Client program quits...")
                client_socket.close()
                break
    except:
            print ("Client program quits...")
            client_socket.close()