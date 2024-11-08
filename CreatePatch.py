import tkinter
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import bsdiff4
import os
import shutil
import json


def initUi():
    root = tkinter.Tk()
    root.title("补丁生成")
    root.geometry("640x240+10+10")
    root.resizable(False, False)
    ttk.Style("sandstone")
    frame1 = Frame(root, padx=16, pady=12)
    frame2 = Frame(root, padx=16, pady=12)
    frame3 = Frame(root, padx=16, pady=6)
    frame4 = Frame(root, padx=16, pady=12)

    # origin build file src
    label = Label(frame1, text="原始打包目录", width=15, justify=LEFT)
    desdir = Entry(frame1, fg="#999999", width=50)
    label.pack(side=LEFT)
    desdir.pack(side=LEFT)
    desdir.config(state="disable")
    buttondir = ttk.Button(
        frame1, text="选择", width=24, command=lambda: selectDir(desdir)
    )
    buttondir.pack(side=LEFT, padx=32, pady=8)

    # update build file src
    label2 = Label(frame2, text="新打包目录", width=15, justify=LEFT)
    des2dir = Entry(frame2, fg="#999999", width=50)
    des2dir.config(state="disable")
    label2.pack(side=LEFT)
    des2dir.pack(side=LEFT)
    buttondir = ttk.Button(
        frame2, text="选择", width=24, command=lambda: selectDir(des2dir)
    )
    buttondir.pack(side=LEFT, padx=32, pady=8)

    # patch label
    patchLabel = Label(frame3, text="", justify=LEFT)
    patchLabel.pack(side=TOP)

    # patch create btn
    buttonstart = ttk.Button(
        frame4,
        text="生成",
        width=32,
        command=lambda: checkFiles(desdir, des2dir, patchLabel),
        bootstyle="success",
    )
    buttonstart.pack(side=BOTTOM)

    frame1.pack(fill=X)
    frame2.pack(fill=X)
    frame3.pack(fill=X)
    frame4.pack(fill=X)

    root.mainloop()


# 检查文件
def checkFiles(origin, des, patchLabel):
    orginPath = origin.get()
    desPath = des.get()
    if desPath != None and orginPath != None:
        orginDic = checkParent(orginPath)
        desDic = checkParent(desPath)
        patchPathDir = "./dist"
        if not os.path.exists(patchPathDir):
            os.mkdir(patchPathDir)
        outputJson = []
        for key in desDic:
            des = {}
            if key in orginDic:
                patchPath = patchPathDir + "/" + key + ".patch"
                patchLabel.config(text="create..." + patchPath)
                bsdiff4.file_diff(orginDic[key], desDic[key], patchPath)
                des["key"] = key
                des["type"] = "patch"
                des["parentDir"] = findParentDir(desDic[key])
                des["patchName"] = key + ".patch"
            else:
                shutil.copyfile(desDic[key], patchPathDir + "/" + key)
                des["key"] = key
                des["parentDir"] = findParentDir(desDic[key])
                des["type"] = "add"
            outputJson.append(des)
        with open(patchPathDir + "/patch.json", "w") as fd:
            fd.write(json.dumps(outputJson))


def findParentDir(path):
    if "Managed" in path:
        return "Managed"
    elif "Resources" in path:
        return "Resources"
    else:
        return ""


def checkParent(parentPath):
    for item in os.scandir(parentPath):
        if item.is_dir():
            if "_Data" in item.path:
                return checkDataDir(item.path)


# 检查data文件目录
def checkDataDir(dataPath):
    result = {}
    for item in os.scandir(dataPath):
        if item.is_dir():
            if "Managed" in item.path:
                checkCshaperChangeDiff(item.path, result)
            if "Resources" in item.path:
                checkResourceChangeDiff(item.path, result)
        if item.is_file():
            checkSceneFileLinkFiles(item, result)
    return result


# 生成代码文件diff
def checkCshaperChangeDiff(assemablePath, result):
    for item in os.scandir(assemablePath):
        if item.is_file():
            if "Assembly-CSharp" in item.path:
                result[item.name] = item.path


# 生成动态Res资源diff
def checkResourceChangeDiff(resourcePath, result):
    for item in os.scandir(resourcePath):
        if item.is_file():
            result[item.name] = item.path


# 生成静态资源diff
def checkSceneFileLinkFiles(item, result):
    if item.is_file():
        result[item.name] = item.path


# diff打包生成patch
def createPatch():
    return


# 选择目录
def selectDir(self):
    path = askdirectory()
    self.config(state="normal")
    self.delete(0, END)
    self.insert(0, path)
    self.config(state="disable")


initUi()
