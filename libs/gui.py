import tkinter
import tkinter.font
from tkinter import ttk
import irmaker
import pyglet
import tkinter.filedialog
import time
import os
import sys
import platform
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeView, QFileSystemModel, QLabel, QLineEdit, QPushButton, QToolButton,
    QDialog, QInputDialog, QMessageBox, QMenu, QAction, QFrame, QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont, QFontDatabase, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize, QDir, QModelIndex, QItemSelectionModel

pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file("font\\Deng.ttf")


class FolderSelector(QMainWindow):
    def __init__(self, title="选择文件夹", initial_dir=None, icon=None):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 850, 600)

        # 设置自定义图标
        if icon:
            self.setWindowIcon(icon)

        # 设置等线体字体
        self.font = self.get_system_font()

        # 设置初始目录
        self.initial_dir = initial_dir or QDir.homePath()
        self.selected_path = None

        # 创建主界面
        self.init_ui()

        # 加载初始目录
        self.navigate_to(self.initial_dir)

        # 设置样式
        self.apply_styles()

    def get_system_font(self):
        """获取系统等线体字体"""
        font = QFont()
        font_family = "Microsoft YaHei UI"  # Windows

        if platform.system() == "Darwin":  # macOS
            font_family = "PingFang SC"
        elif platform.system() == "Linux":  # Linux
            font_family = "Noto Sans CJK SC"

        if font_family in QFontDatabase().families():
            font = QFont(font_family, 10)
        else:
            # 回退到默认字体
            font = QFont()
            font.setPointSize(10)

        return font

    def init_ui(self):
        """初始化用户界面"""
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)

        # 左侧面板（快捷方式）
        left_panel = QWidget()
        left_panel.setMinimumWidth(180)
        left_panel.setMaximumWidth(220)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.setSpacing(10)

        # 计算机驱动器部分
        computer_group = QFrame()
        computer_group.setFrameShape(QFrame.StyledPanel)
        computer_layout = QVBoxLayout(computer_group)
        computer_layout.setContentsMargins(5, 15, 5, 5)
        computer_layout.setSpacing(5)

        computer_label = QLabel("计算机")
        computer_label.setFont(self.font)
        computer_layout.addWidget(computer_label)

        # 获取驱动器列表
        self.drives = self.get_drives()

        for name, path in self.drives:
            btn = QPushButton(name)
            btn.setFont(self.font)
            btn.setIcon(QIcon.fromTheme("drive-harddisk"))
            btn.setIconSize(QSize(16, 16))
            btn.setStyleSheet("text-align: left; padding: 5px;")
            btn.clicked.connect(lambda checked, p=path: self.navigate_to(p))
            computer_layout.addWidget(btn)

        left_layout.addWidget(computer_group)

        # 快捷路径部分
        quick_group = QFrame()
        quick_group.setFrameShape(QFrame.StyledPanel)
        quick_layout = QVBoxLayout(quick_group)
        quick_layout.setContentsMargins(5, 15, 5, 5)
        quick_layout.setSpacing(5)

        quick_label = QLabel("快捷方式")
        quick_label.setFont(self.font)
        quick_layout.addWidget(quick_label)

        # 添加快捷路径
        self.quick_paths = [
            ("桌面", os.path.join(QDir.homePath(), "Desktop")),
            ("文档", os.path.join(QDir.homePath(), "Documents")),
            ("下载", os.path.join(QDir.homePath(), "Downloads")),
            ("图片", os.path.join(QDir.homePath(), "Pictures")),
            ("音乐", os.path.join(QDir.homePath(), "Music")),
            ("视频", os.path.join(QDir.homePath(), "Videos")),
            ("主目录", QDir.homePath())
        ]

        for name, path in self.quick_paths:
            if os.path.exists(path):
                btn = QPushButton(name)
                btn.setFont(self.font)
                btn.setIcon(QIcon.fromTheme("folder"))
                btn.setIconSize(QSize(16, 16))
                btn.setStyleSheet("text-align: left; padding: 5px;")
                btn.clicked.connect(lambda checked, p=path: self.navigate_to(p))
                quick_layout.addWidget(btn)

        left_layout.addWidget(quick_group)
        left_layout.addStretch()

        # 右侧面板
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        # 路径栏
        path_frame = QWidget()
        path_layout = QHBoxLayout(path_frame)
        path_layout.setContentsMargins(0, 0, 0, 0)

        path_label = QLabel("路径:")
        path_label.setFont(self.font)
        path_layout.addWidget(path_label)

        self.path_edit = QLineEdit()
        self.path_edit.setFont(self.font)
        self.path_edit.returnPressed.connect(self.navigate_to_current)
        path_layout.addWidget(self.path_edit)

        go_button = QPushButton("转到")
        go_button.setFont(self.font)
        go_button.clicked.connect(self.navigate_to_current)
        path_layout.addWidget(go_button)

        right_layout.addWidget(path_frame)

        # 按钮栏
        button_frame = QWidget()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)

        up_button = QPushButton("上一级")
        up_button.setFont(self.font)
        up_button.clicked.connect(self.go_up)
        button_layout.addWidget(up_button)

        refresh_button = QPushButton("刷新")
        refresh_button.setFont(self.font)
        refresh_button.clicked.connect(self.refresh)
        button_layout.addWidget(refresh_button)

        new_folder_button = QPushButton("新建文件夹")
        new_folder_button.setFont(self.font)
        new_folder_button.clicked.connect(self.create_folder)
        button_layout.addWidget(new_folder_button)

        button_layout.addStretch()

        self.select_button = QPushButton("选择")
        self.select_button.setFont(self.font)
        self.select_button.clicked.connect(self.confirm_selection)
        button_layout.addWidget(self.select_button)

        right_layout.addWidget(button_frame)

        # 文件树视图
        self.tree_view = QTreeView()
        self.tree_view.setFont(self.font)
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_view.doubleClicked.connect(self.on_double_click)

        # 文件系统模型
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        self.tree_view.setModel(self.model)

        # 隐藏不需要的列
        self.tree_view.setHeaderHidden(True)
        self.tree_view.hideColumn(1)  # 大小
        self.tree_view.hideColumn(2)  # 类型
        self.tree_view.hideColumn(3)  # 修改日期

        right_layout.addWidget(self.tree_view)

        # 添加到分割器
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([200, 600])

        main_layout.addWidget(splitter)

    def get_drives(self):
        """获取系统所有磁盘驱动器"""
        drives = []
        system = platform.system()

        if system == "Windows":
            # Windows系统：获取所有逻辑驱动器
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    drives.append((f"本地磁盘 ({letter}:)", drive))

            # 添加网络驱动器
            network_path = os.path.join(os.path.expanduser("~"), "Network")
            if os.path.exists(network_path):
                drives.append(("网络驱动器", network_path))
        else:
            # Unix/Linux/Mac系统
            drives.append(("根目录", "/"))

            # 添加挂载点
            for mount_point in ["/mnt", "/media", "/Volumes"]:
                if os.path.exists(mount_point):
                    for item in os.listdir(mount_point):
                        full_path = os.path.join(mount_point, item)
                        if os.path.isdir(full_path):
                            drives.append((f"挂载点 ({item})", full_path))

        return drives

    def navigate_to(self, path):
        """导航到指定路径"""
        if os.path.isdir(path):
            self.path_edit.setText(path)
            index = self.model.index(path)

            # 展开父目录
            parent_index = index.parent()
            self.tree_view.expand(parent_index)

            # 选中当前目录
            self.tree_view.scrollTo(index)
            self.tree_view.setCurrentIndex(index)
            self.tree_view.selectionModel().select(index, QItemSelectionModel.ClearAndSelect)
        else:
            QMessageBox.warning(self, "路径无效", f"路径 '{path}' 不存在或不是目录")

    def navigate_to_current(self):
        """导航到当前输入框中的路径"""
        path = self.path_edit.text()
        if os.path.isdir(path):
            self.navigate_to(path)
        else:
            # 尝试创建目录
            reply = QMessageBox.question(
                self, "目录不存在",
                f"目录 '{path}' 不存在。是否要创建它？",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                try:
                    os.makedirs(path, exist_ok=True)
                    self.navigate_to(path)
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"无法创建目录: {str(e)}")

    def go_up(self):
        """返回上一级目录"""
        current_path = self.path_edit.text()
        parent_path = os.path.dirname(current_path)
        if os.path.isdir(parent_path):
            self.navigate_to(parent_path)

    def refresh(self):
        """刷新当前目录"""
        current_path = self.path_edit.text()
        if os.path.isdir(current_path):
            # 重新加载模型
            self.model.refresh()
            self.navigate_to(current_path)

    def create_folder(self):
        """创建新文件夹"""
        current_path = self.path_edit.text()
        if not os.path.isdir(current_path):
            QMessageBox.warning(self, "路径无效", "当前路径无效，无法创建文件夹")
            return

        folder_name, ok = QInputDialog.getText(
            self, "新建文件夹", "请输入文件夹名称:", text="新建文件夹"
        )

        if ok and folder_name:
            new_path = os.path.join(current_path, folder_name)
            try:
                os.makedirs(new_path, exist_ok=False)
                self.refresh()
            except FileExistsError:
                QMessageBox.critical(self, "错误", f"文件夹 '{folder_name}' 已存在")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法创建文件夹: {str(e)}")

    def show_context_menu(self, position):
        """显示右键菜单"""
        index = self.tree_view.indexAt(position)
        if index.isValid():
            path = self.model.filePath(index)
            self.path_edit.setText(path)

        # 创建菜单
        menu = QMenu(self)
        menu.setFont(self.font)

        new_folder_action = QAction("新建文件夹", self)
        new_folder_action.triggered.connect(self.create_folder)
        menu.addAction(new_folder_action)

        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self.refresh)
        menu.addAction(refresh_action)

        # 显示菜单
        menu.exec_(self.tree_view.viewport().mapToGlobal(position))

    def on_double_click(self, index):
        """处理双击事件"""
        if index.isValid():
            path = self.model.filePath(index)
            self.path_edit.setText(path)

    def confirm_selection(self):
        """确认选择"""
        self.selected_path = self.path_edit.text()
        self.close()

    def apply_styles(self):
        """应用样式表"""
        # 设置统一的字体
        self.setFont(self.font)

        # 设置树视图的展开/折叠图标为尖括号
        self.tree_view.setStyleSheet("""
            QTreeView::branch:closed:has-children {
                image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M5 4 L11 8 L5 12 Z" fill="gray"/></svg>');
            }

            QTreeView::branch:open:has-children {
                image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M4 5 L12 5 L8 11 Z" fill="gray"/></svg>');
            }

            QTreeView::branch:has-siblings:!adjoins-item {
                border-image: none;
                image: none;
            }

            QTreeView::branch:has-siblings:adjoins-item {
                border-image: none;
                image: none;
            }

            QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                border-image: none;
                image: none;
            }
        """)

        # 设置按钮样式
        button_style = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 80px;
            }

            QPushButton:hover {
                background-color: #e6e6e6;
            }

            QPushButton:pressed {
                background-color: #d6d6d6;
            }
        """

        # 应用按钮样式
        for widget in self.findChildren(QPushButton):
            widget.setStyleSheet(button_style)

    def get_selected_path(self):
        """获取选择的路径"""
        return self.selected_path


def select_folder(title="选择文件夹", initial_dir=None, icon=None):
    """显示文件夹选择对话框并返回选择的路径

    参数:
        title (str): 窗口标题
        initial_dir (str): 初始目录
        icon (str|QIcon): 窗口图标路径或QIcon对象
    """
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # 处理图标参数
    if icon and isinstance(icon, str):
        # 如果是字符串，转换为QIcon
        icon = QIcon(icon)

    selector = FolderSelector(title, initial_dir, icon)
    selector.show()
    app.exec_()

    return selector.get_selected_path()


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
        self.button__create_project.bind("<ButtonRelease-1>", func=gui__create_project().run)
        self.button__open_project.bind("<ButtonRelease-1>",func=self.open_projectfile)
        self.screen.mainloop()

    @staticmethod
    def open_projectfile(event):
        path_projectfile = tkinter.filedialog.askopenfilename(title="打开工作区文件", filetypes=[("project file", "*.imz"), ("All files", "*.*")])
        time.sleep(0.2)
        path_project= select_folder(title="选择工作区保存目录",icon="image\\logo.ico")
        print(path_projectfile)
        print(path_project)


class gui__create_project:
    def __init__(self):
        self.packname = None
        self.version = None
        self.description = None
        self.project_path = tkinter.StringVar()
        self.this = self  # 添加对自身的引用

    def run(self, event=None):
        def create(event):
            self.packname = str(self.entry__packname.get())
            self.version = self.combobox__version.get()
            self.description = self.text__description.get("1.0", tkinter.END)


        self.option = ["1.12.2", "1.16.5"]
        self.screen = tkinter.Tk()
        self.screen.title("irmaker")
        self.screen.iconbitmap("image\\logo.ico")
        self.screen.geometry("600x400")
        self.screen.resizable(False, False)
        self.font = tkinter.font.Font(family="等线", size=12)
        self.label__packname = tkinter.Label(master=self.screen, text="追加包名称", font=self.font)
        self.label__packname.place(x=20, y=20)
        self.label__version = tkinter.Label(self.screen, text="游戏版本", font=self.font)
        self.label__version.place(x=25, y=60)
        self.label__description = tkinter.Label(self.screen, text="描 述", font=self.font)
        self.label__description.place(x=40, y=100)
        self.label__project_path = tkinter.Label(self.screen, text="工作区目录", font=self.font)
        self.label__project_path.place(x=20, y=165)
        self.entry__packname = tkinter.Entry(master=self.screen, font=self.font, width=55)
        self.entry__packname.place(x=120, y=20)
        self.entry__project_path = tkinter.Entry(master=self.screen, font=self.font, width=52,
                                                 textvariable=self.project_path)
        self.entry__project_path.place(x=120, y=166)
        self.text__description = tkinter.Text(master=self.screen, width=63, height=4)
        self.text__description.place(x=120, y=100)
        self.button__create = ttk.Button(master=self.screen, text="创建")
        self.button__create.place(x=480, y=330)
        self.button__create.bind("<ButtonRelease-1>", create)
        self.button__project_path = ttk.Button(master=self.screen, text="...", width=3)
        self.button__project_path.place(x=542, y=162)

        # 关键修改：绑定到当前实例的方法
        self.button__project_path.bind("<ButtonRelease-1>", self.open__project_path)

        self.combobox__version = ttk.Combobox(master=self.screen, values=self.option, width=61)
        self.combobox__version.set(self.option[0])
        self.combobox__version.place(x=120, y=60)
        self.screen.mainloop()

    def open__project_path(self, event):
        selected_path = select_folder(title="选择项目保存文件夹", icon="image\\logo.ico")
        if selected_path:
            # 更新StringVar和输入框
            self.project_path.set(selected_path)
            self.entry__project_path.delete(0, tkinter.END)
            self.entry__project_path.insert(0, selected_path)


if __name__ == "__main__":
    run = gui__welcome()
    run.run()