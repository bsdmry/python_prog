#!/usr/bin/env python3
import tkinter as tk
import threading

class WinGame(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.start()
	
	def taskloop(self):
		self.app.after(100, self.taskloop)

	def close_win_handle(self):
		self.app.quit()

	def run(self):
		self.viewlist = {};
		self.app = tk.Frame(master = None)
		self.app.master.title("Template app")
		#self.app.master.maxsize(800, 600)
		self.app.master.geometry('{}x{}'.format(800,600)) 
		self.app.master.protocol("WM_DELETE_WINDOW", self.close_win_handle)
		self.app.after(100, self.taskloop)
		self.app.mainloop()

	def set_win_name(self, winname):
		self.app.master.title(winname)
	
	def show_view(self, view_id=None):
		if view_id != None:
			self.app.master.geometry('{}x{}'.format(self.viewlist[view_id]['width'], self.viewlist[view_id]['height']))
			self.app.master.title(self.viewlist[view_id]['title'])
			for control_id in self.viewlist[view_id]['controls'].keys():
				obj = tk.Button(self.app.master, text=self.viewlist[view_id]['controls'][control_id]['text'], command=self.viewlist[view_id]['controls'][control_id]['action'], bg=self.viewlist[view_id]['controls'][control_id]['bgcolor'], fg=self.viewlist[view_id]['controls'][control_id]['fgcolor']).place(x=self.viewlist[view_id]['controls'][control_id]['x'], y=self.viewlist[view_id]['controls'][control_id]['y'])
				setattr(self.app.master, control_id, obj)
		
	def create_view(self, view_id='view1', w=800, h=600, title='Window title'):
		if view_id not in self.viewlist:
			self.viewlist[view_id] = {'width': w, 'height': h, 'title':title, 'controls':{}}
		else:
			print("Error! View {} already exists!".format(view_id))

	def add_button(self, view_id='View', control_id='btn1', text='Btn', bgcolor='white', fgcolor='black', x = 0, y = 0, action = None):
			
		if view_id in self.viewlist:	
			if control_id not in self.viewlist[view_id]['controls']:
				self.viewlist[view_id]['controls'][control_id] = {'text':text, 'bgcolor':bgcolor, 'fgcolor':fgcolor, 'x':x, 'y':y, 'action':action}
			else:
				print("Error! Button {} already exist in view {}".format(control_id, view_id))
		else:
			print("Error! View {} doesn't exist!".format(view_id))
			
