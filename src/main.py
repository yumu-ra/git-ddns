import github
from apscheduler.schedulers.blocking import BlockingScheduler
from config import config_reader
import base64
import os
#定义令牌
GITEE_TOKEN=config_reader.config_params['token']
REPO_NAME=config_reader.config_params['repo']#your_username/your_repo_name
FILE_NAME="/data/ddns.json"#这是默认储存ip address的文件路径 en: This is the default file path to store the ip address
#初始化变量
repo = None
file = None
g = None
scheduler = BlockingScheduler()

def git_init():
    # 初始化Gitee仓库
    global g,repo,file
    # 使用Gitee API创建一个Gitee对象，传入Gitee的访问令牌
    g = github.Gitee(token=GITEE_TOKEN)
    # 获取指定名称的仓库对象
    repo = g.get_repo(REPO_NAME)
    # 使用try-except语句块来处理可能出现的异常情况
    try:
        # 尝试获取仓库中指定名称的文件对象
        file = repo.get_contents(FILE_NAME)
    except github.UnknownObjectException:
        # 如果文件不存在，则创建一个新文件，并设置初始提交信息和内容
        repo.create_file(FILE_NAME, "", "")
        # 获取新创建的文件对象
        file = repo.get_contents(FILE_NAME)
    # 返回Gitee对象、仓库对象和文件对象
    #return g, repo, file

    
def build_data():
    ip =os.system("sh ./Scripts/get_ipv6.sh")
    # 用于构建更新的数据
    data = {
        "IP_ADDRESS":ip,
        }
    return base64.b64encode(str(data).encode()).decode()
def update_data():
    # 用于更新数据
    global repo,file
    data = build_data()
    try:
        repo.update_file(file.path, "Update my ip", data, file.sha)
    except:
        print("更新失败")

def main():
    # 主函数
    # 初始化Gitee仓库
    git_init()
    # 每隔n分钟执行一次函数
    scheduler.add_job(update_data, 'interval', minutes=config_reader.config_params['polling_time'])
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
main()






