# -*- coding: utf-8 -*-
import os
import requests
import zipfile
import warnings

from SparkleLogging.utils.core import LogManager
from logging import Formatter, Logger
from requests.exceptions import ProxyError

warnings.filterwarnings("ignore")

logger: Logger = LogManager.GetLogger(
    log_name='astrbot-launcher',
    out_to_console=True,
    custom_formatter=Formatter('[%(asctime)s| %(name)s - %(levelname)s|%(filename)s:%(lineno)d]: %(message)s', datefmt="%H:%M:%S")
)

PYTHON_EMBED_NAME = "python-3.10.2-embed-amd64.zip"

if __name__ == "__main__":
    has_auto_installed = False
    try:
        # 检测文件夹
        os.makedirs('AstrBot', exist_ok=True)
        project_path = os.path.join('AstrBot')
        try:
            from git.repo import Repo
            repo = Repo(project_path)

            # 检查当前commit的hash值
            commit_hash = repo.head.object.hexsha
            logger.info("当前版本: " + str(commit_hash)[:7])

            # 得到远程仓库的origin的commit的列表
            origin = repo.remotes.origin
            try:
                origin.fetch()
            except:
                pass
            # 得到远程仓库的commit的hash值
            remote_commit_hash = origin.refs.master.commit.hexsha
            logger.info("最新版本: " + str(remote_commit_hash)[:7])
            # 比较两个commit的hash值
            if commit_hash != remote_commit_hash:
                res = input("检测到项目有更新, 是否更新? (y/n): ")
                if res == "y":
                    repo.remotes.origin.pull()
                    logger.info("项目更新完毕")
                if res == "n":
                    logger.info("已取消更新")
            else:
                logger.info("已是最新版本")
        except:
            logger.info("未检查到项目文件，将从 Gitee 上拉取最新代码文件。")

            logger.info("【步骤1】检查 Python")
            mm = os.system('python -V')
            ins_p = True
            if mm == 0:
                logger.info("Python 环境已安装。请检查版本是否 >= 3.9。")
                res = input("y: 是\nn: 否\n输入后回车继续")
                if res == "n":
                    ins_p = True
                elif res == "y":
                    ins_p = False
                else:
                    input("输入错误，程序退出。")
                    exit(0)
            else:
                logger.info("未检测到 Python 环境")
            if ins_p:
                logger.info(f"正在自动下载 python-3.10.2-embed-amd64.zip...")
                try:
                    f = requests.get(f'https://registry.npmmirror.com/-/binary/python/3.10.2/python-3.10.2-embed-amd64.zip', verify=False)
                except ProxyError:
                    logger.error("下载错误。请关掉本机上运行的代理程序然后重试。或者您可以自行将 https://registry.npmmirror.com/-/binary/python/3.10.2/python-3.10.2-embed-amd64.zip 下载后放到本启动器所在目录下。按任意键退出程序。")
                    input()
                    exit(0)
                except BaseException as e:
                    logger.error(e)
                    logger.error("下载时发生错误，原因如上。您可以自行将 https://registry.npmmirror.com/-/binary/python/3.10.2/python-3.10.2-embed-amd64.zip 下载后放到本启动器所在目录下。按任意键退出程序。")
                    input()
                    exit(0)
                # 下载文件
                with open("python-3.10.2-embed-amd64.zip","wb") as code:
                    code.write(f.content)
                logger.info("下载完成，正在解压。")
                # 解压zip
                with zipfile.ZipFile('python-3.10.2-embed-amd64.zip', 'r') as zip_ref:
                    zip_ref.extractall('python')
                logger.info("解压完成。")
                logger.info("正在进行一些必要配置(pth)")
                # 修改python310._pth
                with open('python/python310._pth', 'w') as f:
                    f.write('python310.zip\n.\n../AstrBot\nimport site\n')
                logger.info("配置完毕")
                # 删除zip
                try:
                    os.remove('python-3.10.2-embed-amd64.zip')
                    logger.info("已删除无用文件")
                except:
                    pass
                logger.info("安装 pip3, 请耐心等待。")
                os.system('python\\python.exe get-pip.py')
                logger.info("pip3 安装完毕")
                logger.info("Python 安装完毕")
                has_auto_installed = True

            logger.info("【步骤2】检查Git")
            mm = os.system('git --version')
            ins_g = True
            if mm == 0:
                res = logger.info("Git 环境已安装.")
                ins_g = False
            else:
                logger.info("未检测到 Git 环境。请前往 https://npm.taobao.org/mirrors/git-for-windows/v2.39.2.windows.1/Git-2.39.2-64-bit.exe 下载并安装 Git。")
                logger.info("【重要】在安装时，一路 Next，直到 'Adjusting Your PATH environment' 那里，确保选的是第 2 个选项。")

            logger.info("正在从 https://gitee.com/soulter/QQChannelChatGPT.git 拉取最新代码。")
            try:
                Repo.clone_from('https://gitee.com/soulter/QQChannelChatGPT.git', to_path=project_path, branch='master')
                logger.info("项目拉取完毕")
            except BaseException as e:
                logger.error(e)
                mm = os.system('git --version')
                if mm == 0:
                    input("项目拉取失败。网络问题")
                else:
                    input("项目拉取失败，大概率为 Git 安装问题，请检查 Git 是否安装，并且是否设置了环境变量，按下回车键退出...")
                raise e

        py_pth = "python"
        if os.path.exists("python") and os.path.exists("python\\python.exe"):
            py_pth = "python\\python.exe"
        sel = input("请选择网络环境：\n1. 中国大陆内\n其他. 中国大陆外\n")
        if sel == "1":
            logger.info("正在启动（网络环境：cn）...")
            os.system(f'{py_pth} AstrBot\\main.py -cn')
        else:
            logger.info("正在启动（网络环境：non-cn）...")
            os.system(f'{py_pth} AstrBot\\main.py')

    except BaseException as e:
        logger.error(e)
        logger.error("程序出错，可以加群 322154837 反馈。按下回车键退出...")
        input()