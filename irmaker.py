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


class config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("libs/config.ini")

    def config_get(self, key1, key2):
        return self.config.get(key1, key2)

    def config_set(self, key1, key2, value):
        self.config.set(section=key1, option=key2, value=value)
        with open("libs/config.ini", "w") as configfile:
            self.config.write(configfile)


class Langauge:
    language = {}

    def __init__(self):
        self.lang_type = config().config_get("system", "langauge")
        with open(f"libs/lang/{self.lang_type}.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.language = self.data


class gui:
    class Common:
        def run(self):
            self.screen.mainloop()

        def CutDown(self):
            self.screen.destroy()

        def UpdateColor(self):
            theme_value = config().config_get("User", "theme")

            # 获取颜色
            if theme_value != "custom":
                deep_color = theme[theme_value][0]
                light_color = theme[theme_value][1]
            else:
                deep_color = config().config_get("User", "CustomColor_deep")
                light_color = config().config_get("User", "CustomColor_light")

            # 更新主窗口背景色
            self.screen.config(bg=deep_color)

            # 获取所有主题颜色，用于检测控件是否使用了主题色
            all_theme_colors = []
            for theme_key in theme:
                all_theme_colors.extend(theme[theme_key])

            # 递归更新所有子控件的颜色
            def update_widget_color(widget, parent_bg=None):
                try:
                    # 获取控件的背景色
                    widget_bg = widget.cget("bg")

                    # 对于Frame控件，直接设置背景色为浅色（如果是主容器）或深色（如果是侧边栏）
                    if isinstance(widget, tkinter.Frame):
                        # 检查Frame是否在主窗口中
                        if widget.master == self.screen:
                            # 主容器Frame设置为浅色
                            widget.config(bg=light_color)
                        else:
                            # 检查父控件的背景色
                            if parent_bg:
                                # 如果父控件是深色，子Frame可以是浅色或深色
                                # 这里简化处理：如果父控件是深色，子Frame可能是浅色
                                # 如果父控件是浅色，子Frame可能是深色
                                # 我们可以根据父控件颜色决定
                                if parent_bg == deep_color or parent_bg in [theme[str(i)][0] for i in range(1, 12)]:
                                    # 父控件是深色，子Frame可能是浅色
                                    widget.config(bg=light_color)
                                else:
                                    # 父控件是浅色，子Frame可能是深色
                                    widget.config(bg=deep_color)
                            else:
                                # 默认设置为浅色
                                widget.config(bg=light_color)
                    else:
                        # 非Frame控件：检查是否使用了主题色，如果是则更新
                        if widget_bg in all_theme_colors:
                            if widget_bg == deep_color or widget_bg in [theme[str(i)][0] for i in range(1, 12)]:
                                widget.config(bg=deep_color)
                            else:
                                widget.config(bg=light_color)

                    # 获取控件的其他颜色属性
                    widget_fg = widget.cget("fg")
                    widget_activebg = widget.cget("activebackground") if hasattr(widget,
                                                                                 'cget') and 'activebackground' in widget.keys() else None
                    widget_activefg = widget.cget("activeforeground") if hasattr(widget,
                                                                                 'cget') and 'activeforeground' in widget.keys() else None

                    # 更新前景色
                    if widget_fg in all_theme_colors:
                        if widget_fg == deep_color or widget_fg in [theme[str(i)][0] for i in range(1, 12)]:
                            widget.config(fg=deep_color)
                        else:
                            widget.config(fg=light_color)

                    # 更新活动状态颜色
                    if widget_activebg and widget_activebg in all_theme_colors:
                        if widget_activebg == deep_color or widget_activebg in [theme[str(i)][0] for i in range(1, 12)]:
                            widget.config(activebackground=deep_color)
                        else:
                            widget.config(activebackground=light_color)

                    if widget_activefg and widget_activefg in all_theme_colors:
                        if widget_activefg == deep_color or widget_activefg in [theme[str(i)][0] for i in range(1, 12)]:
                            widget.config(activeforeground=deep_color)
                        else:
                            widget.config(activeforeground=light_color)

                except (tkinter.TclError, AttributeError):
                    # 忽略没有相关属性的控件
                    pass

                # 获取当前控件的背景色，传递给子控件
                current_bg = widget.cget("bg") if hasattr(widget, 'cget') and 'bg' in widget.keys() else None

                # 递归处理子控件
                for child in widget.winfo_children():
                    update_widget_color(child, current_bg)

            # 从主窗口开始更新
            for child in self.screen.winfo_children():
                update_widget_color(child, deep_color)

        def UpdateLanguage(self):
            logging.info("Change Language")

    class MainGUI(Common):
        def __init__(self):
            self.theme = config().config_get("User", "theme")
            self.screen = tkinter.Tk()
            self.screen.title("IR Maker")
            self.screen.iconbitmap(f"libs/image/logo.ico")
            self.screen.geometry("600x350+450+200")
            self.screen.resizable(False, False)

            # 使用当前主题颜色初始化frame1
            if self.theme != "custom":
                frame_bg = theme[self.theme][1]
            else:
                frame_bg = config().config_get("User", "CustomColor_light")

            self.frame1 = tkinter.Frame(master=self.screen, bd=165, width=450, bg=frame_bg)
            self.frame1.place(x=150, y=0, width=450, height=350)

            self.label1 = tkinter.Label(master=self.frame1,
                                        text=Langauge().language['lang']["label"]["welcome_description"],
                                        font=("deng", 15), justify="left", bg=frame_bg)
            self.label1.place(x=-145, y=-50)
            self.label2 = tkinter.Label(master=self.frame1,
                                        text="IR Maker",
                                        font=("deng", 30), justify="left", bg=frame_bg)
            self.label2.place(x=-30, y=-120)
            self.button1 = tkinter.Button(master=self.frame1,
                                          text=Langauge().language['lang']["button"]["welcome_create_project"],
                                          relief="groove", bg=frame_bg,
                                          activebackground=theme[self.theme][
                                              0] if self.theme != "custom" else config().config_get("User",
                                                                                                    "CustomColor_deep"),
                                          activeforeground=frame_bg,
                                          command=lambda: self.CreateWork())
            self.button1.place(x=-120, y=20, height=100, width=100)
            self.button2 = tkinter.Button(master=self.frame1,
                                          text=Langauge().language['lang']["button"]["welcome_open_project"],
                                          relief="groove", bg=frame_bg,
                                          activebackground=theme[self.theme][
                                              0] if self.theme != "custom" else config().config_get("User",
                                                                                                    "CustomColor_deep"),
                                          activeforeground=frame_bg)
            self.button2.place(x=0, y=20, height=100, width=100)
            self.button3 = tkinter.Button(master=self.frame1,
                                          text=Langauge().language['lang']["button"]["welcome_setting"],
                                          relief="groove", bg=frame_bg,
                                          activebackground=theme[self.theme][
                                              0] if self.theme != "custom" else config().config_get("User",
                                                                                                    "CustomColor_deep"),
                                          activeforeground=frame_bg,
                                          command=lambda: self.Setting())
            self.button3.place(x=120, y=20, height=100, width=100)

            if self.theme != "custom":
                self.screen.config(bg=theme[self.theme][0])
            else:
                self.screen.config(bg=config().config_get("User", "CustomColor_deep"))

        def Setting(self):
            gui.SettingGUI(self).run()  # 传递MainGUI实例给SettingGUI

        def CreateWork(self):
            gui.CreateWorkGUI().run()

    class CreateWorkGUI(Common):
        def __init__(self):
            self.work_type = tkinter.IntVar(value=1)
            self.work_type.set(1)
            self.theme = config().config_get("User", "theme")

            if self.theme != "custom":
                deep_color = theme[self.theme][0]
                light_color = theme[self.theme][1]
            else:
                deep_color = config().config_get("User", "CustomColor_deep")
                light_color = config().config_get("User", "CustomColor_light")

            self.screen = tkinter.Tk(screenName="creatework")
            self.screen.title("IR Maker")
            self.screen.config(bg=deep_color)
            self.screen.iconbitmap(f"libs/image/logo.ico")
            self.screen.geometry("450x500+550+200")
            self.screen.resizable(False, False)

            self.frame1 = tkinter.Frame(master=self.screen, bg=light_color)  # 左侧Frame使用浅色
            self.frame1.place(x=0, y=0, width=100, height=500)
            self.frame2 = tkinter.Frame(master=self.screen, bg=light_color)  # 右侧Frame使用浅色
            self.frame2.place(x=100, y=0, width=350, height=500)

            self.button1 = tkinter.Radiobutton(master=self.frame1,
                                               text="immersive\nRailroading",
                                               indicatoron=False,
                                               bg=light_color,
                                               foreground=deep_color,
                                               activebackground=light_color,
                                               activeforeground=deep_color,
                                               variable=self.work_type,
                                               value=1
                                               )
            self.button1.pack(anchor="nw", fill="both")
            self.button2 = tkinter.Radiobutton(master=self.frame1,
                                               text="RealTrainMod",
                                               indicatoron=False,
                                               bg=light_color,
                                               foreground=deep_color,
                                               activebackground=light_color,
                                               activeforeground=deep_color,
                                               variable=self.work_type,
                                               value=2
                                               )
            self.button2.pack(anchor="nw", fill="both")
            self.button1.bind("<Button-1>", self.update)

        def update(self, event):
            self.frame2.destroy()
            theme_value = config().config_get("User", "theme")
            if theme_value != "custom":
                light_color = theme[theme_value][1]
            else:
                light_color = config().config_get("User", "CustomColor_light")

            self.frame2 = tkinter.Frame(master=self.screen, bg=light_color)
            self.frame2.place(x=100, y=0, width=350, height=500)

            if self.work_type.get() == 1:
                self.ImmersiveRailroading()
            else:
                pass

        def ImmersiveRailroading(self):
            theme_value = config().config_get("User", "theme")
            if theme_value != "custom":
                light_color = theme[theme_value][1]
                deep_color = theme[theme_value][0]
            else:
                light_color = config().config_get("User", "CustomColor_light")
                deep_color = config().config_get("User", "CustomColor_deep")

            self.frame3 = tkinter.Frame(master=self.frame2, bg=light_color)
            self.frame3.pack(anchor="n", fill="both", side="top")
            tkinter.Label(master=self.frame3, bg=light_color).pack(anchor="n", fill="x", side="top")
            tkinter.Label(master=self.frame3, bg=light_color).pack(anchor="n", side="left", fill="none")
            self.label1 = tkinter.Label(master=self.frame3,
                                        text=Langauge().language['lang']["label"]["create_project_packname"] + ":",
                                        bg=light_color)
            self.label1.pack(anchor="w", fill="none", side="left")
            self.text1 = tkinter.Entry(master=self.frame3, width=35)
            self.text1.pack(anchor="n", fill="x", side="left")
            self.frame4 = tkinter.Frame(master=self.frame2, bg=light_color)
            self.frame4.pack(anchor="n", fill="both", side="top")
            tkinter.Label(master=self.frame4, bg=light_color).pack(anchor="n", fill="x", side="top")
            tkinter.Label(master=self.frame4, bg=light_color).pack(anchor="n", side="left", fill="none")
            self.label2 = tkinter.Label(master=self.frame4, bg=light_color,
                                        text=Langauge().language['lang']['label']["create_project_author"] + ":")
            self.label2.pack(anchor="n", fill="x", side="left")
            self.text2 = tkinter.Entry(master=self.frame4, width=35)
            self.text2.pack(anchor="n", fill="x", side="left")
            self.frame5 = tkinter.Frame(master=self.frame2, bg=light_color)
            self.frame5.pack(anchor="n", fill="both", side="top")
            tkinter.Label(master=self.frame5, bg=light_color).pack(anchor="n", fill="x", side="top")
            tkinter.Label(master=self.frame5, bg=light_color).pack(anchor="n", side="left", fill="none")
            self.label3 = tkinter.Label(master=self.frame5, bg=light_color,
                                        text=Langauge().language['lang']['label']["create_project_version"] + ":")
            self.label3.pack(anchor="n", fill="x", side="left")
            self.choose1 = ttk.Combobox(master=self.frame5, width=32, values=["1.12.2", "1.16.5"])
            self.choose1.pack(anchor="n", fill="none", side="left")
            self.frame6 = tkinter.Frame(master=self.frame2, bg=light_color)
            self.frame6.pack(anchor="n", fill="both", side="top")
            tkinter.Label(master=self.frame6, bg=light_color).pack(anchor="n", fill="x", side="top")
            tkinter.Label(master=self.frame6, bg=light_color).pack(anchor="n", side="left", fill="none")
            self.label4 = tkinter.Label(master=self.frame6, bg=light_color,
                                        text=Langauge().language['lang']['label']["create_project_version"] + ":")
            self.label4.pack(anchor="n", fill="x", side="left")
            self.text3 = tkinter.Text(master=self.frame6, height=5, width=34)
            self.text3.pack(anchor="n", fill="none", side="left")
            self.button3 = tkinter.Button(master=self.frame2,
                                          text=Langauge().language['lang']['button']["create_work_Create"],
                                          bg=light_color)
            self.button3.pack(anchor="se", fill="none", padx=25, pady=26, side="bottom")

    class SettingGUI(Common):
        def __init__(self, main_gui=None):
            self.main_gui = main_gui  # 保存MainGUI实例
            self.value_color = tkinter.Variable()
            self.value_color.set(value=config().config_get("User", "theme"))
            self.theme = config().config_get("User", "theme")

            # 获取颜色
            if self.theme != "custom":
                deep_color = theme[self.theme][0]
                light_color = theme[self.theme][1]
            else:
                deep_color = config().config_get("User", "CustomColor_deep")
                light_color = config().config_get("User", "CustomColor_light")

            self.screen = tkinter.Toplevel()
            self.screen.title("IR maker" + " " + Langauge().language['lang']["button"]["welcome_setting"])
            self.screen.iconbitmap(f"libs/image/logo.ico")
            self.screen.geometry("600x350+550+180")
            self.screen.resizable(False, False)

            self.frame1 = tkinter.Frame(master=self.screen, bd=165, width=450, bg=light_color)
            self.frame1.place(x=150, y=0, width=450, height=350)

            self.label1 = tkinter.Label(master=self.frame1,
                                        text=Langauge().language["lang"]["label"]["setting_theme"],
                                        bg=light_color)
            self.label1.place(x=-140, y=-145, height=20, width=40)

            # 创建所有主题选择按钮
            self.radiobutton1 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_1"],
                                                    variable=self.value_color,
                                                    value="1",
                                                    bg=light_color,
                                                    command=self.update_colors)
            self.radiobutton1.place(x=-80, y=-146)

            self.radiobutton2 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_2"],
                                                    variable=self.value_color,
                                                    value="2",
                                                    bg=light_color,
                                                    command=self.update_colors)
            self.radiobutton2.place(x=0, y=-146)

            self.radiobutton3 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_3"],
                                                    variable=self.value_color,
                                                    value="3",
                                                    bg=light_color,
                                                    command=self.update_colors)
            self.radiobutton3.place(x=80, y=-146)

            self.radiobutton4 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_4"],
                                                    variable=self.value_color,
                                                    value="4",
                                                    bg=light_color,
                                                    command=self.update_colors)
            self.radiobutton4.place(x=160, y=-146)

            self.radiobutton5 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_5"],
                                                    variable=self.value_color,
                                                    value="5",
                                                    bg=light_color,
                                                    command=self.update_colors)
            self.radiobutton5.place(x=-80, y=-120)

            self.radiobutton6 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_6"],
                                                    variable=self.value_color,
                                                    value="6",
                                                    bg=light_color,
                                                    command=self.update_colors)
            self.radiobutton6.place(x=0, y=-120)

            self.radiobutton7 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_7"],
                                                    variable=self.value_color,
                                                    value="7",
                                                    bg=light_color,
                                                    command=self.update_colors)
            self.radiobutton7.place(x=80, y=-120)

            self.radiobutton8 = tkinter.Radiobutton(master=self.frame1,
                                                    text=Langauge().language["lang"]["button"]["setting_theme_8"],
                                                    variable=self.value_color,
                                                    value="8",
                                                    bg=light_color,
                                                    command=self.update_colors)
            self.radiobutton8.place(x=160, y=-120)

            # 设置窗口背景色
            self.screen.config(bg=deep_color)

        def update_colors(self):
            """更新颜色主题"""
            self.new_color = self.value_color.get()
            config().config_set("User", "theme", self.new_color)

            # 更新设置窗口自身
            self.UpdateColor()

            # 如果有主窗口实例，更新主窗口颜色
            if self.main_gui:
                self.main_gui.UpdateColor()


def init():
    gui.MainGUI().run()


if __name__ == "__main__":
    init()