import tkinter
import tkinter.font
import pyglet

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
        self.screen.mainloop()

class gui__create_project:
    def run(self):
        self.screen = tkinter.Tk()
        self.screen.title("irmaker")
        self.screen.iconbitmap("image\\logo.ico")
        self.screen.geometry("600x400")
        self.screen.resizable(False, False)
        self.font = tkinter.font.Font(family="等线",size=12)
        self.label__packname = tkinter.Label(master=self.screen,text="追加包名称",font=self.font)
        self.label__packname.place(x=20,y=20)
        self.label__version = tkinter.Label(self.screen,text="游戏版本",font=self.font)
        self.label__version.place(x=25, y=60)
        self.label__description = tkinter.Label(self.screen,text="描 述",font=self.font)
        self.label__description.place(x=40,y=100)
        self.label__logo = tkinter.Label(self.screen,text="追加包图标",font=self.font)
        self.label__logo.place(x=20,y=160)
        self.screen.mainloop()


if __name__ == "__main__":
    run = gui__create_project()
    run.run()