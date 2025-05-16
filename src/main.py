import github
from apscheduler.schedulers.blocking import BlockingScheduler
from config import config_reader
import json
import subprocess

# 定义令牌
TOKEN = config_reader.config_params['token']
REPO_NAME = config_reader.config_params['repo']  # your_username/your_repo_name
FILE_NAME = "/data/ddns.json"  # 这是默认储存ip address的文件路径 en: This is the default file path to store the ip address

# 初始化变量
repo = None
file = None
g = None

# 用于存储ip地址的变量，以便于比较是否发生变化
IP_ADDRESS = None
# 修正 STUTAS 初始化
STUTAS = False  # 用于存储状态的变量，以便于比较是否发生变化

scheduler = BlockingScheduler()


def git_init():
    """
    初始化 Github 仓库，获取 Github 对象、仓库对象和文件对象。
    如果文件不存在，则创建一个新文件。
    """
    global g, repo, file
    # 使用 API 创建一个对象，传入访问令牌
    g = github.Github(token=TOKEN)
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
    # 返回 Github 对象、仓库对象和文件对象
    # return g, repo, file


def build_data():
    """
    执行外部脚本获取 IPv6 地址，检查地址是否变化，构建包含 IP 地址的 JSON 数据。

    Returns:
        str: 包含 IP 地址的 JSON 字符串，若地址无变化则返回 None。
    """
    global STUTAS
    try:
        result = subprocess.check_output("./Scripts/get_ipv6.sh", shell=True).decode("utf-8").strip()
        if check_ip_address(result):
            data = {
                "IP_ADDRESS": result,
            }
            STUTAS = True
            return json.dumps(data)
        else:
            STUTAS = False
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Output:", e.stderr)


def check_ip_address(ip_address):
    """
    检查新的 IP 地址是否与之前存储的不同。

    Args:
        ip_address (str): 新获取的 IP 地址。

    Returns:
        bool: 若 IP 地址有变化返回 True，否则返回 False。
    """
    global IP_ADDRESS
    if IP_ADDRESS == ip_address:
        return False
    else:
        IP_ADDRESS = ip_address
        return True


def update_data():
    """
    更新仓库中的文件内容，将新的 IP 地址信息写入文件。
    """
    global repo, file
    data = build_data()
    if data:
        try:
            repo.update_file(file.path, "Update my ip", data, file.sha)
        except github.GithubException as e:
            print(f"更新失败: {e}")


def main():
    """
    主函数，初始化仓库并启动定时任务。
    """
    # 初始化仓库
    git_init()
    # 每隔 n 分钟执行一次函数，修正配置参数使用
    scheduler.add_job(update_data, 'interval', minutes=config_reader.config_params['update_interval'])
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()


main()
