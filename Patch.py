import tkinter
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import bsdiff4
import os
import json


def initUi():
    root = tkinter.Tk()
    root.geometry("640x240+10+10")
    root.resizable(False, False)
    ttk.Style("sandstone")
    root.title("打补丁")
    frame1 = Frame(root, padx=16, pady=12)
    frame2 = Frame(root, padx=16, pady=12)
    frame3 = Frame(root, padx=16, pady=12)

    # origin build file src
    label = Label(frame1, text="安装目录", width=15, justify=LEFT)
    desdir = Entry(frame1, fg="#999999", width=50)
    desdir.config(state="disable")
    label.pack(side=LEFT)
    desdir.pack(side=LEFT)

    buttondir = ttk.Button(
        frame1,
        text="选择",
        width=24,
        command=lambda: selectDir(desdir),
    )
    buttondir.pack(side=LEFT, padx=32, pady=8)

    # update build file src
    label2 = Label(frame2, text="补丁位置", width=15, justify=LEFT)
    des2dir = Entry(frame2, fg="#999999", width=50)
    des2dir.config(state="disable")
    label2.pack(side=LEFT)
    des2dir.pack(side=LEFT)
    buttondir = ttk.Button(
        frame2, text="选择", width=24, command=lambda: selectDir(des2dir)
    )
    buttondir.pack(side=LEFT, padx=32, pady=8)

    # patch create btn
    buttonstart = ttk.Button(
        frame3,
        text="执行",
        width=32,
        command=lambda: patchFile(desdir, des2dir),
        bootstyle="success",
    )
    buttonstart.pack(side=BOTTOM)

    frame1.pack(fill=X)
    frame2.pack(fill=X)
    frame3.pack(fill=X)

    root.mainloop()


# use patch
def patchFile(origin, patch):
    patchPath = patch.get()
    installPath = origin.get()
    patchInfo = []
    for patchFile in os.scandir(patchPath):
        if patchFile.is_file() and patchFile.name.endswith(".json"):
            with open(patchFile.path, "r") as f:
                patchInfo = json.load(f)
    for file in os.scandir(installPath):
        if file.is_dir() and "_Data" in file.name:
            for dataFile in os.scandir(file.path):
                if dataFile.is_dir() and dataFile.path in "Managed":
                    patchScript()
                elif dataFile.is_dir() and dataFile.name in "Resources":
                    patchResources()
                elif dataFile.is_file():
                    patchOthers(patchInfo, dataFile, patchPath)


def patchOthers(patchInfo, dataFile, patchPath):
    for patch in patchInfo:
        if patch["key"] == dataFile.name and patch["type"] == "patch":
            patchRealPath = patchPath + "/" + patch["patchName"]
            print(patchRealPath)
            print(dataFile.path)
            bsdiff4.file_patch_inplace(dataFile.path, patchRealPath)


def patchScript():
    return


def patchResources():
    return


def selectDir(self):
    path = askdirectory()
    self.config(state="normal")
    self.delete(0, END)
    self.insert(0, path)
    self.config(state="disable")


initUi()
