import tkinter
import tkinter.font
from tkinter import ttk

import pyglet
import tkinter.filedialog
import time

pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file("font\\Deng.ttf")





class gui__welcome:
    def run(self):
        self.x_button = 30
        self.y_button = 125
        self.interval_button = 100
        self.screen = tkinter.Tk()
        self.screen.title("irmaker")
        self.screen.geometry("500x280")
        self.screen.iconbitmap("image\\logo.ico")
        self.screen.resizable(False, False)
        self.frame1 = tkinter.Frame(master=self.screen, height=280, width=350, bd=5, relief=tkinter.RAISED)
        self.frame1.place(x=150, y=0)
        self.label__title = tkinter.Label(master=self.frame1, text="IR Maker", font=("等线", 25))
        self.label__title.place(x=105, y=25)
        self.label__description = tkinter.Label(master=self.frame1,text="一个免费的沉浸铁路追加包制作器",font=("等线",11))
        self.label__description.place(x=60,y=75)
        self.button__create_project = tkinter.Button(master=self.frame1, text="创建工作区", height=4, width=10, bd=3)
        self.button__create_project.place(x=self.x_button, y=self.y_button)
        self.button__open_project = tkinter.Button(master=self.frame1, text="打开工作区", height=4, width=10, bd=3)
        self.button__open_project.place(x=self.x_button + self.interval_button, y=self.y_button)
        self.button__setting = tkinter.Button(master=self.frame1, text="设置", height=4, width=10, bd=3)
        self.button__setting.place(x=self.x_button + 2 * self.interval_button, y=self.y_button)
        self.button__create_project.bind("<ButtonRelease-1>",func=gui__create_project().run)
        self.button__open_project.bind("<ButtonRelease-1>",func=self.open_projectfile)
        self.screen.mainloop()

    @staticmethod
    def open_projectfile(event):
        path_projectfile = tkinter.filedialog.askopenfilename(title="打开工作区文件", filetypes=[("project file", "*.imz"), ("All files", "*.*")])
        print(path_projectfile)

class gui__create_project:
    packname = None
    version = None
    description = None
    project_path = None

    def run(this,event):
        this.option = ["1.12.2","1.16.5"]
        this.screen = tkinter.Tk()
        this.screen.title("irmaker")
        this.screen.iconbitmap("image\\logo.ico")
        this.screen.geometry("600x400")
        this.screen.resizable(False, False)
        this.font = tkinter.font.Font(family="等线",size=12)
        this.label__packname = tkinter.Label(master=this.screen,text="追加包名称",font=this.font)
        this.label__packname.place(x=20,y=20)
        this.label__version = tkinter.Label(this.screen,text="游戏版本",font=this.font)
        this.label__version.place(x=25, y=60)
        this.label__description = tkinter.Label(this.screen,text="描 述",font=this.font)
        this.label__description.place(x=40,y=100)
        this.label__project_path = tkinter.Label(this.screen,text="工作区目录",font=this.font)
        this.label__project_path.place(x=20,y=165)
        this.entry__packname = tkinter.Entry(master=this.screen,font=this.font,width=55)
        this.entry__packname.place(x=120,y=20)
        this.entry__project_path = tkinter.Entry(master=this.screen,font=this.font,width=52)
        this.entry__project_path.place(x=120,y=166)
        this.text__description = tkinter.Text(master=this.screen,width=63,height=4)
        this.text__description.place(x=120,y=100)
        this.button__create = ttk.Button(master=this.screen, text="创建")
        this.button__create.place(x=480,y=330)
        this.button__project_path = ttk.Button(master=this.screen,text="...",width=3)
        this.button__project_path.place(x=542,y=162)
        #this.button__project_path.bind("<ButtonRelease-1>", this.open__project_path)
        this.combobox__version = ttk.Combobox(master=this.screen, values=this.option, width=61)
        this.combobox__version.set(this.option[0])
        this.combobox__version.place(x=120, y=60)
        this.screen.mainloop()

    def open__project_path(this,event):
        this.project_path = tkinter.filedialog.askdirectory()
        gui__create_project.project_path = this.project_path



if __name__ == "__main__":
    run = gui__welcome()
    run.run()