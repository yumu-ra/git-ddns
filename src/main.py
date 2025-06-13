import github
from apscheduler.schedulers.blocking import BlockingScheduler
from config import config_reader
import json
import subprocess

# 定义令牌
TOKEN = config_reader.config_params['token']
REPO_NAME = config_reader.config_params['repo']  # your_username/your_repo_name
FILE_NAME = "/data/ddns.json"  # 这是默认储存ip address的文件路径 en: This is the default file path to store the ip address
# 用于存储ip地址的变量，以便于比较是否发生变化
IP_ADDRESS = None
# 修正 STUTAS 初始化
STUTAS = True  # 用于存储状态的变量，以便于比较是否发生变化

scheduler = BlockingScheduler()

class GithubCilent:
    def __init__(self):
        """
            初始化 Github 仓库，获取 Github 对象、仓库对象和文件对象。
            如果文件不存在，则创建一个新文件。
            """
        # 使用 API 创建一个对象，传入访问令牌
        global TOKEN,REPO_NAME,FILE_NAME
        g = github.Github(login_or_token=TOKEN)
        # 获取指定名称的仓库对象
        repo = g.get_repo(REPO_NAME)
        # 使用 try-except 语句块来处理可能出现的异常情况
        try:
            # 尝试获取仓库中指定名称的文件对象
            file = repo.get_contents(FILE_NAME)
        except github.UnknownObjectException:
            # 如果文件不存在，则创建一个新文件，并设置初始提交信息和内容
            repo.create_file(FILE_NAME, "Initial commit", "{}")
            # 获取新创建的文件对象
            file = repo.get_contents(FILE_NAME)
        self.g=g
        self.repo=repo
        self.file=file
        # 返回 Github 对象、仓库对象和文件对象
        # return g, repo, file

    def updateIP(self,data):
        """
        更新仓库中的文件内容，将新的 IP 地址信息写入文件。
        """
        try:
            self.repo.update_file(self.file.path, message="Update my ip",content=data,sha=self.file.sha)
        except github.GithubException as e:
            print(f"更新失败: {e}")

def getBuildIP()->str:
    """
    执行外部脚本获取 IPv6 地址，检查地址是否变化，构建包含 IP 地址的 JSON 数据。

    Returns:
        str: 包含 IP 地址的 JSON 字符串，若地址无变化则返回 None。
    """
    global STUTAS
    try:
        result = subprocess.check_output("./Scripts/get_ipv6.sh", shell=True).decode("utf-8").strip()#得到ip
        global IP_ADDRESS
        if IP_ADDRESS != result:
            data = {
                "IP_ADDRESS": result,
            }
            STUTAS = True
            return json.dumps(data)

        else:
            STUTAS=False
    except subprocess.CalledProcessError:
        print(subprocess.CalledProcessError)

def update():
    git = GithubCilent()
    date=getBuildIP()
    git.updateIP(date=date)
def main():
    """
    主函数，启动定时任务。
    """
    # 每隔 n 分钟执行一次函数，修正配置参数使用
    scheduler.add_job(update(), 'interval', minutes=config_reader.config_params['update_interval'])
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()

main()