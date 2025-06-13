# DDNS 程序 

## 一、项目简介
本 DDNS（Dynamic Domain Name System，动态域名解析）系统程序旨在以**低成本**解决动态 IP 环境下的域名解析问题。不同于传统依赖域名服务商的方案，本程序创新性地将 **GitHub 等代码托管平台作为具备公网地址的 DNS 服务器**。通过将动态公网地址以文件更新的方式提交至代码仓库，用户只需读取 GitHub 上对应文件内容，即可获取真实服务器的 IP 地址并进行访问。目前该程序仅支持 **Linux 系统** ，适用于家庭网络、小型开发测试等对成本敏感的场景。
警告：未经测试；本项目仅用于学习交流，请勿用于非法用途。

## 二、安装与配置
### 1. 依赖环境
- **操作系统**：仅限 **Linux** 系统  
- **编程语言环境**：Python 3.8 及以上版本
- **依赖库**：
  ```bash
  pip install Pygithub # 用于 GitHub API 操作
  pip install apscheduler # 用于定时任务
  ```
### 2. 配置文件
在项目根目录下找到 `config/config.json` 文件，根据实际需求修改配置：
```json
{
    "repo": "your_username/your_repo_name",  // GitHub 仓库所有者&存放 IP 地址的仓库名称
    "token": "1145141919810", //如果你需要
    "update_interval" : 60  //# 检查并更新 IP 的时间间隔，单位：分钟
}


```


## 三、使用方法
### 1. 启动程序
在 Linux 系统终端执行：
```bash
python main.py
```
建议使用venv虚拟环境，避免依赖冲突。

### 2. 后台运行
若需在后台持续运行程序，可使用 `nohup` 命令：
```bash
nohup python main.py > /dev/null 2>&1 &
```
通过 `ps -ef | grep main.py` 命令可查看程序是否正在运行。


## 四、核心原理
1. **IP 地址更新**：程序定期检测当前设备的公网 IP，若发生变化，则将新 IP 写入指定的 GitHub 仓库文件（如 `ddns.json`），并提交更新。
2. **地址获取**：用户通过访问 GitHub 仓库内的文件（例如 `https://github.com/your_username/your_repo_name/date/ddns.json`），读取其中的 IP 地址，即可访问对应服务器。


## 五、项目结构说明
```
.
└── src\
    ├── main.py          # 主程序入口，包含核心逻辑
    ├──ddns.json         # 存放 IP 地址的文件,你的数据将存放在这里
    ├── Scripts          # 脚本目录
    │   └── get_ipv6.sh      # 获取 IP 地址的脚本  
    ├── config           # 配置文件目录
    │   └── ___init__.py   # 初始化文件
    ├──config.json # 配置文件
    └── README.md        # 项目说明文档
```


## 六、贡献与反馈
1. 欢迎通过 [GitHub Issues](你的项目 Issues 链接) 提交 BUG 反馈或功能建议。
2. 若想参与开发，可提交 Pull Request，提交前请确保代码通过 PEP8 规范检查，并添加必要注释。
3.特别感谢豆包ai对我这个初学者的帮助，让我能把这个项目完成。
4.灵感与参考：url： https://github.com/jeessy2/ddns-go 正是这个项目与github木马给我的启发，让我能把这个项目完成，并且通过命令获取IP的命令也是jessy2的，感谢开源世界的力量。

## 七、许可证
本项目采用 [MIT License](LICENSE) 开源协议，允许自由使用、修改和分发。

**作者**：[yumu-ra]  
