import os, sys, datetime, random
import codecs
import csv

DEFAULT_MASK_CHAR = "※"
LOG_TIME_FORMAT = "[%y%m%d][%H:%M:%S][%f]"

class candidateInfo():
    def __init__(self,eid=0,sid=None,name=None,cell=None):
        self.eid = eid
        self.name = name
        self.sid = sid
        self.cell = cell
    def getName(self,mask=DEFAULT_MASK_CHAR):
        if mask is None:
            if self.name is None:
                return "[没有数据]"
            else:
                return self.name
        else:
            if len(self.name)>2:
                name = self.name[0] + mask*(len(self.name)-2) + self.name[-1]
            else:
                name = self.name[0] + mask
            return name
    def getSid(self):
        if self.sid is None:
            return "[没有数据]"
        else:
            return self.sid
    def getCell(self,mask=DEFAULT_MASK_CHAR):
        if mask is None:
            if self.sid is None:
                return "[没有数据]"
            else:
                return self.cell
        else:
            return self.cell[:3]+DEFAULT_MASK_CHAR*(len(self.cell)-7)+self.cell[-4:]
    def getData(self,mask=DEFAULT_MASK_CHAR):
        return [self.getSid(),self.getName(mask),self.getCell(mask)]

class dataPack():
    def __init__(self,title=None,space=0,candidate=[]):
        self.title = title
        self.space = space
        self.candidate = candidate
        self.picked = []
        self.waitlist = []
        self.log = []
        self.logActivity(self,"Datapack created for [%s] with [%d] spaces"%(title,space))
    def logActivity(self,source=None,activity=None):
        if not (source is None or activity is None):
            t = datetime.datetime.now()
            #self.log.append(t.strftime(LOG_TIME_FORMAT)+" <%s> %s"%(type(source).__name__,activity))
            self.log.append(t.strftime(LOG_TIME_FORMAT)+" %s"%activity)
            return True
        else:
            return False
    def load(self,path_to_csv=None):
        self.logActivity(self,"Trying to load candidates from [%s]"%path_to_csv)
        candidate = []
        dropped = []
        row_counter = 0
        title = os.path.basename(path_to_csv).split('.')[0]
        with codecs.open(path_to_csv,'r','utf-8') as cfp:
            cdata = csv.reader(cfp,delimiter=":",quotechar='\'')
            for row in cdata:
                row_counter += 1
                try:
                    c = candidateInfo(row_counter,row[0],row[1],row[2])
                    candidate.append(c)
                except Exception as e:
                    dropped.append([type(e).__name__,row_counter,row])
        self.logActivity(self,"[%d] candidates loaded from [%s] with [%d] errors"%(len(candidate),path_to_csv,len(dropped)))
        for i in range(len(dropped)):
            self.logActivity(self,"[%d]/[%d] [%s] on line [%d] '%s'"%(i,len(dropped),dropped[0],dropped[1],dropped[2]))
        self.candidate = candidate
        self.clearResult()
        self.setTitle(title)
    
    def save(self,path=""):
        os.makedirs(path,exist_ok=True)
        with codecs.open(os.path.join(path,'result.csv'),'w',encoding='utf-8') as ofp:
            for candidate in self.picked:
                try:
                    ofp.write(":".join(candidate.getData(None))+"\n")
                except:
                    pass
        self.logActivity(self,"Result saved to %s"%os.path.join(path,'result.csv'))
        with codecs.open(os.path.join(path,'waitlist.csv'),'w',encoding='utf-8') as ofp:
            for candidate in self.waitlist:
                try:
                    ofp.write(":".join(candidate.getData(None))+"\n")
                except:
                    pass
            for candidate in self.candidate:
                try:
                    ofp.write(":".join(candidate.getData(None))+"\n")
                except:
                    pass
        self.logActivity(self,"Waitlist saved to %s"%os.path.join(path,'waitlist.csv'))
        with codecs.open(os.path.join(path,'log.txt'),'w',encoding='utf-8') as ofp:
            for line in self.log:
                try:
                    ofp.write(line+"\n")
                except:
                    pass


    def clearResult(self):
        self.logActivity(self,"Clearing results")
        self.picked = []
        self.waitlist = []

    def setTitle(self,title=None):
        if title is None:
            return
        else:
            self.logActivity(self,"Title is set to [%s]"%title)
            self.title = title

    def pickone(self,idx=None):
        if idx is None:
            return
        elif len(self.picked)>=self.space:
            self.logActivity(self,"Already picked enough candidates")
            return
        elif idx>=len(self.candidate):
            self.logActivity(self,"Picking [%d] failed, [%d] candidates left"%(idx,len(self.candidate)))
            return
        else:
            self.logActivity(self,"Picking [%d] from candidates"%self.candidate[idx].eid)
            self.picked.append(self.candidate.pop(idx))
    
    def pickmulti(self,idx_list = []):
        for idx in idx_list:
            self.logActivity(self,"Picking [%d] with eid [%d] from candidates"%(idx,self.candidate[idx].eid))
            self.picked.append(self.candidate[idx])
        idx_list.sort(reverse=True)
        for idx in idx_list:
            self.logActivity(self,"Popping [%d] with eid [%d] from candidates"%(idx,self.candidate[idx].eid))
            self.candidate.pop(idx)
    
    def rollDice(self,num=0):
        num = min(min(num,len(self.candidate)),self.space-len(self.picked))
        dice_val = []
        while len(dice_val)<num:
            rand_val = random.randint(0,len(self.candidate)-1)
            while rand_val in dice_val:
                rand_val = random.randint(0,len(self.candidate)-1)
            dice_val.append(rand_val)
        self.logActivity(self,"Dice rolled, Result is %s"%str(dice_val))
        return dice_val
    

    def modifySpace(self,num=0):
        if num < len(self.picked):
            self.logActivity(self,"Space srinked, moving %s to waitlist"%[c.eid for c in self.picked[num:]])
            self.waitlist+=self.picked[num:]
            self.picked = self.picked[:num]
        elif num>(len(self.picked)):
            if len(self.waitlist)>0:
                n = num-len(self.picked)
                self.logActivity(self,"Space epanded, moving %s to picked"%[c.eid for c in self.waitlist[:n]])
                self.picked += self.waitlist[:n]
                self.waitlist = self.waitlist[n:]
        self.logActivity(self,"Modifying space from [%d] to [%d]"%(self.space,num))
        self.space = num


    

if __name__=='__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    d = dataPack("",9)
    d.load('2021寄包箱申请.csv')
    print(d.candidate[324].getData())
    d.pickmulti(d.rollDice(5))
    d.pickmulti(d.rollDice(5))
    d.modifySpace(7)
    d.save("tr")