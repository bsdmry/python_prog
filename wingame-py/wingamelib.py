#!/usr/bin/env python3
import tkinter as tk
import threading
import pyaudio
import wave
import time
from tkinter import PhotoImage

class WinGameSound():
	def __init__(self):
		self.records = {}         # identifier -> filename
		self.threads = {}         # identifier -> thread
		self.stop_flags = {}      # identifier -> threading.Event
		self.pyaudio_instance = pyaudio.PyAudio()

	def add_record(self, filename: str, identifier: str):
		self.records[identifier] = filename

	def play_once(self, identifier: str):
		def _play():
			self._play_wave_file(self.records[identifier])

		self._start_thread(identifier, _play)

	def play_loop(self, identifier: str):
		stop_event = threading.Event()
		self.stop_flags[identifier] = stop_event

		def _loop():
			while not stop_event.is_set():
				self._play_wave_file(self.records[identifier], stop_event)
		self._start_thread(identifier, _loop)

	def stop(self, identifier: str):
		if identifier in self.stop_flags:
			self.stop_flags[identifier].set()
		if identifier in self.threads:
			self.threads[identifier].join()
			del self.threads[identifier]
		if identifier in self.stop_flags:
			del self.stop_flags[identifier]

	def stop_all(self):
		for identifier in list(self.threads.keys()):
			self.stop(identifier)

	def _start_thread(self, identifier: str, target_func):
		if identifier in self.threads:
			self.stop(identifier)
		thread = threading.Thread(target=target_func, daemon=True)
		self.threads[identifier] = thread
		thread.start()

	def _play_wave_file(self, filename: str, stop_event: threading.Event = None):
		wf = wave.open(filename, 'rb')
		stream = self.pyaudio_instance.open(
            format=self.pyaudio_instance.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

		chunk_size = 2048
		data = wf.readframes(chunk_size)
		while data and (stop_event is None or not stop_event.is_set()):
			stream.write(data)
			data = wf.readframes(chunk_size)

		stream.stop_stream()
		stream.close()
		wf.close()

	def __del__(self):
		self.stop_all()
		self.pyaudio_instance.terminate()

class WinGame(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.start()
	# repeating actions for the current window (like animations)
	def taskloop(self): 
		if (len(self.tasks.keys()) > 0):
			for control_id in self.tasks:
				if self.tasks[control_id]['ctl_type'] == 'animation':
					if self.tasks[control_id]['frametimeout'] == self.tasks[control_id]['frametime']:
						self.tasks[control_id]['frametimeout'] = 0
						if  self.tasks[control_id]['current_frame'] ==  self.tasks[control_id]['framecount'] - 1:
							self.tasks[control_id]['current_frame'] = 0
						else:
							self.tasks[control_id]['current_frame'] = self.tasks[control_id]['current_frame'] + 1
						index =  self.tasks[control_id]['current_frame']
						getattr(self.app.master, control_id).config(
								bg=self.windowlist[self.current_window]['controls'][control_id]['animation'][index]['bgcolor'],
								fg=self.windowlist[self.current_window]['controls'][control_id]['animation'][index]['fgcolor'],
								image=self.windowlist[self.current_window]['controls'][control_id]['animation'][index]['image']
								)
					else:
						self.tasks[control_id]['frametimeout'] = self.tasks[control_id]['frametimeout'] + 1

		self.app.after(100, self.taskloop)

	def close_win_handle(self):
		self.app.quit()

	def run(self):
		self.windowlist = {};
		self.current_window = None # keeps current active window id
		self.current_window_controls = [] # keeps control ids of the current window
		self.tasks = {} # keeps control ids for regular actions on a current window
		self.app = tk.Frame(master = None)
		self.app.master.title("Template app")
		self.app.modal = None
		#self.app.master.maxsize(800, 600)
		self.app.master.geometry('{}x{}'.format(800,600)) 
		self.app.master.protocol("WM_DELETE_WINDOW", self.close_win_handle)
		self.app.after(100, self.taskloop)
		self.app.mainloop()

	def set_win_name(self, winname):
		self.app.master.title(winname)
	
	# Removes controls from the window 
	def clear_window(self):
		for current_control in self.current_window_controls:
			if current_control in self.tasks.keys(): #if regular task for the control exist
				del self.tasks[current_control]	#delete this task
			obj = getattr(self.app.master, current_control) #get Tkinter control object
			obj.destroy() # remove control from window
			obj = None 
			delattr(self.app.master, current_control) # delete attribute object

	# Creates controls on the window, according to the configuration object 
	def fill_window(self, window_id=None):
		if window_id != None:
			for control_id in self.windowlist[window_id]['controls'].keys():
				self.current_window_controls.append(control_id)
				if self.windowlist[window_id]['controls'][control_id]['ctl_type'] == 'button':
					obj = tk.Button(self.app.master, 
                            text=self.windowlist[window_id]['controls'][control_id]['text'], 
                            command=self.windowlist[window_id]['controls'][control_id]['action'], 
                            bg=self.windowlist[window_id]['controls'][control_id]['bgcolor'], 
                            fg=self.windowlist[window_id]['controls'][control_id]['fgcolor'])
				elif self.windowlist[window_id]['controls'][control_id]['ctl_type'] == 'label':
					obj = tk.Label(self.app.master, 
                            text=self.windowlist[window_id]['controls'][control_id]['text'],
                            bg=self.windowlist[window_id]['controls'][control_id]['bgcolor'],
                            fg=self.windowlist[window_id]['controls'][control_id]['fgcolor'],
                            height=self.windowlist[window_id]['controls'][control_id]['height'],
                            width=self.windowlist[window_id]['controls'][control_id]['width'])
				elif self.windowlist[window_id]['controls'][control_id]['ctl_type'] == 'image':
					obj = tk.Label(self.app.master,
                            image=self.windowlist[window_id]['controls'][control_id]['image'],
                            bg=self.windowlist[window_id]['controls'][control_id]['bgcolor'],
                            fg=self.windowlist[window_id]['controls'][control_id]['fgcolor'],
                            height=self.windowlist[window_id]['controls'][control_id]['height'],
                            width=self.windowlist[window_id]['controls'][control_id]['width'])
				elif self.windowlist[window_id]['controls'][control_id]['ctl_type'] == 'animation':
					obj = tk.Label(self.app.master,
                            image=self.windowlist[window_id]['controls'][control_id]['animation'][0]['image'],
                            bg=self.windowlist[window_id]['controls'][control_id]['animation'][0]['bgcolor'],
                            fg=self.windowlist[window_id]['controls'][control_id]['animation'][0]['fgcolor'],
                            height=self.windowlist[window_id]['controls'][control_id]['height'],
                            width=self.windowlist[window_id]['controls'][control_id]['width'])
					if control_id not in self.tasks:
						self.tasks[control_id] = {}
					self.tasks[control_id]['ctl_type'] = 'animation'
					self.tasks[control_id]['playtype'] = self.windowlist[window_id]['controls'][control_id]['playtype']
					self.tasks[control_id]['frametimeout'] = 0 #counter for frame time
					self.tasks[control_id]['frametime'] = 5 #frame time in frame units
					self.tasks[control_id]['framecount'] = len(self.windowlist[window_id]['controls'][control_id]['animation'])
					self.tasks[control_id]['current_frame'] = 0
				setattr(self.app.master, control_id, obj)
				obj.place(x=self.windowlist[window_id]['controls'][control_id]['x'],
						y=self.windowlist[window_id]['controls'][control_id]['y'])

	# Changes the main window
	def show_window(self, window_id=None):
		if window_id != None:
			self.current_window = window_id
			self.clear_window()
			self.app.master.geometry('{}x{}'.format(self.windowlist[window_id]['width'], self.windowlist[window_id]['height']))
			self.app.master.title(self.windowlist[window_id]['title'])
			self.fill_window(window_id)

	def show_modal_window(self, modal_window_id=None):
		self.app.modal = tk.Toplevel()
		self.app.modal.title(self.windowlist[modal_window_id]['title'])
		self.app.config(width=self.windowlist[modal_window_id]['width'], height=self.windowlist[modal_window_id]['height'])
		self.app.modal.focus()
		self.app.modal.grab_set()

	# Creates a configuration for a window
	def create_window(self, window_id='window1', w=800, h=600, title='Window title'):
		if window_id not in self.windowlist:
			self.windowlist[window_id] = {'width': w, 'height': h, 'title':title, 'controls':{}}
		else:
			print("Error! View {} already exists!".format(window_id))
	# Adds a button configuration into a window configuration
	def add_button(self, window_id='View', control_id='btn1', text='Btn', bgcolor='white', fgcolor='black', x = 0, y = 0, action = None):
		if window_id in self.windowlist:	
			if control_id not in self.windowlist[window_id]['controls']:
				self.windowlist[window_id]['controls'][control_id] = {'ctl_type':'button', 'text':text, 'bgcolor':bgcolor, 'fgcolor':fgcolor, 'x':x, 'y':y, 'action':action}
			else:
				print("Error! Button {} already exist in window {}".format(control_id, window_id))
		else:
			print("Error! View {} doesn't exist!".format(window_id))
			
	def add_label(self, window_id='View', control_id='lbl1', text='Label', bgcolor='white', fgcolor='black', w=10, h=10, x = 0, y = 0):		
		if window_id in self.windowlist:	
			if control_id not in self.windowlist[window_id]['controls']:
				self.windowlist[window_id]['controls'][control_id] = {'ctl_type':'label', 'text':text, 'bgcolor':bgcolor, 'fgcolor':fgcolor, 'width':w, 'height':h, 'x':x, 'y':y}
			else:
				print("Error! Label {} already exist in window {}".format(control_id, window_id))
		else:
			print("Error! View {} doesn't exist!".format(window_id))

	def add_image(self, window_id='View', control_id='img1', image=None, bgcolor='white', fgcolor='black', onclick=None, onenter=None, onleave=None, w=10, h=10, x = 0, y = 0):		
		if window_id in self.windowlist:	
			if control_id not in self.windowlist[window_id]['controls']:
				self.windowlist[window_id]['controls'][control_id] = {'ctl_type':'image', 'image':PhotoImage(file=image),'bgcolor':bgcolor, 'fgcolor':fgcolor, 'width':w, 'height':h, 'x':x, 'y':y}
			else:
				print("Error! Image {} already exist in window {}".format(control_id, window_id))
		else:
			print("Error! View {} doesn't exist!".format(window_id))

	def add_animation(self, window_id='View', control_id='animation1', animation=[{'image':None, 'bgcolor':'white', 'fgcolor':'black'}], playtype='play_loop', frametime=5,  w=10, h=10, x = 0, y = 0):		
		if window_id in self.windowlist:	
			if control_id not in self.windowlist[window_id]['controls']:
				self.windowlist[window_id]['controls'][control_id] = {'ctl_type':'animation', 'playtype':playtype, 'frametime':frametime, 'animation':[], 'width':w, 'height':h, 'x':x, 'y':y}
				for a in animation:
					im = a['image']
					fg = a['fgcolor']
					bg = a['bgcolor']
					self.windowlist[window_id]['controls'][control_id]['animation'].append({'image':PhotoImage(file=im), 'bgcolor':bg, 'fgcolor':fg})
			else:
				print("Error! Animation {} already exist in window {}".format(control_id, window_id))
		else:
			print("Error! View {} doesn't exist!".format(window_id))
