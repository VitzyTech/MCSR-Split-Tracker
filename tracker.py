import pygame, json, sys, os, win32gui, win32con, win32api
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pygame.locals import *
pygame.init()

#import settings
def import_settings():
    with open("settings.json", "r") as f:
        settings = json.load(f)
    return settings

settings = import_settings()
log_path = os.path.join(settings["minecraft_directory"], "logs", "latest.log")

#define window
WIDTH = 150
HEIGHT = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT), NOFRAME)
FONT = pygame.font.Font("bpdots.squares-bold.otf", settings["costumize"]["font_size"])
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
transparency_color = (255, 0, 128)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparency_color), 0, win32con.LWA_COLORKEY)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
clock = pygame.time.Clock()

#split tracker function
split=None
def split_tracker(split, log_path):
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            return split
        line = lines[-1]
        if "Preparing spawn area" in line:
            split="OWERWORLD"
        if "made the advancement" in line:
            if "[We Need to Go Deeper]" in line:
                split="NETHER"
            elif "[Those Were the Days]" in line:
                split="BASTION"
            elif "[A Terrible Fortress]" in line:
                split="FORTRESS"
            elif "[Eye Spy]" in line:
                split="STRONGHOLD"
            elif "[The End?]" in line:
                split="END"
    return split

while True:
    settings = import_settings()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    split = split_tracker(split, log_path)
    split_text = FONT.render(split, True, "#000000")
    split_text_rect = split_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    
    screen.fill(transparency_color)
    screen.blit(split_text, split_text_rect)

    pygame.display.update()
    clock.tick(20)