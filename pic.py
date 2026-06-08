import threading, time, sys
import tkinter as tk

from PIL import Image, ImageTk
from pynput.mouse import Button, Controller

root = tk.Tk()

''' Reposition the fretboard image (center if possible).
    Rewrite the ugly code.

'''

def setupTk():
    root.title("Fretboard")
    
    fretboard_image = Image.open("fretboard.png")
    tk_image = ImageTk.PhotoImage(fretboard_image)
    
    label = tk.Label(root, image=tk_image)
    label.image = tk_image
    label.pack(padx=100,pady=300)

    position_label = tk.Label(root, text="Mouse Position: ", font=("Arial", 14))
    position_label.pack()

    updateMousePosition(position_label)

def updateMousePosition(position_label):
    mouse = Controller()
    position_label.config(text="Mouse Position: {}".format(mouse.position))
    root.after(250, lambda: updateMousePosition(position_label)) # 500ms

def main():
    setupTk()
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("User interrupted program.")
        sys.exit(1)

