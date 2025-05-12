print("开始获取配置文件")
import json
files = "config.json"
class ConfigReader:
    def __init__(self):
        self.config_params = {}
        self._read_config()

    def _read_config(self):
        """"读取配置"""
        #global files
        with open(files) as json_file:
            configs = json.load(json_file)
        self.config_params["repo"] = configs["repo"]
        self.config_params["token"] = configs["token"]
        self.config_params["update_interval"] = configs["update_interval"]



# 创建类的实例
config_reader = ConfigReader()
