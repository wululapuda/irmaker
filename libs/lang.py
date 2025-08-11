import json
from configparser import ConfigParser
import error

config = ConfigParser()
    # 读取INI文件
config.read("config\\CONFIG.ini")
file = config["lang"]["lang"]


class lang:
    def __init__(self):#实例化类就加载
        "实例话立即读取config，并将data替换为语言文件内容"
        try:
            name = "lang" + "\\" + file + ".json"
            with open(name, "r") as lang_files:
                jsondata = lang_files.readlines()
                self.data = json.loads(jsondata)
                lang_files.close()
        except error.LangError:
            pass
        print(self.data)
    data = None#语言字典存储变量

class function(lang):
    def change(self, langkind):
        try:
            with open("lang" + "\\" + langkind + ".json", "r") as lang_files:
                jsondata = lang_files.readlines()
                self.data = json.loads(jsondata)
                lang_files.close()
        except error.LangError:
            pass


lang()