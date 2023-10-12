import yaml
import ctypes
from pathlib import Path
import tkinter as tk
import _thread

WIDTH=1278
HEIGHT=716
CONFIG_PATH = Path(".") / "config.yml"

def load_yml(file: Path, encoding="utf-8") -> dict:
    with open(file, "r", encoding=encoding) as f:
        data = yaml.safe_load(f)
    return data

def dump_yml(file: Path,project, encoding="utf-8") -> dict:
    with open(file, "w", encoding=encoding) as f:
        yaml.dump(project,f)
        f.close()

def atoi(s):
    s = s[::-1]
    num = 0
    for i, v in enumerate(s):
        for j in range(0, 10):
            if v == str(j):
                num += j * (10 ** i)
    return num

def Save():
    su=env.su_input.get()
    id=atoi(env.id_input.get())
    pw=env.pw_input.get()
    env.cfg['BotSelfConfig']['superusers'][0]=su
    env.cfg['account']['uin']=id
    env.cfg['account']['password']=pw
    dump_yml(CONFIG_PATH,env.cfg)

def Quit():
    Save()
    try:
        env.destroy()
    except:
        pass
    # print('Quit!')
    exit(0)

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.title('Gal Voice Launcher')
        self.protocol("WM_DELETE_WINDOW", lambda: Quit())
        self._build_maze()
        #self.geometry('{0}x{1}'.format(10 * 30, 10 * 30))
        self.resizable(False,False)
        self.cfg=load_yml(CONFIG_PATH)
        # _thread.start_new_thread(self.Play_Music,(0,))
        self.Init_Home()
    
    def _build_maze(self):
        moni=ctypes.windll.user32
        global wt
        global ht
        wt=moni.GetSystemMetrics(0)
        ht=moni.GetSystemMetrics(1)
        self.geometry("{0}x{1}+{2}+{3}".format(WIDTH,HEIGHT,int((wt-WIDTH)/2),int((ht-HEIGHT)/2)))
        self.canvas = tk.Canvas(self,bg='pink',
                        height=HEIGHT,
                        width=WIDTH)
        global bk
        bk = tk.PhotoImage(file = "pic/atri.png")
        image = self.canvas.create_image(WIDTH/2, HEIGHT/2, image=bk)
        self.canvas.pack()
    
    def Init_Home(self):
        su=self.cfg['BotSelfConfig']['superusers'][0]
        id=self.cfg['account']['uin']
        pw=self.cfg['account']['password']
        su_ = tk.StringVar()
        id_ = tk.StringVar()
        pw_ = tk.StringVar()
        su_.set(su)
        id_.set(str(id))
        pw_.set(pw)
        name_saved=tk.StringVar()
        self.su_input=tk.Entry(self,textvariable=su_)
        self.id_input=tk.Entry(self,textvariable=id_)
        self.pw_input=tk.Entry(self,textvariable=pw_,show='*')
        self.su_label=tk.Label(self,text="superuser:")
        self.id_label=tk.Label(self,text="id:")
        self.pw_label=tk.Label(self,text="password:")
        self.Launch=tk.Button(self,text="Launch",command=self.Launch)
        self.Exit=tk.Button(self,text="Quit",command=Quit)
        self.Place_Home()
    
    def Place_Home(self):
        print('fkpps')
        self.Exit.pack()
        self.Exit.place(x=10,y=50,width=100)
        self.su_label.pack()
        self.su_label.place(x=10,y=100,width=80)
        self.su_input.pack()
        self.su_input.place(x=90,y=100,width=100)
        self.id_label.pack()
        self.id_label.place(x=10,y=150,width=80)
        self.id_input.pack()
        self.id_input.place(x=90,y=150,width=100)
        self.pw_label.pack()
        self.pw_label.place(x=10,y=200,width=80)
        self.pw_input.pack()
        self.pw_input.place(x=90,y=200,width=100)
        self.Launch.pack()
        self.Launch.place(x=10,y=250,width=100)

    def Launch(self):
        Save()
        os.system('start cmd /K "go-cqhttp.exe"')
        os.system('start powershell Python38/python bot.py')
        Quit()

import os
if __name__=='__main__':
    env=Maze()
    env.mainloop()