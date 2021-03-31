import os,configparser
import tkinter as tk
from tkinter import font as tf
import dataPack
import time


class lotteryUI(tk.Frame):
    def __init__(self,**kwargs):
        self.config = kwargs.pop('CONFIG')
        self.data_path = kwargs.pop('DATA_PATH')
        print(self.config.sections())
        tk.Frame.__init__(self,**kwargs)
        self.TITLE_FONT = tf.Font(family="宋体",size=40,weight=tf.BOLD)
        self.LABEL_FONT = tf.Font(family="宋体",size=27,weight=tf.BOLD)
        self.INFO_FONT = tf.Font(family="宋体",size=20)
        self.space = int(self.config['LOTTERY_CONFIG']['NUM_SPACE'])
        self.load(os.path.join(self.data_path,self.config['LOTTERY_CONFIG']['CSV_PATH']))
        self.init()
    
    def init(self):
        self.batch_size = int(self.config['LOTTERY_CONFIG']['BATCH_SIZE'])
        self.pause_time = int(self.config['LOTTERY_CONFIG']['PAUSE_TIME'])
        self.wait_time = int(self.config['LOTTERY_CONFIG']['WAIT_TIME'])
        self.time_stamp = time.time()

        #Create UI

        #Control Frame
        self.CONTROL_FRAME = tk.Frame(master = self,width=240)
        self.CONTROL_FRAME.pack(side=tk.RIGHT,fill=tk.Y)
        self.SETTING_FRAME = tk.Frame(master = self.CONTROL_FRAME)
        self.INFO_BUTTON = tk.Button(master=self.SETTING_FRAME,text="完成",width=8,font=self.LABEL_FONT,command=self.showInfo)
        self.INFO_BUTTON.pack(side=tk.BOTTOM,fill=tk.X,expand=False,padx=30,pady=30)
        self.INFO_FRAME = tk.Frame(master=self.CONTROL_FRAME)
        self.SETTING_BUTTON = tk.Button(master=self.INFO_FRAME,text="设置",width=8,height=1,font=self.LABEL_FONT,command=self.showSetting)
        self.SETTING_BUTTON.pack(side=tk.BOTTOM,fill=tk.X,expand=False,padx=30,pady=(0,30))
        self.START_BUTTON = tk.Button(master=self.INFO_FRAME,text="开始",width=8,font=self.LABEL_FONT,command=self.start)
        self.START_BUTTON.pack(side=tk.BOTTOM,fill=tk.X,expand=False,padx=30,pady=(30,0))
        self.NUM_SPACE_LABEL = tk.Label(master = self.INFO_FRAME,text="寄包箱数",font=self.LABEL_FONT)
        self.NUM_SPACE_INFO = tk.Label(master = self.INFO_FRAME,text="0",font=self.LABEL_FONT)
        self.NUM_TOTAL_CANDIDATE_LABEL = tk.Label(master = self.INFO_FRAME,text="参与人数",font=self.LABEL_FONT)
        self.NUM_TOTAL_CANDIDATE_INFO = tk.Label(master = self.INFO_FRAME,text="0",font=self.LABEL_FONT)
        self.NUM_PICKED_LABEL = tk.Label(master = self.INFO_FRAME,text="已选人数",font=self.LABEL_FONT)
        self.NUM_PICKED_INFO = tk.Label(master = self.INFO_FRAME,text="0",font=self.LABEL_FONT)
        self.NUM_CANDIDATE_LABEL = tk.Label(master = self.INFO_FRAME,text="剩余人数",font=self.LABEL_FONT)
        self.NUM_CANDIDATE_INFO = tk.Label(master = self.INFO_FRAME,text="0",font=self.LABEL_FONT)
        self.NUM_SPACELEFT_LABEL = tk.Label(master = self.INFO_FRAME,text="剩余箱数",font=self.LABEL_FONT)
        self.NUM_SPACELEFT_INFO = tk.Label(master = self.INFO_FRAME,text="0",font=self.LABEL_FONT)
        
        self.NUM_SPACE_LABEL.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(15,0))
        self.NUM_SPACE_INFO.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(10,15))
        self.NUM_TOTAL_CANDIDATE_LABEL.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(15,0))
        self.NUM_TOTAL_CANDIDATE_INFO.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(10,15))
        self.NUM_PICKED_LABEL.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(15,0))
        self.NUM_PICKED_INFO.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(10,15))
        self.NUM_CANDIDATE_LABEL.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(15,0))
        self.NUM_CANDIDATE_INFO.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(10,15))
        self.NUM_SPACELEFT_LABEL.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(15,0))
        self.NUM_SPACELEFT_INFO.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(10,15))

        self.NUM_SPACE_LABEL_SETTING = tk.Label(master = self.SETTING_FRAME,text="寄包箱数",font=self.LABEL_FONT)
        self.NUM_SPACE_INFO_SETTING = tk.Entry(master = self.SETTING_FRAME,font=self.LABEL_FONT,justify='center',width=8)
        self.NUM_SPACE_INFO_SETTING.bind('<Return>',self.setSpace)
        self.NUM_PAUSE_LABEL_SETTING = tk.Label(master = self.SETTING_FRAME,text="等待时间",font=self.LABEL_FONT)
        self.NUM_PAUSE_INFO_SETTING = tk.Entry(master = self.SETTING_FRAME,font=self.LABEL_FONT,justify='center',width=8)
        self.NUM_PAUSE_INFO_SETTING.bind('<Return>',self.setPause)
        self.NUM_BATCH_LABEL_SETTING = tk.Label(master = self.SETTING_FRAME,text="批处理数",font=self.LABEL_FONT)
        self.NUM_BATCH_INFO_SETTING = tk.Entry(master = self.SETTING_FRAME,font=self.LABEL_FONT,justify='center',width=8)
        self.NUM_BATCH_INFO_SETTING.bind('<Return>',self.setBatch)

        self.NUM_SPACE_LABEL_SETTING.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(15,0))
        self.NUM_SPACE_INFO_SETTING.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(10,15))
        self.NUM_PAUSE_LABEL_SETTING.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(15,0))
        self.NUM_PAUSE_INFO_SETTING.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(10,15))
        self.NUM_BATCH_LABEL_SETTING.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(15,0))
        self.NUM_BATCH_INFO_SETTING.pack(side=tk.TOP,fill=tk.Y,expand=False,pady=(10,15))

        self.INFO_FRAME.pack(fill=tk.BOTH,expand=True)
        self.SETTING_FRAME.pack(fill=tk.BOTH,expand=True)
        self.SETTING_FRAME.pack_forget()

        #Title Frame
        self.TITLE_FRAME = tk.Frame(master=self,height=60)
        self.TITLE_FRAME.pack(fill=tk.X,expand=False)
        self.TITLE = tk.Label(master=self.TITLE_FRAME,text="未指定",font=self.TITLE_FONT)
        self.TITLE.pack(fill=tk.X,expand=False)
        # Main
        self.MAIN_SCROLL = tk.Scrollbar(master=self,orient=tk.VERTICAL)
        self.MAIN_SCROLL.pack(side=tk.RIGHT,fill=tk.BOTH,expand=False)
        self.MAIN_VIEW = tk.Listbox(master=self,font=self.LABEL_FONT)
        self.MAIN_VIEW.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=(40,0))
        self.MAIN_VIEW.config(yscrollcommand = self.MAIN_SCROLL.set)
        self.MAIN_SCROLL.config(command=self.MAIN_VIEW.yview)

        self.updateInfoStatus()

    def updateInfoStatus(self):
        self.TITLE.config(text=self.data.title)
        self.NUM_SPACE_INFO.config(text=str(self.data.space))
        self.NUM_TOTAL_CANDIDATE_INFO.config(text=str(len(self.data.picked)+len(self.data.waitlist)+len(self.data.candidate)))
        self.NUM_PICKED_INFO.config(text=str(len(self.data.picked)))
        self.NUM_CANDIDATE_INFO.config(text=str(len(self.data.candidate))+("+"+str(len(self.data.waitlist)) if len(self.data.waitlist) else ""))
        self.NUM_SPACELEFT_INFO.config(text=str(self.data.space-len(self.data.picked)))
        self.updateMainStatus()
    def updateSettingStatus(self):
        self.NUM_SPACE_INFO_SETTING.delete(0,tk.END)
        self.NUM_SPACE_INFO_SETTING.insert('end',str(self.data.space))
        self.NUM_PAUSE_INFO_SETTING.delete(0,tk.END)
        self.NUM_PAUSE_INFO_SETTING.insert('end',str(self.pause_time))
        self.NUM_BATCH_INFO_SETTING.delete(0,tk.END)
        self.NUM_BATCH_INFO_SETTING.insert('end',str(self.batch_size))

    def setSpace(self,event):
        self.data.modifySpace(int(self.NUM_SPACE_INFO_SETTING.get()))
        self.space = self.data.space
    def setPause(self,event):
        self.pause_time = int(self.NUM_PAUSE_INFO_SETTING.get())
    def setBatch(self,event):
        self.batch_size = int(self.NUM_BATCH_INFO_SETTING.get())
    
    def updateMainStatus(self):
        ys = int(self.MAIN_VIEW.yview()[0] * self.MAIN_VIEW.size())
        self.MAIN_VIEW.delete(0,tk.END)
        for p in self.data.picked:
            self.MAIN_VIEW.insert(tk.END,self.strfperson(p.getData()))
        self.MAIN_VIEW.yview_scroll(ys,'units')

    def start(self):
        self.startRoll = True
        self.START_BUTTON.configure(text='暂停',command=self.pause)
        self.time_stamp = time.time()
        self.draftorauto()

    def pause(self):
        self.START_BUTTON.configure(text='开始',command=self.start)
        self.startRoll = False
        self.updateInfoStatus()

    def showSetting(self):
        self.SETTING_FRAME.pack(fill=tk.BOTH,expand=True)
        self.INFO_FRAME.pack_forget()
        self.updateSettingStatus()
    def showInfo(self):
        self.setSpace(None)
        self.setPause(None)
        self.setBatch(None)
        self.INFO_FRAME.pack(fill=tk.BOTH,expand=True)
        self.SETTING_FRAME.pack_forget()
        self.updateInfoStatus()
    
    def roll(self):
        self.updateInfoStatus()
        dice_val = self.data.rollDice(self.batch_size)
        for dice in dice_val:
            self.MAIN_VIEW.insert(tk.END,self.strfperson(self.data.candidate[dice].getData()))
        self.MAIN_VIEW.yview_scroll(len(dice_val),'unit')
    def pickroll(self):
        dice_val = self.data.rollDice(self.batch_size)
        self.data.pickmulti(dice_val)
        self.updateInfoStatus()
        self.MAIN_VIEW.yview_scroll(len(dice_val),'unit')

    def draftorauto(self):
        if len(self.data.picked)>=self.data.space:
            if time.time()-self.time_stamp>self.pause_time:
                self.time_stamp = time.time()
                if self.MAIN_VIEW.yview()[1]==1.0:
                    self.MAIN_VIEW.yview_moveto(0)
                else:
                    self.MAIN_VIEW.yview_scroll(1,'pages')
            self.MAIN_VIEW.after(self.wait_time,self.draftorauto)
        else:
            if self.startRoll:
                if time.time()-self.time_stamp>self.pause_time:
                    self.pickroll()
                    self.time_stamp = time.time()
                    if len(self.data.picked) == self.data.space:
                        self.data.save("Result")
                        self.pause_time *= 5
                        #self.draftorauto()
                    # freeze the page for 5x wait time so that people can see results
                    self.MAIN_VIEW.after(self.wait_time*5,self.draftorauto)
                else:
                    self.roll()
                    self.MAIN_VIEW.after(self.wait_time,self.draftorauto)
                

        


    def strfperson(self,pdata):
        lenID=len(str(pdata[0]))
        lenName = len(str(pdata[1]))
        sID = (15 - lenID) 
        sName =  (8 - lenName)*2
        return str(pdata[0]) + sID*" " + str(pdata[1])+sName*" "+str(pdata[2])

    def load(self,path_to_csv=''):
        self.data = dataPack.dataPack("",self.space)
        self.data.load(path_to_csv)

if __name__ == '__main__':
    app = tk.Tk()
    lui = lotteryUI(master=app,bg='red')
    lui.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
    app.update()
    app.mainloop()