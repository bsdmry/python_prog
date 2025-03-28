#!/usr/bin/env python3
import time
from wingamelib import WinGame

myapp = WinGame()
#myapp.runapp()
myapp.create_view(view_id="first", w=900,h=700,title="FIRST")
myapp.create_view(view_id="second", w=500,h=400,title="Second window")
myapp.add_button(view_id="first", control_id="bb", text="OK", bgcolor='red', x=100, y=100)
myapp.add_label(view_id="second", control_id="mylab", text="Label text", bgcolor='blue', x=200, y=150)
time.sleep(2)
print("Timeout!")
myapp.set_win_name("Hello")
time.sleep(2)
myapp.show_view("first")
time.sleep(2)
myapp.show_view("second")
