import time
import tkinter
import tkinterdnd2
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk
import configparser
import json
import logging
import datetime



theme = {"1":["#4A6572","#E1E8ED"],
         "2":["#5B7876","#EDF3F2"],
         "3":["#A1887F","#F5EFEB"],
         "4":["#6D5D6E","#F0EEF2"],
         "5":["#616161","#F5F5F5"],
         "6":["#2C3E50","#EAEDF1"],
         "7":["#BF6C3B","#FDF2E9"],
         "8":["#424242","#FAFAFA"],
         "9":["#A76B90","#FBECF4"],
         "10":["#005B5B","#E5F2F2"],
         "11":["#FFC107","#FFF9E6"]
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
        def UpdateColor(self):
            logging.info("Change Theme")
            if self.theme != "custom":
                self.screen.config(bg=theme[self.theme][0])
                self.frame1.config(bg=theme[self.theme][1])
            else:
                self.screen.config(bg=config_get("User", "CustomColor_deep"))
                self.frame1.config(bg=config_get("User", "CustomColor_light"))
        def UpdateLanguage(self):
            logging .info("Change Language")

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
                                          activebackground=theme[self.theme][0], activeforeground=theme[self.theme][1],
                                          command=lambda:self.Setting())
            self.button3.place(x=120, y=20, height=100, width=100)
            if self.theme != "custom":
                self.screen.config(bg=theme[self.theme][0])
                self.frame1.config(bg=theme[self.theme][1])
            else:
                self.screen.config(bg=config_get("User","CustomColor_deep"))
                self.frame1.config(bg=config_get("User","CustomColor_light"))
        def Setting(self):
            gui.SettingGUI().run()
    class CreateWork(Common):
        def __init__(self):
            self.theme = config_get("User", "theme")
            self.screen = tkinter.Tk()
            self.screen.title("IR Maker")
            self.screen.iconbitmap(f"libs/image/logo.ico")
            self.screen.geometry("600x350+450+200")
    class SettingGUI(Common):
        def __init__(self):
            self.value_color = tkinter.Variable()
            self.value_color.set(value=config_get("User", "theme"))
            self.theme = config_get("User", "theme")
            self.screen = tkinter.Toplevel()
            self.screen.title("IR maker"+" "+Langauge().language['lang']["button"]["welcome_setting"])
            self.screen.iconbitmap(f"libs/image/logo.ico")
            self.screen.geometry("600x350+550+180")
            self.screen.resizable(False, False)
            self.frame1 = tkinter.Frame(master=self.screen, bd=165, width=450, bg="#E1E8ED")
            self.frame1.place(x=150, y=0, width=450, height=350)
            self.label1 = tkinter.Label(master=self.frame1,
                                        text=Langauge().language["lang"]["label"]["setting_theme"],
                                        bg=theme[self.theme][1])
            self.label1.place(x=-140,y=-145,height=20,width=40)
            self.radiobutton1 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_1"],
                                                    variable=self.value_color,
                                                    value="1",
                                                    bg=theme[self.theme][1])
            self.radiobutton1.place(x=-80,y=-146)
            self.radiobutton2 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_2"],
                                                    variable=self.value_color,
                                                    value="2",
                                                    bg=theme[self.theme][1])
            self.radiobutton2.place(x=0, y=-146)
            self.radiobutton3 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_3"],
                                                    variable=self.value_color,
                                                    value="3",
                                                    bg=theme[self.theme][1])
            self.radiobutton3.place(x=80, y=-146)
            self.radiobutton4 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_4"],
                                                    variable=self.value_color,
                                                    value="4",
                                                    bg=theme[self.theme][1])
            self.radiobutton4.place(x=160, y=-146)
            self.radiobutton5 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_5"],
                                                    variable=self.value_color,
                                                    value="5",
                                                    bg=theme[self.theme][1])
            self.radiobutton5.place(x=-80, y=-120)
            self.radiobutton6 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_6"],
                                                    variable=self.value_color,
                                                    value="6",
                                                    bg=theme[self.theme][1])
            self.radiobutton6.place(x=0, y=-120)
            self.radiobutton7 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_7"],
                                                    variable=self.value_color,
                                                    value="7",
                                                    bg=theme[self.theme][1])
            self.radiobutton7.place(x=80, y=-120)
            self.radiobutton8 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_8"],
                                                    variable=self.value_color,
                                                    value="8",
                                                    bg=theme[self.theme][1])
            self.radiobutton8.place(x=160, y=-130)
            if self.theme != "custom":
                self.screen.config(bg=theme[self.theme][0])
                self.frame1.config(bg=theme[self.theme][1])
            else:
                self.screen.config(bg=config_get("User", "CustomColor_deep"))
                self.frame1.config(bg=config_get("User", "CustomColor_light"))

def init():
    gui.MainGUI().run()






if __name__ == "__main__":
    init()