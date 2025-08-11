#coding:utf-8
from configparser import ConfigParser


class config_read:
    config = ConfigParser()
    # 读取INI文件
    config.read("libs\\config\\CONFIG.ini")
    def lang(self):
        return self.config["lang"]["lang_type"]