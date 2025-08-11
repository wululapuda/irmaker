import tkinter
import lang
class welcome:
    data = lang.lang()
    screen = tkinter.Tk()
    screen.title= data.data[""]
    def __init__(self):
        self.screen.mainloop()
