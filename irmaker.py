import time
import tkinter
import tkinterdnd2
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk as ttk
import configparser
import json
import logging
import datetime


theme = {"1": ["#4A6572", "#E1E8ED"],
         "2": ["#5B7876", "#EDF3F2"],
         "3": ["#A1887F", "#F5EFEB"],
         "4": ["#6D5D6E", "#F0EEF2"],
         "5": ["#616161", "#F5F5F5"],
         "6": ["#2C3E50", "#EAEDF1"],
         "7": ["#BF6C3B", "#FDF2E9"],
         "8": ["#424242", "#FAFAFA"],
         "9": ["#A76B90", "#FBECF4"],
         "10": ["#005B5B", "#E5F2F2"],
         "11": ["#FFC107", "#FFF9E6"]
         }



def config_get(key1, key2):
    config = configparser.ConfigParser()
    config.read("libs/config.ini")
    return config.get(key1, key2)
def confgi_set(key1,key2,value):
    config = configparser.ConfigParser()
    config.read("libs/config.ini")
    config.set(key1,key2,value)
    with open("libs/config.ini","w") as f:
        config.write(f)

class DateWrite:
    def __init__(self,date:dict,file:str):
        with open(file,"w",encoding="utf-8") as f:
            json.dumps(date,f,ensure_ascii=False, indent=3)


