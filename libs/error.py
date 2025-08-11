class LangError(Exception):
    def __init__(self, message, error_code):
        self.massage = message
        self.error_code = error_code
    def __str__(self):
        return f"LangError + {self.massage}"
        return f"语言文件出现错误,错误代码 + {self.error_code}"