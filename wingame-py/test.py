#!/usr/bin/env python3
import time
from wingamelib import WinGame, WinGameSound


myapp = WinGame()
mysound = WinGameSound()
def show_m():
    myapp.show_modal_window("modv")

def step2second():
    myapp.show_window("second")

def do_music():
	mysound.play_once("track1")

def stop_music():
	mysound.stop_all()
	

#myapp.runapp()
mysound.add_record("lumberjack_m_44100_s16.wav", "track1")
mysound.add_record("EDGE - italohouse2-s16.wav", "track2")
myapp.create_window(window_id="first", w=900,h=700,title="FIRST")
myapp.create_window(window_id="second", w=500,h=400,title="Second window")
myapp.create_window(window_id="modv", w=200,h=100,title="Modal")
myapp.add_button(window_id="first", control_id="bb", text="OK", bgcolor='red', x=100, y=100, action=show_m)
myapp.add_button(window_id="first", control_id="nxtwin", text="Next", bgcolor='yellow', x=200, y=100, action=do_music)
myapp.add_button(window_id="first", control_id="shutup", text="Stop music", bgcolor='green', x=300, y=100, action=stop_music)
myapp.add_label(window_id="second", control_id="mylab", text="Label text", bgcolor='blue', x=200, y=150)
time.sleep(2)
mysound.play_loop("track2")
print("Timeout!")
myapp.set_win_name("Hello")
time.sleep(2)
myapp.show_window("first")
#time.sleep(2)
#myapp.show_modal_window("modv")
#myapp.show_window("second")
