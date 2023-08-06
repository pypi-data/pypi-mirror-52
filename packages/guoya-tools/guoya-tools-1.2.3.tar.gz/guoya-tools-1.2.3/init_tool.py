# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/18 20:27
import os
import shutil
import stat
import subprocess
import yaml
import time
import requests

def get_yaml(yaml_path):
    with open(yaml_path,'r',encoding='utf-8') as f:
        content =yaml.load(f.read(),Loader=yaml.FullLoader)
    return content

def invoke(cmd):
    try:
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        print(o)
        return o
    except Exception as e:
        print('执行命令失败，请检查环境配置')
        print(e)
        raise

def copy_file(src_file,target_dir):
    shutil.copy(src_file,target_dir)

def copy_dir(src_dir,target_dir):
    if not os.path.exists(target_dir):
        shutil.copytree(src_dir,target_dir)

def get_root_path():
    root_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
    print(root_path)
    if root_path.find('venv') > 0:
        root_path=root_path[:root_path.find('venv')-1]
    return root_path+'/'

def mkdir(path):
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
def deldir(dir):
    if os.path.exists(dir):
        for file in os.listdir(dir):
            file = os.path.join(dir, file)
            if os.path.isdir(file):
                print("remove dir", file)
                os.chmod(file, stat.S_IWRITE|stat.S_IWOTH)
                deldir(file)
            elif os.path.isfile(file) :
                print("remove file", file)
                os.chmod(file, stat.S_IWRITE|stat.S_IWOTH)
                os.remove(file)
        shutil.rmtree(dir,True)

def copy_file(src_file,target_dir):
    shutil.copy(src_file,target_dir)


def down_big_file(srcUrl, localFile):
    print('%s\n --->>>\n  %s' % (srcUrl, localFile))
    startTime = time.time()
    with requests.get(srcUrl, stream=True) as r:
        contentLength = int(r.headers['content-length'])
        line = 'content-length: %dB/ %.2fKB/ %.2fMB'
        line = line % (contentLength, contentLength / 1024, contentLength / 1024 / 1024)
        print(line)
        print('正在下载中..............')
        downSize = 0
        with open(localFile, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
                downSize += len(chunk)
                line = '%d KB/s - %.2f MB， 共 %.2f MB'
                line = line % (
                downSize / 1024 / (time.time() - startTime), downSize / 1024 / 1024, contentLength / 1024 / 1024)
                print(line, end='\r')
                if downSize >= contentLength:
                    break
        timeCost = time.time() - startTime
        line = '共耗时: %.2f s, 平均速度: %.2f KB/s'
        line = line % (timeCost, downSize / 1024 / timeCost)
        print(line)

def init_ui_project():
    root_path = get_root_path()
    url = 'http://chromedriver.storage.googleapis.com/75.0.3770.90/chromedriver_win32.zip'
    mkdir(root_path + 'chrome_driver')
    down_big_file(url,root_path+'chrome_driver/chromedriver.exe')

    ## 先删除，再下载tools和ui工程
    tools_prj = 'c:/guoya/auto_test_init/guoya-tools'
    deldir(tools_prj)
    mkdir(tools_prj)
    cmd = 'git clone https://github.com/LudvikWoo/guoya-tools-test.git ' + tools_prj
    invoke(cmd)
    copy_dir(tools_prj+'/'+'tools',root_path+'tools')


    ui_prj = 'c:/guoya/auto_test_init/guoya-ui-test'
    deldir(ui_prj)
    mkdir(ui_prj)
    cmd = 'git clone https://github.com/LudvikWoo/guoya-ui-test.git ' + ui_prj
    invoke(cmd)

    ## 读取ui初始化配置文件
    y = get_yaml(ui_prj + '/init_ui_project.yaml')
    ## 复制文件夹
    dirs = y['dirs']
    for dir in dirs:
        copy_dir(ui_prj + '/' + dir, root_path + dir)
    ## 复制文件
    files = y['files']
    for file in files:
        copy_file(ui_prj + '/' + file, root_path)


if __name__ == '__main__':
    init_ui_project()