class Langauge:
    language = {}

    def __init__(self):
        self.lang_type = config_get("system", "langauge")
        with open(f"libs/lang/{self.lang_type}.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.language = self.data


class gui:
    Showing_gui = []
    def Update(self,*args):
        for i in self.Showing_gui:
            i.updateGUI()
    class Common:
        def run(self):
            self.screen.mainloop()

        def CutDown(self):
            self.screen.destroy()
        def register(self):
            gui.Showing_gui.append(self)
            print(gui.Showing_gui)
        def unregister(self):
            self.Code = gui.Showing_gui.index(self)
            gui.Showing_gui[self.Code].screen.destroy()
            del gui.Showing_gui[self.Code]
            print(gui.Showing_gui)
        def updateGUI(self):
            for i in self.screen.winfo_children():
                i.destroy()
                print(gui.Showing_gui)
            self.pack()


    class MainGUI(Common):
        def __init__(self):
            self.register()
            self.screen = tkinter.Tk()
            self.screen.title("IR Maker")
            self.screen.iconbitmap(f"libs/image/logo.ico")
            self.screen.geometry("600x350+450+200")
            self.screen.resizable(False, False)
            self.screen.protocol("WM_DELETE_WINDOW",self.unregister)
            self.pack()

        def pack(self):
            self.theme = config_get("User", "theme")
            self.frame1 = tkinter.Frame(master=self.screen, bd=165, width=450, bg="#E1E8ED")
            self.frame1.place(x=150, y=0, width=450, height=350)
            self.label1 = tkinter.Label(master=self.frame1,
                                        text=Langauge().language['lang']["label"]["welcome_description"],
                                        font=("deng", 15), justify="left", bg=theme[self.theme][1])
            self.label1.place(x=-145, y=-50)
            self.label2 = tkinter.Label(master=self.frame1,
                                        text="IR Maker",
                                        font=("deng", 30), justify="left", bg=theme[self.theme][1])
            self.label2.place(x=-30, y=-120)
            self.button1 = tkinter.Button(master=self.frame1,
                                          text=Langauge().language['lang']["button"]["welcome_create_project"],
                                          relief="groove", bg=theme[self.theme][1],
                                          activebackground=theme[self.theme][0],
                                          activeforeground=theme[self.theme][1],
                                          command=lambda: self.CreateWork())
            self.button1.place(x=-120, y=20, height=100, width=100)
            self.button2 = tkinter.Button(master=self.frame1,
                                          text=Langauge().language['lang']["button"]["welcome_open_project"],
                                          relief="groove", bg=theme[self.theme][1],
                                          activebackground=theme[self.theme][0], activeforeground=theme[self.theme][1])
            self.button2.place(x=0, y=20, height=100, width=100)
            self.button3 = tkinter.Button(master=self.frame1,
                                          text=Langauge().language['lang']["button"]["welcome_setting"],
                                          relief="groove", bg=theme[self.theme][1],
                                          activebackground=theme[self.theme][0], activeforeground=theme[self.theme][1],
                                          command=lambda: self.Setting())
            self.button3.place(x=120, y=20, height=100, width=100)
            if self.theme != "custom":
                self.screen.config(bg=theme[self.theme][0])
                self.frame1.config(bg=theme[self.theme][1])
            else:
                self.screen.config(bg=config_get("User", "CustomColor_deep"))
                self.frame1.config(bg=config_get("User", "CustomColor_light"))

        def Setting(self):
            gui.SettingGUI().run()

        def CreateWork(self):
            gui.CreateWorkGUI().run()

    class CreateWorkGUI(Common):
        def __init__(self):
            self.work_type = tkinter.StringVar(value="immersiveRailroading")
            self.work_type.set("immersiveRailroading")
            self.theme = config_get("User", "theme")
            self.register()
            self.screen = tkinter.Toplevel()
            self.screen.wm_attributes("-topmost")
            self.screen.title("IR Maker")
            self.screen.iconbitmap(f"libs/image/logo.ico")
            self.screen.geometry("450x500")
            self.screen.resizable(False, False)
            self.screen.protocol("WM_DELETE_WINDOW", lambda: self.unregister())
            self.pack()
        def pack(self):
            self.screen.config(bg=theme[self.theme][0])
            self.frame1 = tkinter.Frame(master=self.screen, bg=theme[self.theme][0])
            self.frame1.place(x=0, y=0, width=100, height=500)
            self.frame2 = tkinter.Frame(master=self.screen, bg=theme[self.theme][1])
            self.frame2.place(x=100, y=0, width=350, height=500)

            self.button1 = tkinter.Radiobutton(master=self.frame1,
                                               text="immersive\nRailroading",
                                               indicatoron=False,
                                               bg=theme[self.theme][1],
                                               foreground=theme[self.theme][0],
                                               activebackground=theme[self.theme][1],
                                               activeforeground=theme[self.theme][0],
                                               variable=self.work_type,
                                               value="immersiveRailroading"
                                               )
            self.button1.pack(anchor="nw", fill="both")
            self.button2 = tkinter.Radiobutton(master=self.frame1,
                                               text="RealTrainMod",
                                               indicatoron=False,
                                               bg=theme[self.theme][1],
                                               foreground=theme[self.theme][0],
                                               activebackground=theme[self.theme][1],
                                               activeforeground=theme[self.theme][0],
                                               variable=self.work_type,
                                               value="RealTrainMod",
                                               )
            self.button2.pack(anchor="nw", fill="both")
            self.work_type.trace("w", self.update)
            self.update(event=0)
        def update(self,event,*args):
            for i in self.frame2.winfo_children():
                i.destroy()
            if self.work_type.get() == "immersiveRailroading":
                self.ImmersiveRailroading()
            else:
                pass

        def ImmersiveRailroading(self):
            """self.frame[num] = tkinter.Frame(master=self.frame2, bg=theme[self.theme][1])
            self.frame[num].pack(anchor="n", fill="both", side="top")
            tkinter.Label(master=self.frame[num], bg=theme[self.theme][1]).pack(anchor="n", fill="x", side="top")
            tkinter.Label(master=self.frame[num], bg=theme[self.theme][1]).pack(anchor="n", side="left", fill="none")
            self.label[num] = tkinter.Label(master=self.frame6, bg=theme[self.theme][1],
                                        text=Langauge().language['lang']['label']["create_project_version"] + ":")
            self.label[num].pack(anchor="n", fill="x", side="left")
            something.....
            """
            def ask_file(key):
                path = tkinter.filedialog.askdirectory()
                key.delete(0,1000000)
                key.insert(0,path)
            def creatework():
                pass
            self.frame3 = tkinter.Frame(master=self.frame2, bg=theme[self.theme][1])
            self.frame3.pack(anchor="n", fill="both", side="top")
            tkinter.Label(master=self.frame3, bg=theme[self.theme][1]).pack(anchor="n", fill="x", side="top")
            tkinter.Label(master=self.frame3, bg=theme[self.theme][1]).pack(anchor="n", side="left", fill="none")
            self.label1 = tkinter.Label(master=self.frame3,
                                        text=Langauge().language['lang']["label"]["create_project_packname"] + ":",
                                        bg=theme[self.theme][1])
            self.label1.pack(anchor="w", fill="none", side="left")
            self.text1 = tkinter.Entry(master=self.frame3, width=35)
            self.text1.pack(anchor="n", fill="x", side="left")

            self.frame4 = tkinter.Frame(master=self.frame2, bg=theme[self.theme][1])
            self.frame4.pack(anchor="n", fill="both", side="top")
            tkinter.Label(master=self.frame4, bg=theme[self.theme][1]).pack(anchor="n", fill="x", side="top")
            tkinter.Label(master=self.frame4, bg=theme[self.theme][1]).pack(anchor="n", side="left", fill="none")
            self.label2 = tkinter.Label(master=self.frame4, bg=theme[self.theme][1],
                                        text=Langauge().language['lang']['label']["create_project_author"] + ":")
            self.label2.pack(anchor="n", fill="x", side="left")
            self.text2 = tkinter.Entry(master=self.frame4, width=35)
            self.text2.pack(anchor="n", fill="x", side="left")

            self.frame5 = tkinter.Frame(master=self.frame2, bg=theme[self.theme][1])
            self.frame5.pack(anchor="n", fill="both", side="top")
            tkinter.Label(master=self.frame5, bg=theme[self.theme][1]).pack(anchor="n", fill="x", side="top")
            tkinter.Label(master=self.frame5, bg=theme[self.theme][1]).pack(anchor="n", side="left", fill="none")
            self.label3 = tkinter.Label(master=self.frame5, bg=theme[self.theme][1],
                                        text=Langauge().language['lang']['label']["create_project_version"] + ":")
            self.label3.pack(anchor="n", fill="x", side="left")
            self.choose1 = ttk.Combobox(master=self.frame5, width=32, values=["1.12.2", "1.16.5"])
            self.choose1.pack(anchor="n", fill="none", side="left")

            self.frame6 = tkinter.Frame(master=self.frame2, bg=theme[self.theme][1])
            self.frame6.pack(anchor="n", fill="both", side="top")
            tkinter.Label(master=self.frame6, bg=theme[self.theme][1]).pack(anchor="n", fill="x", side="top")
            tkinter.Label(master=self.frame6, bg=theme[self.theme][1]).pack(anchor="n", side="left", fill="none")
            self.label4 = tkinter.Label(master=self.frame6, bg=theme[self.theme][1],
                                        text=Langauge().language['lang']['label']["create_project_version"] + ":")
            self.label4.pack(anchor="n", fill="x", side="left")
            self.text3 = tkinter.Text(master=self.frame6, height=5, width=34)
            self.text3.pack(anchor="n", fill="none", side="left")
            self.button3 = tkinter.Button(master=self.frame2,
                                          text=Langauge().language['lang']['button']["create_work_Create"])
            self.button3.pack(anchor="se", fill="none", padx=25, pady=26, side="bottom")

            self.frame7 = tkinter.Frame(master=self.frame2, bg=theme[self.theme][1])
            self.frame7.pack(anchor="n", fill="both", side="top")
            tkinter.Label(master=self.frame7, bg=theme[self.theme][1]).pack(anchor="n", fill="x", side="top")
            tkinter.Label(master=self.frame7, bg=theme[self.theme][1]).pack(anchor="n", side="left", fill="none")
            self.label5 = tkinter.Label(master=self.frame7, bg=theme[self.theme][1],
                                        text=Langauge().language['lang']['label']["create_project_filepath"] + ":   ")
            self.label5.pack(anchor="n", fill="x", side="left")
            self.text4 = tkinter.Entry(master=self.frame7,width=31)
            self.text4.pack(anchor="n", fill="none", side="left")
            self.button4 = ttk.Button(master=self.frame7,width=2,text="...",command=lambda:ask_file(self.text4))
            self.button4.pack(anchor="e", fill="none", side="left")

    class SettingGUI(Common):
        def __init__(self):
            self.register()
            self.value_color = tkinter.Variable()
            self.value_color.set(value=config_get("User", "theme"))
            self.theme = config_get("User", "theme")
            self.screen = tkinter.Toplevel()
            self.screen.title("IR maker" + " " + Langauge().language['lang']["button"]["welcome_setting"])
            self.screen.iconbitmap(f"libs/image/logo.ico")
            self.screen.geometry("600x350+550+180")
            self.screen.resizable(False, False)
            self.screen.protocol("WM_DELETE_WINDOW", lambda: self.unregister())
            self.pack()
        def pack(self):
            self.frame1 = tkinter.Frame(master=self.screen, bd=165, width=450, bg="#E1E8ED")
            self.frame1.place(x=150, y=0, width=450, height=350)
            self.label1 = tkinter.Label(master=self.frame1,
                                        text=Langauge().language["lang"]["label"]["setting_theme"],
                                        bg=theme[self.theme][1])
            self.label1.place(x=-140, y=-145, height=20, width=40)
            self.radiobutton1 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_1"],
                                                    variable=self.value_color,
                                                    value="1",
                                                    bg=theme[self.theme][1])
            self.radiobutton1.place(x=-80, y=-146)
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
            self.radiobutton8.place(x=160, y=-120)
            if self.theme != "custom":
                self.screen.config(bg=theme[self.theme][0])
                self.frame1.config(bg=theme[self.theme][1])
            else:
                self.screen.config(bg=config_get("User", "CustomColor_deep"))
                self.frame1.config(bg=config_get("User", "CustomColor_light"))
            self.value_color.trace("w", lambda *args:self.changecolor())
        def changecolor(self):
            confgi_set("User","theme",str(self.value_color.get()))
            gui().Update()

def init():
    gui.MainGUI().run()


if __name__ == "__main__":
    init()