# -*-coding:utf-8-*-
import os, sys, math, threading, time, random, configparser
import utils

DEFAULT_KEYMAP = {
					"up":["w"],
					"down":["s"],
					"left":["a"],
					"right":["d"],
					"confirm":["j"],
					"cancel":["k"]
				}

DEFAULT_DP_LINES = 10
DEFAULT_PAGE_TIME = 4 #in ms
DEFAULT_DATA_FILE = 'test_data.csv'
DEFAULT_OUTPUT_FILE = 'result.csv'
DEFAULT_CACHE_FILE = 'cache'
DEFAULT_SPACE = 5

LOG_FILE = 'app.log'


class app:
	def __init__(self,DP_LINES = DEFAULT_DP_LINES, KEYMAP = DEFAULT_KEYMAP,DATA_FILE = DEFAULT_DATA_FILE, SPACE = DEFAULT_SPACE, OUTPUT_FILE = DEFAULT_OUTPUT_FILE, CACHE_FILE=DEFAULT_CACHE_FILE):
		self.DP_LINES = DP_LINES
		self.KEYMAP = KEYMAP
		self.DATA_FILE = DATA_FILE
		self.SPACE = SPACE
		self.OUTPUT_FILE = OUTPUT_FILE
		self.CACHE_FILE = CACHE_FILE
		self.SHOW_CELL = False
		self.PAGE_TIME = DEFAULT_PAGE_TIME
		
		self.main_menu = 	[
					"Start/Step",
					"Auto View",
					"Save Result",
					"Settings",
					"Exit"
				]
		self.setting_menu = [
					"Reload Data",
					self.SPACE,
					self.DP_LINES,
					self.PAGE_TIME,
					self.SHOW_CELL,
					"BACK"
				]
		self.confirm_dialog = [
							"yes",
							"no"
						]
		self.autoview_dialog = [
								"quit"
								]
		
		self.menu_system = [self.main_menu,self.setting_menu,self.confirm_dialog,self.autoview_dialog]
		self.menu_stack = [[0,1]]
		
		self.AUTO_VIEW = False
		self.PENDINGACT = None
		self.PAGE = 0
		self.PROGRESS_WIDTH = 60.0
		self.TIMER = [0,time.time()]
		self.RESULT = []
		self.ROLLING = False
		
		self.key_thread = threading.Thread(target=self.getKey)
		self.key_thread.setDaemon(True)
		
		self.initiate()
		
	def start(self):
		self.RUNNING = True
		self.key_thread.start()
		self.disp()
		self.hasUpdate = False
		self.LOG("New session starts")
		while self.RUNNING:
			
			if self.ROLLING:
				self.hasUpdate = True
			
			if self.AUTO_VIEW:
				self.TIMER[0] = time.time()-self.TIMER[1]
				if self.TIMER[0]>self.PAGE_TIME:
					self.TIMER[0] -= self.PAGE_TIME
					self.PAGE = (self.PAGE+1) % self.PAGES
					self.TIMER[1] = time.time()
				self.hasUpdate = True
			if self.hasUpdate:
				self.disp()
				time.sleep(0.03)
	
	def LOG(self,message):
		global LOG_FILE
		if not os.path.exists(LOG_FILE):
			with open(LOG_FILE,'w+') as logf:
				pass
		with open(LOG_FILE,'a') as logf:
			t = time.time()
			logf.write("[{}.{}] {}\n\r".format(time.ctime(t),t-int(t),message))
	def calcPages(self):
		self.PAGES = int(math.ceil(self.SPACE * 1.0 / self.DP_LINES))
	def fixPage(self):
		self.PAGE = max(min(self.PAGE,self.PAGES-1),0)
	def loadData(self):
		self.DATA = utils.loadData(self.DATA_FILE)
		self.LOG(self.DATA_FILE + " Loaded")
		#for i in range(15):
		#	self.RESULT.append(self.DATA[i])
	def initiate(self):
		self.AUTO_VIEW = False
		self.PENDINGACT = None
		self.PAGE = 0
		self.RESULT = []
		self.loadData()
		self.calcPages()
		self.fixPage()
		self.LOG("Initiated")
	def nextPage(self):
		self.PAGE = min(self.PAGE+1,self.PAGES-1)
	def prevPage(self):
		self.PAGE = max(self.PAGE-1,0)
	def gotoLastPage(self):
		self.PAGE = min(self.PAGES-1,int(len(self.RESULT)/self.DP_LINES))
	
	def isDone(self):
		return len(self.RESULT)==self.SPACE
	
	def getKey(self):
		while self.RUNNING:
			key = utils.getch()
			self.keyAction(key)
	def keyAction(self,key):
		key = key.lower()
		if key in self.KEYMAP["up"]:
			if self.menu_stack[-1][0] == 0:
				self.menu_stack.append([-1,0])
			elif self.menu_stack[-1][0] == 1:
				if self.menu_stack[-1][1] == 1:
					self.SPACE += 1
				elif self.menu_stack[-1][1] == 2:
					self.DP_LINES += 1
				elif self.menu_stack[-1][1] == 3:
					self.PAGE_TIME = min(10,self.PAGE_TIME+1)
				elif self.menu_stack[-1][1] == 4:
					self.SHOW_CELL = True
				else:
					#self.menu_stack.append([-1,0])
					pass
				self.calcPages()
				self.fixPage()
			self.hasUpdate = True
		elif key in self.KEYMAP["down"]:
			if self.menu_stack[-1][0] == -1:
				self.menu_stack.pop(-1)
			elif self.menu_stack[-1][0] == 1:
				if self.menu_stack[-1][1] == 1:
					self.SPACE = max(self.SPACE-1,len(self.RESULT))
				elif self.menu_stack[-1][1] == 2:
					self.DP_LINES -= 1
				elif self.menu_stack[-1][1] == 3:
					self.PAGE_TIME = max(0,self.PAGE_TIME-1)
				elif self.menu_stack[-1][1] == 4:
					self.SHOW_CELL = False
				self.calcPages()
				self.fixPage()
			self.hasUpdate = True
		elif key in self.KEYMAP["left"]:
			if self.menu_stack[-1][0]==-1:
				self.prevPage()
			else:
				self.menu_stack[-1][1] = max(self.menu_stack[-1][1]-1,0)
			self.hasUpdate = True
		elif key in self.KEYMAP["right"]:
			if self.menu_stack[-1][0]==-1:
				self.nextPage()
			else:
				#menu_length = len(self.main_main) if self.menu_stack[-1][0]==0
				#menu_length = len(self.setting_menu) if self.menu_stack[-1][0]==1
				#menu_length = len(self.confirm_dialog) if self.menu_stack[-1][0]==2
				#menu_length = len(self.auto_view_dialog) if self.menu_stack[-1][0]==3
				self.menu_stack[-1][1] = min(self.menu_stack[-1][1]+1,len(self.menu_system[self.menu_stack[-1][0]])-1)
			self.hasUpdate = True
		elif key in self.KEYMAP["confirm"]:
			if self.menu_stack[-1][0]==0:
				if self.menu_stack[-1][1] == 0: #roll page
					if self.ROLLING:
						#draw
						self.ROLLING = False
						self.draw(self.rollDice())
						self.hasUpdate= True
						if self.isDone():
							self.saveCache()
							self.LOG("Job Finished")
							self.saveResult()
					else:
						if not self.isDone():
							self.gotoLastPage()
							#roll dice
							if not len(self.RESULT)>(self.PAGE+1)*self.DP_LINES:
								self.ROLLING = True
						else:
							pass
				elif self.menu_stack[-1][1] == 1: #Auto View
					if self.isDone(): #all finished
						self.AUTO_VIEW = not self.AUTO_VIEW
						if self.AUTO_VIEW:
							self.TIMER = [0,time.time()]
							self.menu_stack.append([3,0])
					else:
						self.AUTO_VIEW = False
				elif self.menu_stack[-1][1] == 2: #Save Result
					if len(self.RESULT)==self.SPACE: #all finished
						self.PENDINGACT = self.saveResult
						self.menu_stack.append([2,0])
					else:
						#TODO add response here
						pass
				elif self.menu_stack[-1][1] == 3: #go to settings
					self.menu_stack.append([1,0])
				elif self.menu_stack[-1][1] == 4: #exit
					self.PENDINGACT = self.exit
					self.menu_stack.append([2,0])
			elif self.menu_stack[-1][0]==1:
				if self.menu_stack[-1][1] == 0: #Reload Data
					self.PENDINGACT = self.initiate
					self.menu_stack.append([2,0])
				elif self.menu_stack[-1][1] == 5: #back to menu
					self.menu_stack.pop(-1)
			elif self.menu_stack[-1][0]==2:
				if self.menu_stack[-1][1] == 0: #confirmed
					self.PENDINGACT()
					self.PENDINGACT = None
					self.menu_stack.pop(-1)
				elif self.menu_stack[-1][1] == 1:
					self.PENDINGACT = None
					self.menu_stack.pop(-1)
			elif self.menu_stack[-1][0]==3:
				self.AUTO_VIEW = False
				self.menu_stack.pop(-1)
			self.hasUpdate = True
		elif key in self.KEYMAP["cancel"]:
			if self.menu_stack[-1][0]==2:
				self.PENDINGACT = None
			elif self.menu_stack[-1][0]==3:
				self.AUTO_VIEW = False
			if (self.menu_stack[-1][0]==1) or (self.menu_stack[-1][0] == 2) or (self.menu_stack[-1][0] == 3):
				self.menu_stack.pop(-1)
			self.hasUpdate = True
	def getStatusBar(self):
		if self.menu_stack[-1][0] == -1:
			msg = u"Total [{}] Slots\n\r [{}] students, [{}] slots left\t\tPage <{}> out of {}\n\r".format(self.SPACE,len(self.DATA),self.SPACE-len(self.RESULT),self.PAGE+1,self.PAGES)
		else:
			msg = u"Total [{}] Slots\n\r [{}] students, [{}] slots left\t\tPage  {}  out of {}\n\r".format(self.SPACE,len(self.DATA),self.SPACE-len(self.RESULT),self.PAGE+1,self.PAGES)
		return msg		
	def getMenuBar(self):
		msg = u""# + str(self.menu_stack) + "\n\r"
		self.menu_system[1] = [
					u"Reload Data",
					self.SPACE,
					self.DP_LINES,
					self.PAGE_TIME,
					self.SHOW_CELL,
					u"BACK"
				]
		#print 'A'/'∀' for settings->SPACE/dp_lines
		print_ud_flag = False
		if self.menu_stack[-1][0] == 1:
			if self.menu_stack[-1][1] == 1 or self.menu_stack[-1][1] == 2 or self.menu_stack[-1][1] == 3 or self.menu_stack[-1][1] == 4:
				print_ud_flag = True
		#build menu section
		#SPACE_menu = self.main_menu if self.menu_stack[-1][0]==0 
		#SPACE_menu = self.setting_menu if self.menu_stack[-1][0]==1
		#SPACE_menu = self.confirm_dialog if self.menu_stack[-1][0]==2
		#SPACE_menu = self.auto_view_dialog if self.menu_stack[-1][0]==3
		if self.menu_stack[-1][0]==-1:
			menu_id = self.menu_stack[-2][0]
			sub_id = self.menu_stack[-2][1]
		else:
			menu_id = self.menu_stack[-1][0]
			sub_id = self.menu_stack[-1][1]
		SPACE_menu = self.menu_system[menu_id]
		menu_line = [u"",u"",u""]
		for i in range(len(SPACE_menu)):
			#print SPACE_menu
			menu_line[1] += (
								(
									(u" " + str(SPACE_menu[i]) + u" ")
									if i!=sub_id else 
									(u"{" + str(SPACE_menu[i]) + u"}")
								)
								+
								(u"\t" if i!=len(SPACE_menu)-1 else u"\n\r")
							)
			if print_ud_flag:
				menu_line[0] +=	(
									(
										(u" " + u' '*len(str(SPACE_menu[i])) + u" ")
										if i!=sub_id else
										(u" ▲" + u' '*len(str(SPACE_menu[i])))
									)
									+
									(u"\t" if i!=len(SPACE_menu)-1 else u"\n\r")
								)
				menu_line[2] +=	(
									(
										(u" " + u' '*len(str(SPACE_menu[i])) + u" ")
										if i!=sub_id else
										(u" ▼" + u' '*len(str(SPACE_menu[i])))
									)
									+
									(u"\t" if i!=len(SPACE_menu)-1 else u"\n\r")
								)
			else:
				menu_line[0] = u'\n\r'
				menu_line[2] = u'\n\r'
			if self.AUTO_VIEW:
				menu_line[0] = u"["+u"=" * (int(self.PROGRESS_WIDTH*self.TIMER[0]/self.PAGE_TIME))+u" "* (int(self.PROGRESS_WIDTH*(1.0-self.TIMER[0]/self.PAGE_TIME)))+u"]" + u"\n\r"
		for item in menu_line:
			msg+=item
		return msg
	def getList(self):
		if self.ROLLING:
			floating = self.rollDice()
		else:
			floating = [] 
		if len(self.RESULT) <= self.DP_LINES * self.PAGE:
			new_list = []
		else:
			new_list = self.RESULT[self.DP_LINES * self.PAGE:]
		for idx in floating:
			new_list.append(self.DATA[idx])
		msg = u"\n\r"
		for i in range(self.DP_LINES):
			if i < len(new_list):
				#id_section = new_list[i][0].decode('utf-8')
				#name_section =  new_list[i][1].decode('utf-8')
				
				#line = u"\t" +  new_list[i][0].decode('utf-8') + u"\t\t" + new_list[i][1].decode('utf-8') +u"\n\r"
				#line = u"\t".join([v.decode('utf-8') for v in new_list[i]]) +u"\n\r"
				line = utils.strfperson(new_list[i],self.SHOW_CELL)
			else:
				line = u"\n\r"
			msg+=line
		return msg
	def disp(self):
		utils.cls()
		msg = u" " + os.path.splitext(self.DATA_FILE)[0].decode("utf-8") + u"\n\r"
		#msg += str(self.ROLLING) + "\n\r"
		#msg += str(self.menu_stack) + "\n\r"
		#msg += str(self.RESULT)+ "\n\r"
		sys.stdout.write(msg)
		
		sys.stdout.write(self.getStatusBar())
		#self.getList()
		sys.stdout.write(self.getList())
		sys.stdout.write(self.getMenuBar())
		#sys.stdout.write(msg)
		self.hasUpdate = False
	def saveCache(self):
		utils.saveData(self.RESULT,self.CACHE_FILE)
	def saveResult(self):
		utils.saveData(self.RESULT,self.OUTPUT_FILE)
		self.LOG("Results saved to: " + self.OUTPUT_FILE)
	def exit(self):
		self.RUNNING = False
		self.key_thread.join()
	def rollDice(self):
		#num results on current Page
		num_r = len(self.RESULT) - self.DP_LINES * self.PAGE
		dice_val = []
		while len(dice_val)<min(self.DP_LINES-num_r,self.SPACE-len(self.RESULT)):
			rand_val = random.randint(0,len(self.DATA)-1)
			while rand_val in dice_val:
				rand_val = random.randint(0,len(self.DATA)-1)
			dice_val.append(rand_val)
		return dice_val
	
	def draw(self,lst):
		lst.sort(reverse=True)
		result = []
		while len(lst)>0:
			result.append(self.DATA.pop(lst.pop(0)))
		self.LOG("Rolled: " + ",".join([str(item[0]) for item in result]))
		self.RESULT += result
	
if __name__ == "__main__":
	p = app()
	p.start()
	
