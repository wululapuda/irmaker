import json
import error
class lang:
    def __init__(self):#实例化类就加载

    data = None#语言字典存储变量
class function(lang):
    def change(self, langkind):
        try:
            with open("lang" + "\\" + langkind + ".json", "r") as lang_files:
                jsondata = lang_files.readline()
                self.data = json.load(jsondata)
                lang_files.close()
        except error.LangError:
            pass


