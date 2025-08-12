import tkinter
import tkinter.font
import pyglet

pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file("font\\Deng.ttf")

class gui__create_project:
    def run(this):
        this.screen.mainloop()
    screen = tkinter.Tk()
    screen.title("irmaker")
    screen.iconbitmap("image\\logo.ico")
    screen.geometry("600x400")
    screen.resizable(False, False)
    font = tkinter.font.Font(family="等线",size=15)
    label__packname = tkinter.Label(master=screen,text="追加包名称",font=font)
    label__packname.place(x=20,y=30)



gui__create_project().run()