#!/usr/bin/env python3
import time
from wingamelib import WinGame, WinGameSound

myapp = WinGame()
mysound = WinGameSound()
time.sleep(1)

def do_sound():
	mysound.play_once("track1")

def do_music():
	if mysound.is_playing("track2"):
		mysound.stop("track2")
	else:
		mysound.play_loop("track2")

mysound.add_record("lumberjack_m_44100_s16.wav", "track1")
mysound.add_record("EDGE - italohouse2-s16.wav", "track2")
myapp.create_window(window_id="first", w=400,h=400,title="Music test")
myapp.add_button(window_id="first", control_id="play", text="Sound!", bgcolor='red', x=100, y=100, action=do_sound)
myapp.add_button(window_id="first", control_id="background", text="Background", bgcolor='yellow', x=200, y=100, action=do_music)
myapp.show_window("first")
mysound.play_loop("track2")
