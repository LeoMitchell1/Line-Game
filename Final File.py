from tkinter import *
import time
import random

win = Tk()
win.title("Line Game")
win.geometry('500x500')
win.resizable(False, False)

c = Canvas(win, width = 500, height = 500, bg='white')
c.pack()

while True:
    x = random.choice(range(0, 500))
    y = random.choice(range(0, 500))
    c.create_text(x, y, text = 'PENIS')
    win.update()
    time.sleep(.01)

win.mainloop()