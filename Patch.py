import tkinter
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk


def initUi():
    root = tkinter.Tk()
    root.title("打补丁")
    frame1 = Frame(root, padx=16, pady=6)
    frame2 = Frame(root, padx=16, pady=6)

    # origin build file src
    label = Label(frame1, text="安装目录", width=15, justify=LEFT)
    desdir = Entry(frame1, fg="#999999", width=30)
    label.pack(side=LEFT)
    desdir.pack(side=LEFT)
    buttondir = ttk.Button(frame1, text="选择", command=lambda: selectDir(desdir))
    buttondir.pack(side=LEFT, padx=8, pady=8)

    # update build file src
    label2 = Label(frame2, text="补丁位置", width=15, justify=LEFT)
    des2dir = Entry(frame2, fg="#999999", width=30)
    label2.pack(side=LEFT)
    des2dir.pack(side=LEFT)
    buttondir = ttk.Button(frame2, text="选择", command=lambda: selectDir(desdir))
    buttondir.pack(side=LEFT, padx=8, pady=8)

    frame1.pack(fill=X)
    frame2.pack(fill=X)

    root.mainloop()


def selectDir(self, p):
    path = askdirectory()
    p.delete(0, "end")
    p.insert(0, path)
    self.dirpath.set(path)


initUi()
