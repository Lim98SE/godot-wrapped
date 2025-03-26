# yeah the code's probably horrible lol
# when posting pls tag @lim95.com on bluesky !!
# also follow me and check out my game Green Guy Goes Grappling

# requires pygame-ce (not regular pygame)
# font.ttf should be jetbrains mono regular
# just do python3/py main.py [path to your game folder here (the one with project.godot)]

# mine for example (CLI)

# Total lines: 4198
# Biggest file: GGGG/Source/manager.gd (696 lines)
# Tool scripts: 9 | Process scripts: 106
# ====================================================================================================================================================================
# 578 variables (165 were explicitly typed, so 29%)
# 85 @export calls
# 62 connected signals (out of 5 defined)
# ====================================================================================================================================================================
# Scenes (*.tscn): 92
# Assets (*.tres): 46
# ====================================================================================================================================================================
# Your top 3 most used file formats:
# #1: png (183)
# #2: gd (142)
# #3: tscn (92)

import os
import pygame
import sys

try:
    sys.argv[1]

except IndexError:
    print("supply a directory on the command line doofus! (/lh)")
    sys.exit(-1)

dir_to_scan = " ".join(sys.argv[1:])

pygame.init()

window = pygame.display.set_mode((800, 800), pygame.NOFRAME)
font = pygame.Font("font.ttf", 32)
small_font = pygame.Font("font.ttf", 20)

files = []
ignore_folders = ["addons"]

extensions = {}

scene_count = 0
asset_count = 0

def scan_folder(folder):
    global files
    global asset_count
    global scene_count
    global extensions

    for i in os.listdir(folder):
        if i[0] == ".": continue
        p = f"{folder}/{i}"

        if os.path.isdir(p) and not i in ignore_folders:
            scan_folder(p)
        
        elif os.path.isfile(p):
            if ".uid" not in i and ".import" not in i:
                if ".gd" in i:
                    files.append(p)
                
                elif ".tscn" in i:
                    scene_count += 1
                
                elif ".tres" in i:
                    asset_count += 1
                
                ext = os.path.splitext(i)[-1]

                if ext not in extensions.keys():
                    extensions[ext] = 1
                
                else:
                    extensions[ext] += 1

# dir_to_scan = "C:/Users/Lim/Documents/Godot/GGGG"

scan_folder(dir_to_scan)

lines = 0
biggest_file = ""
biggest_file_lines = 0

process_files = 0
tool_files = 0
exported_variables = 0
total_vars = 0
typed_variables = 0
connected_signals = 0
ud_signals = 0

with open(f"{dir_to_scan}/project.godot") as proj:
    data = proj.read().strip().split("\n")

name = ""

for i in data:
    if "config/name" in i:
        name = eval(i.replace("config/name=", ""))

for i in files:
    with open(i) as file:
        data = file.read().strip().split("\n")
    
    current_file_lines = 0

    for l in data:
        if "_process(" in l: process_files += 1
        if "@tool" in l: tool_files += 1
        if "@export" in l: exported_variables += 1
        if "var" in l:
            if ":" in l: typed_variables += 1
            total_vars += 1
        if ".connect(" in l: connected_signals += 1
        if "signal " in l: ud_signals += 1
        if len(l) == 0: continue
        lines += 1
        current_file_lines += 1
    
    if current_file_lines > biggest_file_lines:
        biggest_file = i
        biggest_file_lines = current_file_lines

sorted_extensions = dict(sorted(extensions.items(), key=lambda item: -item[1]))

os.system('cls' if os.name == 'nt' else 'clear')
print(f"{name}: wrapped")
print("=" * os.get_terminal_size()[0])
print(f"Total lines: {lines}")
print(f"Biggest file: {biggest_file} ({biggest_file_lines} lines)")
print(f"Tool scripts: {tool_files} | Process scripts: {process_files}")
print("=" * os.get_terminal_size()[0])
print(f"{total_vars} variables ({typed_variables} were explicitly typed, so {round((typed_variables / total_vars) * 100)}%)")
print(f"{exported_variables} @export calls")
print(f"{connected_signals} connected signals (out of {ud_signals} defined)")
print("=" * os.get_terminal_size()[0])
print(f"Scenes (*.tscn): {scene_count}")
print(f"Assets (*.tres): {asset_count}")
print("=" * os.get_terminal_size()[0])

top3 = list(sorted_extensions.keys())[0:3]

print("Your top 3 most used file formats:")

index = 1

for i in top3:
    print(f"#{index}: {i.strip()[1:]} ({sorted_extensions[i]})")
    index += 1

running = True

background = pygame.Surface((1, 2))
background.set_at((0, 0), (6, 31, 29))
background.set_at((0, 1), (9, 2, 20))

def draw_text(text, position, color="#FFFFFF", font=small_font):
    r = font.render(text, True, color, wraplength=800)
    # sr = font.render(text, True, f"{color}20", wraplength=800)
    # window.blit(sr, pygame.Vector2(position) + pygame.Vector2((2, 1)))
    window.blit(r, position)
    return r.get_height()

def format_number(value): # https://stackoverflow.com/questions/5180365/add-commas-into-number-string
    return '{:,}'.format(value)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill("#FFFFFF")
    window.blit(pygame.transform.smoothscale(background, window.get_size()))

    y = draw_text("godot wrapped: created by @lim95.com (bluesky)", (4, 4))
    y += draw_text(f"{name}", (4, y + 8), font=font)
    y += 32
    y += draw_text(f"you used {format_number(lines)} lines over {format_number(len(files))} files (average of {round(lines / len(files), 2)} lines per file)", (4, y + 8))
    y += draw_text(f"your biggest file was {os.path.split(biggest_file)[-1]} with {format_number(biggest_file_lines)} lines", (4, y + 8))
    y += draw_text(f"you had {format_number(tool_files)} tool scripts and {format_number(process_files)} scripts with a process function", (4, y + 8))
    y += 32
    y += draw_text(f"you have {format_number(total_vars)} variables ({format_number(typed_variables)} were explicitly typed, so {round((typed_variables / total_vars) * 100)}%)", (4, y + 8))
    y += draw_text(f"you used @export {format_number(exported_variables)} times", (4, y + 8))
    y += draw_text(f"you connected to signals {format_number(connected_signals)} times (but you only defined {format_number(ud_signals)})", (4, y + 8))
    y += 32
    y += draw_text(f"you used {format_number(scene_count)} scenes and {format_number(asset_count)} assets", (4, y + 8))
    y += 32
    y += draw_text("your most used file formats were:", (4, y + 8))
    index = 1
    for i in top3:
        y += draw_text(f"#{index}: *{i.strip()} ({format_number(sorted_extensions[i])})", (4, y + 8))

    if (window.get_height() != y + 32):
        window = pygame.display.set_mode((800, y + 32), pygame.NOFRAME)

    pygame.display.update()