import threading, time, sys
import tkinter as tk

from PIL import Image, ImageTk
from pynput.mouse import Button, Controller, Listener

root = tk.Tk()
mouse = Controller()

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
    position_label.config(text="Mouse Position: {}".format(mouse.position))
    update_time = 250
    root.after(update_time, lambda: updateMousePosition(position_label))

click_positions = []
# on a click event record the coordintes: [x,y]
# and append it to the click positions list
# at the end of the program, output the list
def on_click(x, y, button, pressed):
    if pressed and button == Button.left:
        return click_positions.append(mouse.position)

def main():
    setupTk()
    root.mainloop()

if __name__ == "__main__":
    with Listener(
        on_click=on_click) as listener:
        try:
            main()
            listener.join()
        except KeyboardInterrupt:
            print("User interrupted program.")
            print(click_positions)
            sys.exit(1)

