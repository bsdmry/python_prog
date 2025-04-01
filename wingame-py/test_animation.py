#!/usr/bin/env python3
import time
from wingamelib import WinGame

pic1 = 'happy_130.png'
pic2 = 'sad_130.png'
myapp = WinGame()
def set_sad_face(p):
	print("Sad!")
	myapp.update_image(window_id="second", control_id="face", image=pic2)

def set_happy_face(p):
	print("Happy!")
	myapp.update_image(window_id="second", control_id="face", image=pic1)

time.sleep(2)
myapp.create_window(window_id="first", w=900,h=700,title="FIRST")
myapp.create_window(window_id="second", w=900,h=700,title="Second")
myapp.add_button(window_id="second", control_id="bb", text="OK", bgcolor='red', x=100, y=100)
myapp.add_image(window_id="second", control_id="face", image=pic1, bgcolor='white', onenter=set_sad_face, onleave=set_happy_face, w=130, h=130, x=310, y=310)
#myapp.add_image(window_id="second", control_id="face", image=pic1, bgcolor='white', w=130, h=130, x=310, y=310)
myapp.add_animation(window_id="second", control_id="my_anim", w=100, h=100, x=200, y=200, animation=[{'image':'red_sq.png', 'bgcolor':'white', 'fgcolor':'black'}, {'image':'yellow_sq.png', 'bgcolor':'white', 'fgcolor':'black'}, {'image':'green_sq.png', 'bgcolor':'white', 'fgcolor':'black'} ], frametime=5)
myapp.set_win_name("Hello")
myapp.show_window("first")
time.sleep(1)
myapp.show_window("second")
