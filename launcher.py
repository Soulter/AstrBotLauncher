# -*- coding: utf-8 -*-
import os
import requests

if __name__ == "__main__":
    print("欢迎来到QQChannelChatGPT项目的Windows启动向导，正在进行依赖检查")
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
            print("当前版本: " + commit_hash)

            # 得到远程仓库的origin的commit的列表
            origin = repo.remotes.origin
            try:
                origin.fetch()
            except:
                pass
            # 得到远程仓库的commit的hash值
            remote_commit_hash = origin.refs.master.commit.hexsha
            print("最新版本: " + remote_commit_hash)
            # 比较两个commit的hash值
            if commit_hash != remote_commit_hash:
                res = input("检测到项目有更新, 是否更新? (y/n): ")
                if res == "y":
                    repo.remotes.origin.pull()
                    print("项目更新完毕")
                if res == "n":
                    print("已取消更新")
            else:
                print("已是最新版本")
        except:
            print("未检查到QQChannelChatGPT项目，将自动安装安装。\n--------------------------------")

            print("【步骤1】检查Python")
            mm = os.system('python -V')
            ins_p = True
            if mm == 0:
                res = input("Python环境已安装，请检查上面显示的版本版本是否为3.9及以上版本。是y 否n，输入后回车继续")
                if res == "n":
                    ins_p = True
                elif res == "y":
                    ins_p = False
                else:
                    input("输入错误，程序退出。")
                    exit(0)
            else:
                print("未检测到Python环境")
            if ins_p:
                print("正在自动下载Python3.10.2...")
                f=requests.get('https://npm.taobao.org/mirrors/python/3.10.2/python-3.10.2-amd64.exe')
                #下载文件
                with open("python-target.exe","wb") as code:
                    code.write(f.content)
                input("下载完成，自动安装Python3.10.2。安装时, 请务必勾选下面的“Add Python to PATH”选项，不然无法进行。输入回车启动安装。(如果未启动，请自己启动，就在本启动器目录下。)")
                os.system('python-target.exe')
                input("如果安装完成，按回车继续。")
                # os.system('rm python-target.exe')
                has_auto_installed = True


            print("【步骤2】检查Git")
            mm = os.system('git --version')
            ins_g = True
            if mm == 0:
                res = print("Git环境已安装.")
                ins_g = False
            else:
                print("未检测到Git环境，正在下载...")

            if ins_g:
                f=requests.get('https://npm.taobao.org/mirrors/git-for-windows/v2.39.2.windows.1/Git-2.39.2-64-bit.exe')
                #下载文件
                with open("git-target.exe","wb") as code:
                    code.write(f.content)
                input("下载完成，自动安装Git。输入回车启动安装。(如果未启动，请自己启动，就在本启动器目录下。)")
                print("【重要消息】在安装时，一路Next下去，直到'Adjusting Your PATH environment'那里，确保选的是第二个选项。")
                os.system('git-target.exe')
                input("如果安装完成，按回车继续。")
                # os.system('rm git-target.exe')
                has_auto_installed = True

            if has_auto_installed:
                print("--------------------------------")
                input("安装完毕。请右上角关掉本程序然后重启。")

            # print("如果您在中国大陆内，本项目全程挂全局代理使用会提高成功率。")
            print("正在从https://gitee.com/soulter/QQChannelChatGPT.git拉取最新项目...")
            try:
                Repo.clone_from('https://gitee.com/soulter/QQChannelChatGPT.git',to_path=project_path,branch='master')
                print("项目拉取完毕")
            except BaseException as e:
                print(e)
                mm = os.system('git --version')
                if mm == 0:
                    input("项目拉取失败。网络问题")
                else:
                    input("项目拉取失败，大概率为Git安装问题，请检查Git是否安装，并且是否设置了环境变量，按下回车键退出...")
                raise e

        # print("提示：如果要启用go-cq，可以")
        # res = input("是否要使用QQ机器人？（不是QQ频道） 输入y是，输入其他则不启动，回车继续。")
        # if res == 'y':
        #     if not os.path.exists('go-cqhttp'):
        #         print("没有go-cqhttp，你是不是删除了?如果删除了那请自行重新下载。")
        #     else:
        #         print("【小贴士】如果你是初次使用，请在go-cqhttp/config.yml下配置QQ号和密码，具体的内容请进去这个文件内看。")
        #         os.system("start cmd /K go-cqhttp\\go-cqhttp.exe ")
        #         print("go-cqhttp执行启动成功。")

        print("如果您是初次启动, 请先在QQChannelChatGPT/configs/config.yaml填写或者修改相关机器人配置! 等待5秒继续...")
        import time
        time.sleep(5)

        # if not has_auto_installed:
        # else:
        #     input("初次启动, 请先在QQChannelChatGPT/configs/config.yaml填写相关配置! 如果已经填写，回车继续。")

        print("正在启动...")
        os.system('python QQChannelChatGPT\\main.py')
    except BaseException as e:
        print(e)
        input("程序出错，可以加群322154837反馈。按下回车键退出...")