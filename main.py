import pygame, sys, json, tkinter, button, subprocess
from pygame.locals import *
from tkinter import filedialog
pygame.init()

#json files
def settings_import():
    with open("settings.json", "r") as f:
        settings=json.load(f)
    return settings
def settings_write():
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)
settings = settings_import()

#screen definition
WIDTH = 600
HEIGHT = 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#buttons definition
FONT = pygame.font.Font("bpdots.squares-bold.otf", 20)
select_dir = button.Button(image=None, pos=(300, 50), text_input="Select directory", font=FONT, base_color="#000000", hovering_color="#292929")
launchB = button.Button(image=None, pos=(300, 100), text_input="Launch Tracker", font=FONT, base_color="#000000", hovering_color="#292929")

#select directory function
def directory_selector():
    root = tkinter.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title="Select a directory")
    return path.replace("\\", "/")

#tracker launch function
def launch_tracker():
    tracker_process = subprocess.Popen(["tracker.py"], creationflags=subprocess.CREATE_NO_WINDOW)
    return tracker_process

while True:
    MOUSE_POS=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if select_dir.checkForInput(MOUSE_POS):
                    settings["minecraft_directory"]=directory_selector()
                    settings_write()
                if launchB.checkForInput(MOUSE_POS):
                    launch_tracker()

    screen.fill("#FFFFFF")
    select_dir.changeColor(MOUSE_POS)
    select_dir.update(screen)
    launchB.changeColor(MOUSE_POS)
    launchB.update(screen)

    pygame.display.update()