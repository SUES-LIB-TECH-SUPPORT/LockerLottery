import os, sys, csv, math

DATA_FILE = 'data.csv'
OUTPUT_FILE = 'result.csv'

def loadData(data_file=DATA_FILE):
	data = []
	with open(data_file,'rb') as cfp:
		cdata = csv.reader(cfp,delimiter=":",quotechar='\'')
		for row in cdata:
			data.append(row)
	return data

def saveData(data=[[]],data_file=OUTPUT_FILE):
	with open(data_file,'w') as ofp:
		for row in data:
			try:
				ofp.write(":".join([str(element) for element in row])+"\n\r")
			except:
				pass					

def strfperson(pdata,show_cell=False):
	try:
		id_section = pdata[0].decode('utf-8')
		name_section = pdata[1].decode('utf-8')
		cell_section = pdata[2].decode('utf-8')
		result = u"\t"+id_section+u"\t" + name_section
		if show_cell:
			result += u"\t\t" + cell_section
		result += u"\n\r"
	except:
		result = u"\n\r"
	return result
	#return " ".join(pdata).decode('utf-8')

def cls():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
	
try:
    from msvcrt import getch
except ImportError:
    def getch():
        """
        Gets a single character from STDIO.
        """
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

	
	
