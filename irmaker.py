#coding:utf-8
from configparser import ConfigParser


class config_read:
    config = ConfigParser()
    # 读取INI文件
    config.read("libs\\config\\CONFIG.ini")
    def lang(self):
        return self.config["lang"]["lang_type"]

def create_project(name:str,version,description:str,path):
    number = 0
    if version == "1.12.2":
        number = 3
    if version == "1.16.5":
        number = 6
    with open(path+name+".irmaker","rb+") as f:
        f.writelines(["packname"+"  "+name,"gameversion"+"  "+version+"\n","{\n\n"])
        f.close()
    with open(path+"pack.mcmeta","w") as f:
        f.writelines(["{\n","  \"pack\":{\n","    \"pack_format\": "+str(number)+"\n","    \"description\": "+"\""+description+"\""+"\n","  }\n","}"])
        f.close()
