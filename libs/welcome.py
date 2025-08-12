import tkinter

import pyglet

pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file("font\\Deng.ttf")


class gui__welcome:
    x_button = 30
    y_button = 125
    interval_button = 100
    screen = tkinter.Tk()
    screen.title("irmaker")
    screen.geometry("500x280")
    screen.iconbitmap("image\\logo.ico")
    screen.resizable(False,False )
    frame1 = tkinter.Frame(master=screen,height=280,width=350,bd=5,relief=tkinter.RAISED)
    frame1.place(x=150,y=0)
    label__title = tkinter.Label(master=frame1,text="IR Maker",font=("等线",25))
    label__title.place(x=105,y=25)
    button__create_project = tkinter.Button(master=frame1,text="创建工作区",height=4,width=10,bd=3)
    button__create_project.place(x=x_button, y=y_button)
    button__open_project = tkinter.Button(master=frame1, text="打开工作区", height=4, width=10, bd=3)
    button__open_project.place(x=x_button + interval_button, y=y_button)
    button__create_project = tkinter.Button(master=frame1, text="设置", height=4, width=10, bd=3)
    button__create_project.place(x=x_button + 2*interval_button, y=y_button)
    def run(self):
        self.screen.mainloop()