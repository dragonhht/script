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
    if (not os.path.exists(path)):
        print('目录 %s 不存在， 正在创建该目录...' % path)
        os.makedirs(path)
    for name in name_list:
        print('正在导出...')
        os.system('cd %s && docker export -o %s.tar %s' % (path, name, name))
    print('导出完成')
        
def pack_backup(path):
    '''
    打包备份文件
    '''
    print('正在打包...')
    os.system('cd %s && tar -czf backup.tar backup/' % path)
    print('打包完成...')

def main():
    path = '/home/huang/study-test/test/'
    export_docker('%sbackup/docker' % path)
    pack_backup(path)

if __name__ == '__main__':
    main()