
import os, sys, pygame, math
from tkinter import filedialog
from tkinter import *

pygame.init()

size = width, height = 640, 480

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Purple Void Map Editor')

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
arial = pygame.font.SysFont('Segoe UI', 16)

def arial_text(text):
    global arial
    return arial.render(text, False, (255, 255, 255))

clock = pygame.time.Clock()

p_player = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/p_player_idle_r_0.bmp")), (128, 128))
p_portal = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/p_portal.bmp")), (64, 128))
p_box = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/p_box.bmp")), (64, 64))
g_player = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/g_player_idle_r_0.bmp")), (128, 128))
g_portal = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/g_portal.bmp")), (64, 128))
g_box = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/g_box.bmp")), (64, 64))
g_jumper = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/g_jumper.bmp")), (64, 64))
platform = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/platform.bmp")), (128, 16))
bouncy_platform = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/platform_bouncy.bmp")), (128, 16))
hidden_platform = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/platform_hidden.bmp")), (128, 16))
death_platform = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/platform_death.bmp")), (128, 16))
destroy_platform = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/platform_destroy.bmp")), (128, 16))
ascend_platform = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/platform_ascend.bmp")), (128, 16))
descend_platform = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/platform_descend.bmp")), (128, 16))
elevator_platform = pygame.transform.scale(pygame.image.load(os.path.abspath("../res/platform_elevator.bmp")), (128, 16))

p_images = {
    "player" : p_player,
    "portal" : p_portal,
    "box" : p_box,
    "platform" : platform,
    "bouncy_platform" : bouncy_platform,
    "hidden_platform" : hidden_platform,
    "death_platform" : death_platform,
    "destroy_platform" : destroy_platform,
    "ascend_platform" : ascend_platform,
    "descend_platform" : descend_platform,
    "elevator_platform" : elevator_platform,
    "jumper" : g_jumper,
}

g_images = {
    "player" : g_player,
    "portal" : g_portal,
    "box" : g_box,
    "platform" : platform,
    "bouncy_platform" : bouncy_platform,
    "hidden_platform" : hidden_platform,
    "death_platform" : death_platform,
    "destroy_platform" : destroy_platform,
    "ascend_platform" : ascend_platform,
    "descend_platform" : descend_platform,
    "elevator_platform" : elevator_platform,
    "jumper" : g_jumper,
}

editor_x = -320
editor_y = -240

menus = [arial_text("File"), arial_text("Objects"), arial_text("Actions"), arial_text("Themes")]
menu_bounds = []
draw_grid = True
dropdown = -1

all_objects = ["player", "portal", "box", "platform", "bouncy_platform", "hidden_platform",
    "death_platform", "destroy_platform", "ascend_platform", "descend_platform", "elevator_platform", "jumper"]
placing = "box"

objects = [] # ((0, 0), "box")

purple_theme = ((205, 0, 204), (255, 128, 255), p_images)
green_theme = ((50, 164, 50), (50, 192, 50), g_images)
themes = [("purple", purple_theme), ("green", green_theme)]
theme = themes[0]

def theme_from_name(name):
    global themes
    for i in range(0, len(themes)):
        if themes[i][0] == name:
            return themes[i]
    return None

def save_objects():
    global objects
    root = Tk()
    filename = filedialog.asksaveasfilename(filetypes=(("Map Text File", ".txt"), ("All Files", "*.*")))
    root.destroy()
    if filename == "": return
    file = open(filename, "w")
    file.write("theme %s\n" % theme[0])
    for i in range(0, len(objects)):
        file.write("%s @ %d %d\n" % (objects[i][1], objects[i][0][0], objects[i][0][1]))
    file.close()

def load_objects():
    global objects, theme, themes
    root = Tk()
    filename = filedialog.askopenfilename(filetypes=(("Map Text File", ".txt"), ("All Files", "*.*")))
    root.destroy()
    if filename == "": return
    file = open(filename, "r")
    del objects[:]
    theme = themes[0]
    for line in file:
        if line.startswith("theme "):
            theme_text, theme_name = line.split()
            theme = theme_from_name(theme_name)
            continue
        id, at, x, y = line.split()
        objects.append(((float(x), float(y)), id))
    file.close()

def place_object():
    global objects, all_objects, placing
    tx, ty = math.floor((mouse_pos[0] + editor_x) / 32), math.floor((mouse_pos[1] + editor_y) / 32)
    objects.append(((tx * 32, ty * 32), placing))

def delete_object():
    global objects
    for i in range(0, len(objects)):
        if objects[i][0][0] == math.floor((mouse_pos[0] + editor_x) / 32) * 32 and objects[i][0][1] == math.floor((mouse_pos[1] + editor_y) / 32) * 32:
            del objects[i]
            return

menu_bounds_offset = 4
for i in range(0, len(menus)):
    menu_button_width = menus[i].get_width() + 8
    menu_bounds.append((menu_bounds_offset, menu_bounds_offset + menu_button_width))
    menu_bounds_offset += menu_button_width + 4

def show_file_menu():
    global dropdown
    dropdown = 0

def show_objects_menu():
    global dropdown
    dropdown = 1

def show_actions_menu():
    global dropdown
    dropdown = 2

def show_themes_menu():
    global dropdown
    dropdown = 3

def toggle_grid():
    global draw_grid
    draw_grid = not draw_grid

menu_actions = [show_file_menu, show_objects_menu, show_actions_menu, show_themes_menu]

file_dropdown = [arial_text("Open"), arial_text("Save"), arial_text("Quit")]
def file_dropdown_actions(index):
    if index == 0: load_objects()
    if index == 1: save_objects()
    if index == 2: exit(0)

