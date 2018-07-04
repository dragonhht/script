#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import os

# 更新笔记目录内容

# 记录需修改文件路径的文件
record_file_name = '.record'
# 需修改的目标文件的父路径
target_parent_path = ''

def createRecord():
    '''
    初始化保存笔记目录的readme文件路径
    '''
    now_path = os.path.abspath('.')
    record_file = now_path + '\\' + record_file_name
    print(os.path.exists(record_file))
    # 创建记录文件
    #if (os.path.exists(record_file)):
    str = input('Please enter the file path to be modified: ')
    # 将路径写入文件
    f = None
    try:
        f = open(record_file, 'w')
        f.write(str)
    except:
        print('路径写入错误!!!')
    finally:
        if (f):
            f.close()

def getTargetPath():
    '''
    获取目标文件路径
    '''
    f = None
    try:
        f = open(record_file_name, 'r')
        target_path = f.readline()
        return target_path
    except:
        print('记录文件不存在，请先初始化记录文件')
    finally:
        if (f):
            f.close()
        
def getParentTargetPath():
    '''
    获取目标文件的父路径
    '''
    path = getTargetPath()

def addContents():
    '''
    向文件中添加内容
    '''
    f = None
    path = getTargetPath()
    print(path)

    content = input('请输入将目录放置哪个层级下：')
    if (content == ''):
        content = 'Java'
    content = '## ' + content.strip()

    try:
        f = open(path, 'r+', encoding='utf-8')
        flag = True
        position = 0
        while(flag):
            line = f.readline()
            if (line.strip() == content):
                position = f.tell()
                flag = False
                break
        
        # 文件中未出现制定的目录层次
        if (flag):
            f.write('\n' + content)
            writeContext(f)
        else:
            f.seek(position)
            writeContext(f)

    # except:
    #     print('读取目标文件失败!!!')
    finally:
        if (f):
            f.close()
    
def writeContext(f):
    title = input('请输入title：')
    url = input('请输入链接地址:')
    str = '\n' + '-    [' + title.strip() + '](' + url.strip() + ')'
    f.write(str)

def main():
    addContents()

if __name__ == '__main__':
    main()