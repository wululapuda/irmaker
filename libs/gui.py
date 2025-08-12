import tkinter
import tkinter.font
from tkinter import filedialog

import pyglet
from tkinter import filedialog
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
        self.button__create_project.bind("<ButtonRelease-1>",func=gui__create_project.run)
        self.button__open_project.bind("<ButtonRelease-1>",func=self.open_projectfile)
        self.screen.mainloop()

    @staticmethod
    def open_projectfile(event):
        path_projectfile = filedialog.askopenfilename(title="打开工作区文件", filetypes=[("project file", "*.imz"), ("All files", "*.*")])
        print(path_projectfile)

class gui__create_project:
    @staticmethod
    def run(event):

        screen = tkinter.Tk()
        screen.title("irmaker")
        screen.iconbitmap("image\\logo.ico")
        screen.geometry("600x400")
        screen.resizable(False, False)
        font = tkinter.font.Font(family="等线",size=12)
        label__packname = tkinter.Label(master=screen,text="追加包名称",font=font)
        label__packname.place(x=20,y=20)
        label__version = tkinter.Label(screen,text="游戏版本",font=font)
        label__version.place(x=25, y=60)
        label__description = tkinter.Label(screen,text="描 述",font=font)
        label__description.place(x=40,y=100)
        label__logo = tkinter.Label(screen,text="追加包图标",font=font)
        label__logo.place(x=20,y=160)



if __name__ == "__main__":
    run = gui__welcome()
    run.run()