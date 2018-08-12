#!/usr/bin/python
# -*- coding: UTF-8 -*- 

'''
备份服务器应用(Python2.7)
'''

import commands
import re
import os

def export_docker(path):
    '''
    导出docker容器
    '''
    docker_path = path + '/backup/docker'
    re_obj = re.compile('\\s{2,}')
    containers = commands.getoutput('docker ps -a')
    name_list = []
    # 获取每行
    lines = containers.split('\n')
    index = 0
    # 获取容器名称
    for line in lines:
        if (index == 0):
            index += 1
            continue
        # 将连个以上的空格替换为 ，
        line_rep, n = re.subn(re_obj, '?!', line)
        vals = line_rep.split('?!')
        name_list.append(vals[-1])
    # 导出docker容器
    if (not os.path.exists(docker_path)):
        print('目录 %s 不存在， 正在创建该目录...' % docker_path)
        os.makedirs(docker_path)
    for name in name_list:
        print('正在导出...')
        os.system('cd %s && docker export -o %s.tar %s' % (docker_path, name, name))
    print('导出完成')
    
    pack_backup(path)
        
def pack_backup(path):
    '''
    打包备份文件
    '''
    print('正在打包...')
    os.system('cd %s && tar -czf backup.tar backup/' % path)
    print('打包完成...')

def install_backup(path, file_name, target='.'):
    '''
    安装备份文件
    '''
    # 解压文件
    print('正在解压备份文件...')
    os.system('cd %s && tar -zxf %s' % (path, file_name))
    print('解压文件完成...')

    install_docker_images(path)

def install_docker_images(path):
    '''
    导入备份文件中的docker文件
    '''
    path += '/backup/docker'
    files = commands.getoutput('cd %s && ls' % path)
    files = files.split('\n')
    print(files)
    print('开始导入Docker...')
    for file in files:
        name = file[:-4]
        os.system('cd %s && docker import %s test/%s' % (path, file, name))
    print('导入完成')

def main():
    type = raw_input('请输入需执行的操作（[backup: 备份],[install: 安装]）：')
    type = type.strip()
    if (type == 'backup'):
        path = raw_input('请输入备份后文件的存放路径: ')
        path = path.strip()
        export_docker(path)
    if (type == 'install'):
        path = raw_input('请输入备份文件存放的父目录：')
        path = path.strip()
        file_name = 'backup.tar'
        install_backup(path, file_name)

if __name__ == '__main__':
    main()