import math
import pygame
import tkinter as tk
from tkinter import filedialog

WWIDTH, WHEIGHT = (1920, 1000)
WMP, HMP = WHEIGHT / 2, WHEIGHT / 2 # This is the midpoint of the screen

WIN = pygame.display.set_mode((WWIDTH, WHEIGHT))

rtime = 0 # Time since the render started.
fps = 999

currentModel = None
pause = False
modelSize = 2000
ZOOM_THROTTLE = 6
verts = []

mdown = False

x_offset = 0
y_offset = 0

window = tk.Tk()
window.title("Config")
window.geometry("300x400")

def open_configuration_window():
    tk.Label(window, text="\n▀▄▀▄▀▄▀▄ INFO ▀▄▀▄▀▄▀▄\n").pack()

    global pausebutton
    global applybutton
    global fpsField

    tk.Label(window, text="\n▀▄▀▄▀▄▀▄ TOGGLES ▀▄▀▄▀▄▀▄\n").pack()

    pausebutton = tk.Button(window, text="PAUSE", command=pause_render)
    pausebutton.pack()

    tk.Label(window, text="\n▀▄▀▄▀▄▀▄ VALUES ▀▄▀▄▀▄▀▄\n").pack()

    tk.Label(window, text="UPDATE RATE").pack()
    fpsField = tk.Entry(window, width=35)
    #window.overrideredirect(True)
    fpsField.pack()

    tk.Label(window, text="\n▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n").pack()

    applybutton = tk.Button(window, text="APPLY CONFIGURATION", command=apply_settings)
    applybutton.pack()

    window.after(1, main)
    window.attributes("-topmost", True)
    window.mainloop()

# Functions

def apply_settings():
    global fps
    fps = int(fpsField.get())

def pause_render():
    global pause
    global pausebutton
    global rtime

    pausebutton['text'] = pause == False and "RESET" or "PAUSE"
    
    pause = not pause
    #rtime = 0

# Prompt the user to open a file, and set this as the target file for the program.
def init():
    global currentModel

    currentModel = filedialog.askopenfilename()
    pygame.display.set_caption('PyRender — ' + currentModel)
    
    build_mesh()
    open_configuration_window()

# This will parse and update the mesh once; use this for viewing a mesh without using unnecessary amounts
# of resources.
def build_mesh():
    global verts
    verts = parse_obj(currentModel)
    update_mesh()

def parse_obj(path):
    file = open(path, 'r') # open given file
    lines = file.readlines()
    coordList = [] # coordinates will be stored here

    for line in lines:
        if (line.startswith('v ')): # is this a line that holds a vertex location?
            rawcoord = line.partition('v ')[2]
            coordsplit = rawcoord.split(' ')
            coord = (-float(coordsplit[0]), -float(coordsplit[1]), float(coordsplit[2]))

            coordList.append(coord)
    
    coordList.sort() # (,reverse=True)
    return coordList
    
def update_mesh():
    global x_offset
    global y_offset
    global color

    WIN.fill((0, 0, 0))

    for x in range(50):
        mult = 4
        pygame.draw.rect(WIN, (0, 0, x*mult), pygame.Rect(0, x * 20, 1920, 20))

    # faggot mode
    # for x in range(50):
    #     pygame.draw.rect(WIN, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), pygame.Rect(0, x * 20, 1920, 20))
      
    for x in range(len(verts)):
        x_offset = 444 + verts[x][2] / 8 * math.sin(rtime / 32) * modelSize
        y_offset = 444 + verts[x][2] / 8 * math.cos(rtime / 32) * modelSize
        
        #dist_size = .01 + verts[x][2] > 1 and 3 + verts[x][2] or 1
        dist_size = 1.5 + (verts[x][2] / 8)
        dist_shade = verts[x][2] > 0 and 255 - verts[x][2] * 1666 or 255

        POS = (WMP + x_offset + verts[x][0] * modelSize, HMP + y_offset + verts[x][1] * modelSize)
        #     next_vert = x < (len(verts) - 1) and (verts[x + 1]) or (0, 0)
        #     pygame.draw.line(WIN, (255, 0, 0), POS, (WMP + x_offset + next_vert[0] * modelSize, WMP + x_offset + next_vert[1] * modelSize))
        pygame.draw.circle(WIN, (dist_shade, dist_shade, dist_shade), POS, dist_size)
    
    pygame.display.update()

def main():
    clock = pygame.time.Clock()

    global rtime
    global mdown
    global fps

    clock.tick(fps)
    rtime += 1

    if (not pause):
        update_mesh()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            window.quit()
        elif event.type == pygame.MOUSEWHEEL:
            global modelSize

            modelSize += event.y * modelSize / ZOOM_THROTTLE
        elif event.type == pygame.MOUSEBUTTONDOWN:
                mdown = True

        elif event.type == pygame.MOUSEBUTTONUP:
                mdown = False

    window.after(1, main)


init()