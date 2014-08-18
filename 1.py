import os
def tree(path, count = 1):
    if not os.path.exists(path):
        return
    list = os.listdir(path)
    for i in list:
        if os.path.isfile(path+'/'+i):
            print '\t'*count+'├──'+os.path.basename(path+'/'+i)
        elif os.path.isdir(path+'/'+i):
            print '\t'*count+'├──'+path+'/'+i
            tree(path+'/'+i,count+1)

tree('D:\php study\php code')
