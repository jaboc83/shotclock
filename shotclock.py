from tkinter import *
from tkinter import ttk
import time

toggle = True
pause = True
flashcount = 0

def setColors():
	if int(timer.get()) <= 5 :
		lbl.configure(background='red')
		root.configure(background='red')
		lbl.configure(foreground='black')
	else:
		lbl.configure(background='black')
		root.configure(background='black')
		lbl.configure(foreground='red')


def decrement_label():
	global pause
	if pause :
		return

	timer.set(str(int(timer.get()) - 1).zfill(2))

	if timer.get() == "00":
		flash()
		return

	setColors()

	root.after(1000, decrement_label)

def flash():
	global toggle
	global flashcount
	flashcount += 1
	if toggle:	
		root.configure(background='red')
		lbl.configure(background='red')
		lbl.configure(foreground='black')
	else:
		root.configure(background='black')
		lbl.configure(background='black')
		lbl.configure(foreground='red')
	toggle = not toggle
	if flashcount < 30:
		root.after(100, flash)
	else:
		pause = True
		flashcount = 0
	
def reset(e):
	timer.set("24")

def pauseResume(e):
	global pause
	if pause:
		pause = False
		root.after(500, decrement_label)
	else:
		pause = True

def increment(e):
	global pause
	pause = True
	timer.set(str(int(timer.get()) + 1).zfill(2))
	setColors()

def decrement(e):
	global pause
	pause = True
	if int(timer.get()) > 0:
		timer.set(str(int(timer.get()) - 1).zfill(2))
	setColors()

root = Tk()
#w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#root.geometry("%dx%d+0+0" % (w, h))
root.title("Minnesota Rangers Shotclock")
root.configure(background='black')
root.attributes("-fullscreen", True)

timer = StringVar() 

lbl = Label(root, textvariable=timer, width=2, height=1, fg="red", bg="black", font=("DS-Digital", 800))
lbl.pack(side="top")

root.bind("<Return>", reset);
root.bind("<space>", pauseResume);
root.bind("<Up>", increment);
root.bind("<Down>", decrement);

reset(None)
root.mainloop()