objects_dropdown = [arial_text("player"), arial_text("portal"), arial_text("box"), arial_text("platform"),
    arial_text("bouncy platform"), arial_text("hidden platform"), arial_text("death platform"), arial_text("destroy platform"),
    arial_text("ascending platform"), arial_text("descending platform"), arial_text("elevator platform"), arial_text("jumper")]
def objects_dropdown_actions(index):
    global placing, all_objects
    if(index >= 0 and index < len(all_objects)):
        placing = all_objects[index]
    return

actions_dropdown = [arial_text("Toggle Grid")]
def actions_dropdown_actions(index):
    if index == 0: toggle_grid()

themes_dropdown = [arial_text("Purple Theme"), arial_text("Green Theme")]
def themes_dropdown_actions(index):
    global theme, themes
    theme = themes[index]

dropdown_menus = [file_dropdown, objects_dropdown, actions_dropdown, themes_dropdown]
dropdown_menu_actions = [file_dropdown_actions, objects_dropdown_actions, actions_dropdown_actions, themes_dropdown_actions]
dropdown_menu_heights = []

obj_hotkeys = [(pygame.K_e, "platform"), (pygame.K_b, "bouncy_platform"), (pygame.K_x, "box"),
    (pygame.K_j, "jumper"), (pygame.K_l, "ascend_platform"), (pygame.K_m, "descend_platform"), (pygame.K_p, "portal"),
    (pygame.K_h, "hidden_platform"), (pygame.K_z, "destroy_platform"), (pygame.K_k, "death_platform"), (pygame.K_v, "elevator_platform")]

menu_hotkeys = [(pygame.K_o, 0, 0), (pygame.K_s, 0, 1), (pygame.K_q, 0, 2)]

for i in range(0, len(dropdown_menus)):
    if(dropdown_menus[i] == None):
        dropdown_menu_heights.append(8)
        continue
    total_height = 0
    for j in range(0, len(dropdown_menus[i])):
        total_height += 24
    dropdown_menu_heights.append(total_height)

while 1:
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width = event.w
            height = event.h
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                draw_grid = not draw_grid
            if keys[pygame.K_LCTRL]:
                for i in range(0, len(menu_hotkeys)):
                    if event.key == menu_hotkeys[i][0]:
                        dropdown_menu_actions[menu_hotkeys[i][1]](menu_hotkeys[i][2])
                        break
            else:
                for i in range(0, len(obj_hotkeys)):
                    if event.key == obj_hotkeys[i][0]:
                        placing = obj_hotkeys[i][1]
                        break
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if mouse_pos[1] <= 24:
                for i in range(0, len(menu_bounds)):
                    if mouse_pos[0] >= menu_bounds[i][0] and mouse_pos[0] <= menu_bounds[i][1]:
                        menu_actions[i]()
                        break
            elif dropdown != -1 and mouse_pos[0] >= menu_bounds[dropdown][0] - 4 and mouse_pos[0] <= menu_bounds[dropdown][0] - 4 + 164:
                item_index = math.floor((mouse_pos[1] - 24) / 24)
                if item_index >= 0 and item_index < len(dropdown_menus[dropdown]):
                    dropdown_menu_actions[dropdown](item_index)
                dropdown = -1
            elif dropdown == -1:
                place_object()
            else:
                dropdown = -1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            delete_object()

    dt = clock.tick(60)
    if keys[pygame.K_d]: editor_x += 0.3 * dt
    if keys[pygame.K_a]: editor_x -= 0.3 * dt
    if keys[pygame.K_s]: editor_y += 0.3 * dt
    if keys[pygame.K_w]: editor_y -= 0.3 * dt

    screen.fill(theme[1][0])

    if draw_grid:
        diff = math.floor(editor_x) % 32
        for i in range(0, math.ceil(width / 32) + 1):
            pygame.draw.line(screen, theme[1][1], (32 * i - diff, 0), (32 * i - diff, height))

        diff = math.floor(editor_y) % 32
        for i in range(0, math.ceil(height / 32) + 1):
            pygame.draw.line(screen, theme[1][1], (0, 32 * i - diff), (width, 32 * i - diff))

    for i in range(0, len(objects)):
        screen.blit(theme[1][2][objects[i][1]], (objects[i][0][0] - editor_x, objects[i][0][1] - editor_y))

    pygame.draw.rect(screen, (192, 192, 192, 255), (0, 0, width, 24))

    menu_offset = 8
    for i in range(0, len(menus)):
        screen.blit(menus[i], (menu_offset, 0))
        menu_offset += menus[i].get_width() + 8

    if dropdown != -1:
        pygame.draw.rect(screen, (192, 192, 192, 255), (menu_bounds[dropdown][0] - 4, 24, 164, dropdown_menu_heights[dropdown]))
        if dropdown_menus[dropdown] != None:
            item_y = 24
            for i in range(0, len(dropdown_menus[dropdown])):
                screen.blit(dropdown_menus[dropdown][i], (menu_bounds[dropdown][0], item_y))
                item_y += dropdown_menus[dropdown][i].get_height()

    pygame.draw.rect(screen, (192, 192, 192, 255), (0, height - 24, width, height))
    tx, ty = math.floor((mouse_pos[0] + editor_x) / 32), math.floor((mouse_pos[1] + editor_y) / 32)
    screen.blit(arial.render('(%s, %s) - placing: %s' % (tx, ty, placing), False, (0, 0, 0)), (4, height - 24))
    pygame.display.flip()
