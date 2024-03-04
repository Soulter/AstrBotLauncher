# -*- coding: utf-8 -*-
import os
import requests
import zipfile
import warnings
import general_utils as gu
from requests.exceptions import ProxyError
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    gu.log("=== 欢迎来到QQChannelChatGPT项目Windows启动向导，正在进行依赖检查 ===", fg=gu.FG_COLORS["blue"])
    has_auto_installed = False
    try:
        # 检测文件夹
        if not os.path.exists('QQChannelChatGPT'):
            os.mkdir('QQChannelChatGPT')
        project_path = os.path.join('QQChannelChatGPT')
        try:
            from git.repo import Repo
            repo = Repo(project_path)
            # 检查当前commit的hash值
            commit_hash = repo.head.object.hexsha
            gu.log("当前版本: " + str(commit_hash)[:7])

            # 得到远程仓库的origin的commit的列表
            origin = repo.remotes.origin
            try:
                origin.fetch()
            except:
                pass
            # 得到远程仓库的commit的hash值
            remote_commit_hash = origin.refs.master.commit.hexsha
            gu.log("最新版本: " + str(remote_commit_hash)[:7])
            # 比较两个commit的hash值
            if commit_hash != remote_commit_hash:
                res = input("检测到项目有更新, 是否更新? (y/n): ")
                if res == "y":
                    repo.remotes.origin.pull()
                    gu.log("项目更新完毕")
                if res == "n":
                    gu.log("已取消更新")
            else:
                gu.log("已是最新版本")
        except:
            gu.log("未检查到QQChannelChatGPT项目，将自动安装安装。\n--------------------------------")

            gu.log("【步骤1】检查Python", bg=gu.FG_COLORS["yellow"])
            mm = os.system('python -V')
            ins_p = True
            if mm == 0:
                res = input("Python环境已安装，请检查上面显示的版本版本是否为3.9及以上版本。\ny: 是\nn: 否\n\n输入后回车继续\n")
                if res == "n":
                    ins_p = True
                elif res == "y":
                    ins_p = False
                else:
                    input("输入错误，程序退出。")
                    exit(0)
            else:
                gu.log("未检测到Python环境")
            if ins_p:
                gu.log("正在自动下载Python3.10...")
                try:
                    f = requests.get('https://registry.npmmirror.com/-/binary/python/3.10.2/python-3.10.2-embed-amd64.zip', verify=False)
                except ProxyError:
                    input("下载错误。请关掉本机上运行的代理程序，然后按回车键继续。")
                    f = requests.get('https://registry.npmmirror.com/-/binary/python/3.10.2/python-3.10.2-embed-amd64.zip', verify=False)
                # f=requests.get('https://npm.taobao.org/mirrors/python/3.10.2/python-3.10.2-amd64.exe')
                #下载文件
                with open("python.zip","wb") as code:
                    code.write(f.content)
                gu.log("下载完成，正在解压。")
                # os.system('python-target.exe')
                # 解压zip
                with zipfile.ZipFile('python.zip', 'r') as zip_ref:
                    zip_ref.extractall('python')
                gu.log("解压完成。")
                gu.log("正在进行一些必要配置(pth)")
                # 修改python310._pth
                with open('python/python310._pth', 'w') as f:
                    f.write('python310.zip\n.\n../QQChannelChatGPT\nimport site\n')
                gu.log("配置完毕")
                # 删除zip
                try:
                    os.remove('python.zip')
                    gu.log("已删除无用文件")
                except:
                    gu.log("删除无用文件失败，请手动删除python.zip。")
                gu.log("安装pip3, 请等待。")
                os.system('python\\python.exe get-pip.py')
                gu.log("pip3安装完毕")
                gu.log("Python安装完毕")
                has_auto_installed = True

            gu.log("【步骤2】检查Git")
            mm = os.system('git --version')
            ins_g = True
            if mm == 0:
                res = gu.log("Git环境已安装.")
                ins_g = False
            else:
                gu.log("未检测到Git环境，正在下载...")

            if ins_g:
                f=requests.get('https://npm.taobao.org/mirrors/git-for-windows/v2.39.2.windows.1/Git-2.39.2-64-bit.exe',verify=False)
                #下载文件
                with open("git-target.exe","wb") as code:
                    code.write(f.content)
                input("下载完成，自动安装Git。输入回车启动安装。(如果未启动，请自己启动，就在本启动器目录下。)")
                gu.log("【重要消息】在安装时，一路Next下去，直到'Adjusting Your PATH environment'那里，确保选的是第二个选项。")
                os.system('git-target.exe')
                input("如果安装完成，按回车继续。")
                # os.system('rm git-target.exe')
                has_auto_installed = True

            if has_auto_installed:
                gu.log("--------------------------------")

            # gu.log("如果您在中国大陆内，本项目全程挂全局代理使用会提高成功率。")
            gu.log("正在从 https://gitee.com/soulter/QQChannelChatGPT.git 拉取最新代码。")
            try:
                Repo.clone_from('https://gitee.com/soulter/QQChannelChatGPT.git',to_path=project_path,branch='master')
                gu.log("项目拉取完毕")
            except BaseException as e:
                gu.log(e)
                mm = os.system('git --version')
                if mm == 0:
                    input("项目拉取失败。网络问题")
                else:
                    input("项目拉取失败，大概率为Git安装问题，请检查Git是否安装，并且是否设置了环境变量，按下回车键退出...")
                raise e

        py_pth = "python"
        if os.path.exists("python") and os.path.exists("python\\python.exe"):
            py_pth = "python\\python.exe"
        sel = input("请选择网络环境：\n1. 中国大陆内\n其他. 中国大陆外\n")

        if sel == "1":
            gu.log("正在启动（网络环境：cn）...")
            os.system(f'{py_pth} QQChannelChatGPT\\main.py -cn')
        else:
            gu.log("正在启动（网络环境：non-cn）...")
            os.system(f'{py_pth} QQChannelChatGPT\\main.py')
        
        
    except BaseException as e:
        gu.log(e)
        input("程序出错，可以加群322154837反馈。按下回车键退出...")