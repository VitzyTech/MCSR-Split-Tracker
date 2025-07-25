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
minecraft_dir = os.path.join(settings["minecraft_directory"], "saves")

#sets the watchdog
class AdvancementHandler(FileSystemEventHandler):
    def __init__(self):
        self.player_advancements = {}
    def on_modified(self, event):        
        #Event path
        full_path = event.src_path.replace("\\", "/")
        
        #Check if is in advancments folder
        if "/advancements/" in full_path:
            #split the path
            parts = full_path.split("/")
            
            try:
                saves_index = parts.index("saves")
                world_name = parts[saves_index + 1]
            except (ValueError, IndexError):
                return
            
            advancements_dir = os.path.join(minecraft_dir, world_name, "advancements")
            
            #reads the advancments
            if os.path.exists(advancements_dir):
                for filename in os.listdir(advancements_dir):
                    if filename.endswith(".json"):
                        file_path = os.path.join(advancements_dir, filename)
                        with open(file_path, "r") as f:
                            self.player_advancements = json.load(f)
        return self.player_advancements

def start_watchdog():
    event_handler = AdvancementHandler()
    observer = Observer()
    observer.schedule(event_handler, minecraft_dir, recursive=True)
    observer.start()
    return event_handler

#split tracker
splits={
    "OWERWORLD":"minecraft:story/root",
    "NETHER":"minecraft:story/enter_the_nether",
    "BASTION":"minecraft:nether/find_bastion",
    "FORTRESS":"minecraft:nether/find_fortress",
    "STRONGHOLD":"minecraft:story/follow_ender_eye",
    "END":"minecraft:story/enter_the_end"
}
def split_tracker(player_advancements):
    latest_split = None
    for split_name, advancement_id in splits.items():
        if advancement_id in player_advancements:
            latest_split = split_name
    return latest_split

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

handler = start_watchdog()

while True:
    settings = import_settings()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    split = split_tracker(handler.player_advancements)
    if split is not None:
        split_text = FONT.render(split, True, "#000000")
    else:
        split_text = FONT.render("Offline", True, "#000000")
    
    screen.fill(transparency_color)
    screen.blit(split_text, (0, 0))

    pygame.display.update()
    clock.tick(1)