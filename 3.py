##目录树
import os
def travelTree(currentPath, count):
    if not os.path.exists(currentPath):
        return
    if os.path.isfile(currentPath):
        fileName = os.path.basename(currentPath)
        print '\t' * count + '├── ' + fileName
    elif os.path.isdir(currentPath):
        print '\t' * count + '├── ' + currentPath
        pathList = os.listdir(currentPath)
        for eachPath in pathList:
            travelTree(currentPath+'/'+eachPath, count+1)

travelTree('D:\php study\php code',1)
