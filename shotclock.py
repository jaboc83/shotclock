from tkinter import *
from tkinter import ttk
import time
import pygame.mixer
from pygame.mixer import Sound

# Is the timer paused?
is_paused = True
# 24 second shotclock
max_clock = 24
# Light color default is Red
light = 'red'
# Dark color default is Black
dark = 'black'
# How many seconds left before flipping colors
time_running_out = 5

# Use red background and black text
def use_flipped_colors():
  global dark, light
  lbl.configure(background=light)
  root.configure(background=light)
  lbl.configure(foreground=dark)

# Use black background and red text
def use_normal_colors():
  global dark, light
  lbl.configure(background=dark)
  root.configure(background=dark)
  lbl.configure(foreground=light)

# Set the clock colors based on how much time is left
def set_clock_colors():
  global time_running_out
  # Invert the colors if it's the final seconds
  if int(timer.get()) <= time_running_out:
    use_flipped_colors()
  else:
    use_normal_colors()

# Move the clock forward or back one second
def adjust_clock(amount):
  timer.set(str(int(timer.get()) + amount).zfill(2))

# Run the clock
def countdown():
  global is_paused, buzzer
  one_second = 1000

  # Stop the clock
  if is_paused :
    return

  # Decrement the timer 1 second
  adjust_clock(-1)

  # Timer ran out
  if int(timer.get()) == 0:
    # Start flashing and pause the clock
    flash(True, 0)
    is_paused = True
    # Fire the buzzer
    pygame.mixer.music.play("/home/pi/src/python/shotclock/buzzer.mp3")
    return

  # Update the clock's colors
  set_clock_colors()

  # Wait 1 second then countdown again
  root.after(one_second, countdown)

# Flash the clock colors between normal and flipped
def flash(use_flipped, flashcount):
  flashcount += 1

  if use_flipped:
    use_flipped_colors()
  else:
    use_normal_colors()

  # Only flash 30 times
  if flashcount < 30:
    # Flash to opposite colors after 100 ms
    root.after(100, flash, not use_flipped, flashcount)

# Reset the clock to max time and pause
def reset(e):
  global max_clock
  global is_paused
  is_paused = True
  timer.set(str(max_clock))

# toggle the clock running/paused state
def toggle_clock(e):
  global is_paused
  if is_paused:
    is_paused = False
    root.after(500, countdown)
  else:
    is_paused = True

# Set the clock back one second
def increment_clock(e):
  global is_paused
  is_paused = True
  # Don't increment beyond clock maximum
  if int(timer.get()) < max_clock:
    adjust_clock(1)
  set_clock_colors()

# Move the clock forward one second
def decrement_clock(e):
  global is_paused
  is_paused = True
  # Don't decrement below 0
  if int(timer.get()) > 0:
    adjust_clock(-1)
  set_clock_colors()

# Initialize for sound
pygame.init()
pygame.mixer.init()
# buzzer sound
pygame.mixer.music.load("/home/pi/src/python/shotclock/buzzer.mp3")

# root UI element
root = Tk()
root.title("UnsignedBytes Shotclock")
root.attributes("-fullscreen", True)

# The clock's current time
timer = StringVar()

# Label to shot current clock time in big red letters
lbl = Label(root, textvariable=timer, width=2, height=1, font=("DS-Digital", 800))
lbl.pack()

# Reset the clock to max on Enter pressed
root.bind("<Return>", reset);
# Pause/Resume the clock on Space pressed
root.bind("<space>", toggle_clock);
# Increment the clock on up arrow pressed
root.bind("<Up>", increment_clock);
# Decrement the clock on down arrow pressed
root.bind("<Down>", decrement_clock);

# Set the clock to Max initially
reset(None)
# Start with the normal Color Scheme
use_normal_colors()

# Start the application
root.mainloop()
