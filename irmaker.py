import time
import tkinter
import tkinterdnd2
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk
import configparser
import json

from pyglet import image

theme = {"1":["#4A6572","#E1E8ED"],
         "2":["#5B7876","#EDF3F2"],
         "3":["#A1887F","#F5EFEB"],
         "4":["#6D5D6E","#F0EEF2"],
         "5":["#616161","#F5F5F5"]
         }

def config_get(key1,key2):
    config = configparser.ConfigParser()
    config.read("libs/config.ini")
    return config.get(key1,key2)

class Langauge:
    language = {}
    def __init__(self):
        self.lang_type = config_get("system","langauge")
        with open(f"libs/lang/{self.lang_type}.json","r",encoding="utf-8") as f:
            self.data = json.load(f)
        self.language = self.data



class gui:
    class Common:
        def run(self):
            self.screen.mainloop()
        def CutDown(self):
            self.screen.destroy()
    class MainGUI(Common):
        def __init__(self):
            self.theme = config_get("User","theme")
            self.screen = tkinter.Tk()
            self.screen.title("IR Maker")
            self.screen.iconbitmap(f"libs/image/logo.ico")
            self.screen.geometry("600x350+450+200")
            self.screen.resizable(False,False)
            self.frame1 = tkinter.Frame(master=self.screen,bd=165,width=450,bg="#E1E8ED")
            self.frame1.place(x=150,y=0,width=450,height=350)
            self.label1 = tkinter.Label(master=self.frame1, text=Langauge().language['lang']["label"]["welcome_description"],font=("deng",15),justify="left",bg=theme[self.theme][1])
            self.label1.place(x=-145,y=-50)
            self.label2 = tkinter.Label(master=self.frame1,
                                        text="IR Maker",
                                        font=("deng", 30), justify="left", bg=theme[self.theme][1])
            self.label2.place(x=-30, y=-120)
            self.button1 = tkinter.Button(master=self.frame1,text=Langauge().language['lang']["button"]["welcome_create_project"],relief="groove",bg=theme[self.theme][1],activebackground=theme[self.theme][0],activeforeground=theme[self.theme][1])
            self.button1.place(x=-120,y=20,height=100,width=100)
            self.button2 = tkinter.Button(master=self.frame1,
                                          text=Langauge().language['lang']["button"]["welcome_open_project"],
                                          relief="groove", bg=theme[self.theme][1],
                                          activebackground=theme[self.theme][0], activeforeground=theme[self.theme][1])
            self.button2.place(x=0, y=20, height=100, width=100)
            self.button3 = tkinter.Button(master=self.frame1,
                                          text=Langauge().language['lang']["button"]["welcome_setting"],
                                          relief="groove", bg=theme[self.theme][1],
                                          activebackground=theme[self.theme][0], activeforeground=theme[self.theme][1])
            self.button3.place(x=120, y=20, height=100, width=100)
            if self.theme != "custom":
                self.screen.config(bg=theme[self.theme][0])
                self.frame1.config(bg=theme[self.theme][1])




def init():
    gui.MainGUI().run()






if __name__ == "__main__":
    init()