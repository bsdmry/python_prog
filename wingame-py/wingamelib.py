#!/usr/bin/env python3
import tkinter as tk
import threading
from tkinter import PhotoImage

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
		self.current_view = None
		self.current_view_controls = []
		self.app = tk.Frame(master = None)
		self.app.master.title("Template app")
		#self.app.master.maxsize(800, 600)
		self.app.master.geometry('{}x{}'.format(800,600)) 
		self.app.master.protocol("WM_DELETE_WINDOW", self.close_win_handle)
		self.app.after(100, self.taskloop)
		self.app.mainloop()

	def set_win_name(self, winname):
		self.app.master.title(winname)

	def clear_view(self):
		for current_control in self.current_view_controls:
			obj = getattr(self.app.master, current_control)
			obj.destroy()
			obj = None
			delattr(self.app.master, current_control)

	def fill_view(self, view_id=None):
		if view_id != None:
			for control_id in self.viewlist[view_id]['controls'].keys():
				self.current_view_controls.append(control_id)
				if self.viewlist[view_id]['controls'][control_id]['ctl_type'] == 'button':
					obj = tk.Button(self.app.master, 
                            text=self.viewlist[view_id]['controls'][control_id]['text'], 
                            command=self.viewlist[view_id]['controls'][control_id]['action'], 
                            bg=self.viewlist[view_id]['controls'][control_id]['bgcolor'], 
                            fg=self.viewlist[view_id]['controls'][control_id]['fgcolor'])
				elif self.viewlist[view_id]['controls'][control_id]['ctl_type'] == 'label':
					obj = tk.Label(self.app.master, 
                            text=self.viewlist[view_id]['controls'][control_id]['text'],
                            bg=self.viewlist[view_id]['controls'][control_id]['bgcolor'],
                            fg=self.viewlist[view_id]['controls'][control_id]['fgcolor'],
                            height=self.viewlist[view_id]['controls'][control_id]['height'],
                            width=self.viewlist[view_id]['controls'][control_id]['width'])
				elif self.viewlist[view_id]['controls'][control_id]['ctl_type'] == 'image':
					obj = tk.Label(self.app.master,
                            image=self.viewlist[view_id]['controls'][control_id]['image'],
                            bg=self.viewlist[view_id]['controls'][control_id]['bgcolor'],
                            fg=self.viewlist[view_id]['controls'][control_id]['fgcolor'],
                            height=self.viewlist[view_id]['controls'][control_id]['height'],
                            width=self.viewlist[view_id]['controls'][control_id]['width'])
				setattr(self.app.master, control_id, obj)
				obj.place(x=self.viewlist[view_id]['controls'][control_id]['x'],
						y=self.viewlist[view_id]['controls'][control_id]['y'])

	def show_view(self, view_id=None):
		if view_id != None:
			self.current_view = view_id
			self.clear_view();
			self.app.master.geometry('{}x{}'.format(self.viewlist[view_id]['width'], self.viewlist[view_id]['height']))
			self.app.master.title(self.viewlist[view_id]['title'])
			self.fill_view(view_id)

	def create_view(self, view_id='view1', w=800, h=600, title='Window title'):
		if view_id not in self.viewlist:
			self.viewlist[view_id] = {'width': w, 'height': h, 'title':title, 'controls':{}}
		else:
			print("Error! View {} already exists!".format(view_id))

	def add_button(self, view_id='View', control_id='btn1', text='Btn', bgcolor='white', fgcolor='black', x = 0, y = 0, action = None):
		if view_id in self.viewlist:	
			if control_id not in self.viewlist[view_id]['controls']:
				self.viewlist[view_id]['controls'][control_id] = {'ctl_type':'button', 'text':text, 'bgcolor':bgcolor, 'fgcolor':fgcolor, 'x':x, 'y':y, 'action':action}
			else:
				print("Error! Button {} already exist in view {}".format(control_id, view_id))
		else:
			print("Error! View {} doesn't exist!".format(view_id))
			
	def add_label(self, view_id='View', control_id='lbl1', text='Label', bgcolor='white', fgcolor='black', w=10, h=10, x = 0, y = 0):		
		if view_id in self.viewlist:	
			if control_id not in self.viewlist[view_id]['controls']:
				self.viewlist[view_id]['controls'][control_id] = {'ctl_type':'label', 'text':text, 'bgcolor':bgcolor, 'fgcolor':fgcolor, 'width':w, 'height':h, 'x':x, 'y':y}
			else:
				print("Error! Label {} already exist in view {}".format(control_id, view_id))
		else:
			print("Error! View {} doesn't exist!".format(view_id))

	def add_image(self, view_id='View', control_id='img1', image=None, bgcolor='white', fgcolor='black', w=10, h=10, x = 0, y = 0):		
		if view_id in self.viewlist:	
			if control_id not in self.viewlist[view_id]['controls']:
				self.viewlist[view_id]['controls'][control_id] = {'ctl_type':'image', 'image':PhotoImage(file=image),'bgcolor':bgcolor, 'fgcolor':fgcolor, 'width':w, 'height':h, 'x':x, 'y':y}
			else:
				print("Error! Image {} already exist in view {}".format(control_id, view_id))
		else:
			print("Error! View {} doesn't exist!".format(view_id))
