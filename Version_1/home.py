import pickle
import time
import ctypes
from tkinter import *
import tkinter.colorchooser
import random
tk = Tk()
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
# Variables
blockSize = 10
background = canvas.create_rectangle(0, 0, 600, 600, fill="pink", outline="pink")
# Functions
class Game:
    def __init__(self, tk, canvas):
        self.user_Id = canvas.create_oval(0, 0, 10, 10, fill="black")
        self.tk = tk
        self.canvas = canvas
        self.canvasArray = []
        
    def update(self):
        self.tk.update_idletasks()
        self.tk.update()


    def move_left(self, event):
        self.canvas.move(self.user_Id, -10, 0)

    def move_right(self, event):
        self.canvas.move(self.user_Id, 10, 0)

    def move_up(self, event):
        self.canvas.move(self.user_Id, 0, -10)

    def move_down(self, event):
        self.canvas.move(self.user_Id, 0, 10)
    

    def add_previous_blocks(self, array):
        for x in array:
            position = x["pos"]
            color = x["color"]
            if x["type"] == "rectangle":
                canvas.create_rectangle(position[0], position[1], position[2], position[3], fill=color, outline="", tags="added")
            elif x["type"] == "circle":
                canvas.create_oval(position[0], position[1], position[2], position[3], fill=color, outline="", tags="added")
            self.canvasArray.append(x)

    def create_block(self, event):
        pos = self.canvas.coords(self.user_Id)
        color = tkinter.colorchooser.askcolor()
        currentBlock = {}
        currentBlock["ID"] = self.canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill=color[1], outline="", tags="added")
        currentBlock["pos"] = pos
        currentBlock["color"] = color[1]
        currentBlock["type"] = "rectangle"
        self.canvasArray.append(currentBlock)

    def create_circle(self, event):
        pos = self.canvas.coords(self.user_Id)
        color = tkinter.colorchooser.askcolor()
        currentCircle = {}
        currentCircle["ID"] = self.canvas.create_oval(pos[0], pos[1], pos[2], pos[3], fill=color[1], outline="", tags="added")
        currentCircle["pos"] = pos
        currentCircle["color"] = color[1]
        currentCircle["type"] = "circle"
        self.canvasArray.append(currentCircle)
        
    def save(self, event):
        file = open("gameData.dat", 'wb')
        pickle.dump(self.canvasArray, file)
        file.close()

    def destroy(self):
        self.canvas.delete("added")
        self.update()
        self.canvasArray = []
        file = open("gameData.dat", 'wb')
        pickle.dump(self.canvasArray, file)
        file.close()
        Msg = Label(tk, text="Deleting... Please wait while we remove the save data...")
        Msg.pack()
        self.update()
        time.sleep(3)
        Msg.pack_forget()
        self.update()
        ctypes.windll.user32.MessageBoxW(0, "Successfully deleted... Game has been restarted", "Save data deleted", 0)
    
    def reset(self, event):
        x = ctypes.windll.user32.MessageBoxW(0, "WARNING! This will delete everything.  Are you sure you want to do this?", "Delete save data?", 4)
        if x == 6:
            self.destroy()
        elif x == 7:
            return
def setup():
    try:
        file = open("gameData.dat", 'rb')
        loaded_game_data = pickle.load(file)
        file.close()
        g.add_previous_blocks(loaded_game_data)
        print("World initialized.  Commands:")
        print("Up arrow to go up")
        print("Down arrow to go down")
        print("Left arrow to go left")
        print("Right arrow to go right")
        print("Press 'b' to create a block")
        print("Press 's' to save")
        print("Press 'r' to reset everything")
        print("Press 'c' to create a circle")
        del loaded_game_data
    except:
        print("Could not load save data.  Initializing virtual world... Please wait...")
        todo = ctypes.windll.user32.MessageBoxW(0, "Cannot load save data.  What to do?", "Request denied", 2)
        if todo == 3:
            while True:
                exit()
        elif todo == 4:
            setup()
            return
        elif todo == 5:
            print("World initialized.  Commands:")
            print("Up arrow to go up")
            print("Down arrow to go down")
            print("Left arrow to go left")
            print("Right arrow to go right")
            print("Press 'b' to create a block")
            print("Press 's' to save")
            print("Press 'r' to reset everything")
            print("Press 'c' to create a circle")
            return
# Program
g = Game(tk, canvas)
setup()
g.update()
canvas.bind_all('<KeyPress-Up>', g.move_up)
canvas.bind_all('<KeyPress-Down>', g.move_down)
canvas.bind_all('<KeyPress-Left>', g.move_left)
canvas.bind_all('<KeyPress-Right>', g.move_right)
canvas.bind_all('b', g.create_block)
canvas.bind_all('s', g.save)
canvas.bind_all('r', g.reset)
canvas.bind_all('c', g.create_circle)
while True:
    v = random.randint(0, 1000)
    g.update()
