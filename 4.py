##打印制定目录下csv后缀的文件 通过默认值模拟静态变量mylist
import os
def tree(path,mylist = []):
    if os.path.isfile(path): return
    dir = os.listdir(path)
    for each in dir:
        if os.path.isdir(path+'/'+each):
            tree(path+'/'+each)
        else:
            if each.endswith('csv'):
                mylist.append(each)

    return mylist


print tree('D:\php study\php code\caiji')

    
