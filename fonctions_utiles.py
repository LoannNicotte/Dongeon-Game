# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 13:33:53 2021

@author: loann
"""
import pygame
import animation
import math
import os
import images as img

pygame.init()


def display_salle():
    screen.blit(img.salles[salle[0]][salle[1]], (convert(448), convert(28)))


def display_open_porte():
    screen.blit(txt_porte, (screen.get_width() / 2 -
                            txt_porte.get_width() / 2,
                            2 * screen.get_height() / 3))


def display_open_coffre():
    screen.blit(txt_coffre, (screen.get_width() / 2 -
                             txt_porte.get_width() / 2,
                             2 * screen.get_height() / 3))


def display_fps():
    FPS = font_fps.render(
        f"{round(clock.get_fps())} FPS", True, (100, 100, 100))
    screen.blit(FPS, (4, 4))


def convert(x):
    return round(x * screen.get_width() / 1920)


def get_plan(salle):
    plan = open(f"assets/plan/{salle[1]}-{salle[0]}.txt", "r")
    plan = plan.readlines()
    for line in range(len(plan)):
        plan[line] = plan[line][:16]
    return plan


def get_pos_salle(x, y):
    x -= convert(448)
    y -= convert(28)
    return round(x // convert(64)), round(y // convert(64))


def get_pos_screen(x, y):
    return convert(448 + x * 64), convert(28 + y * 64)


def get_distance(player, mob):
    center = player.get_center_screen()
    x1 = center[0]
    y1 = center[1]

    if mob.name == "slime":
        center = mob.get_center_screen()
        x2 = center[0]
        y2 = center[1]

    else:
        x2 = mob.posx
        y2 = mob.poy

    return math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))


def init_salle(salle):
    plan = get_plan(salle)
    (pos_walls, pos_coffres, pos_portes, spikes,
     torches, spawnable) = [], [], [], [], [], []

    for i in range(len(plan)):
        for j in range(len(plan[i])):
            pos = get_pos_screen(j, i)

            if plan[i][j] == 'P':
                pos_portes.append((j, i))

            elif plan[i][j] == '^':
                torches.append(animation.Animation(img.images_torches_up,
                                                   pos[0] + convert(25),
                                                   pos[1] + convert(11),
                                                   pygame.time.get_ticks()))

            elif plan[i][j] == '>':
                torches.append(animation.Animation(img.images_torches_right,
                                                   pos[0] + convert(50),
                                                   pos[1] + convert(10),
                                                   pygame.time.get_ticks()))

            elif plan[i][j] == '<':
                torches.append(animation.Animation(img.images_torches_left,
                                                   pos[0],
                                                   pos[1] + convert(10),
                                                   pygame.time.get_ticks()))

            elif plan[i][j] == 'S':
                pos = get_pos_screen(j, i)
                spikes.append(animation.Animation(img.images_spikes,
                                                  pos[0], pos[1],
                                                  pygame.time.get_ticks(),
                                                  100, "spike"))

            elif plan[i][j] == 'X':
                pos_walls.append((j, i))

            elif plan[i][j] == 'C':
                pos_coffres.append((j, i))

            elif plan[i][j] == "1":
                spawnable.append((j, i))

    return pos_walls, pos_coffres, pos_portes, spikes, torches, spawnable


# Constantes
screen = img.screen

pygame.mouse.set_cursor(*pygame.cursors.tri_left)

pygame.display.set_caption("Dongeon Game")

clock = pygame.time.Clock()

font_fps = pygame.font.SysFont(None, 20)
font_txt = pygame.font.SysFont(None, 35)
font_item = pygame.font.Font("assets/font/font.ttf", convert(40))
font = pygame.font.Font("assets/font/font.ttf", convert(20))


txt_porte = font_txt.render("Press SPACE for take door", True, (255, 255, 255))
txt_coffre = font_txt.render(
    "Press SPACE for open chest", True, (255, 255, 255))

armor_value = {"chestplate_brown": 0.5, "chestplate_white": 0.5,
               "chestplate_chain": 1.5, "chestplate_leather": 1,
               "chestplate_metal": 2.5, "feet_leather": 0.5,
               "feet_metal": 1, "gloves": 0.5, "helmet_chain": 1,
               "helmet_leather": 0.5, "helmet_metal": 1.5, "hood_chain": 1,
               "hood_leather": 0.5, "legs_leather": 1, "legs_metal": 1.5}

item_name = {"chestplate_brown": "T-Shirt Marron", "chestplate_white": "T-Shirt Blanc",
             "chestplate_chain": "Cotte de Maille", "chestplate_leather": "Plastron en Cuir",
             "chestplate_metal": "Plastron en Metal", "feet_leather": "Botte en Cuir",
             "feet_metal": "Botte en Metal", "gloves": "Gant en Metal", "helmet_chain": "Casque en Maille",
             "helmet_leather": "Casque en Cuir", "helmet_metal": "Casque en Metal", "hood_chain": "Chapeau en Maille",
             "hood_leather": "Chapeau en Cuir", "legs_leather": "Jambiere en Cuir", "legs_metal": "Jambiere en Metal",
             "belt_leather": "Ceinture en Cuir", "belt_rope": "Ceinture en Corde",
             "bow": "Arc", "dagger": "Dague", "quiver": "Carquois",
             "sheild1": "Bouclier", "spear": "Lance", "arrow": "Fleche",
             "rope": "Corde", "stick": "Baton", "string": "Ficelle"}

item_type = {"chestplate_brown": "chestplate", "chestplate_white": "chestplate",
             "chestplate_chain": "chestplate", "chestplate_leather": "chestplate",
             "chestplate_metal": "chestplate", "feet_leather": "feets",
             "feet_metal": "feets", "gloves": "gloves", "helmet_chain": "helmet",
             "helmet_leather": "helmetr", "helmet_metal": "helmet", "hood_chain": "helmet",
             "hood_leather": "helmet", "legs_leather": "legs", "legs_metal": "legs",
             "belt_leather": "belt", "belt_rope": "belt",
             "bow": "weapons", "dagger": "weapons", "quiver": "weapons",
             "sheild1": "sheild", "spear": "weapons", "arrow": "item",
             "rope": "item", "stick": "item", "string": "item"}

item_class = {"armor": ["chestplate_brown", "chestplate_white", "chestplate_chain", "chestplate_leather",
                        "chestplate_metal", "feet_leather", "feet_metal", "gloves", "helmet_chain",
                        "helmet_leather", "helmet_metal", "hood_chain", "hood_leather", "legs_leather",
                        "legs_metal", "belt_leather", "belt_rope", ],
              "weapons": ["bow", "dagger", "quiver",  "sheild1", "spear"],
              "item": ["rope", "stick", "string", "arrow"]}

target_cursor = pygame.cursors.compile(("          XXXX          ",
                                        "          X..X          ",
                                        "          X..X          ",
                                        "        XXX..XXX        ",
                                        "       X........X       ",
                                        "      X...X..X..X       ",
                                        "     X..XXX..XXX..X     ",
                                        "    X..X  X..X  X..X    ",
                                        "   X..X   X..X   X..X   ",
                                        "   X..X   X..X   X..X   ",
                                        "XXXX.XXXXX XX XXXXX.XXXX",
                                        "X.........X  X.........X",
                                        "X.........X  X.........X",
                                        "XXXX.XXXXX XX XXXXX.XXXX",
                                        "   X..X   X..X   X..X   ",
                                        "   X..X   X..X   X..X   ",
                                        "    X..X  X..X  X..X    ",
                                        "     X..XXX..XXX..X     ",
                                        "      X...X..X...X      ",
                                        "       X........X       ",
                                        "        XXX..XXX        ",
                                        "          X..X          ",
                                        "          X..X          ",
                                        "          XXXX          ",))

# Variables

play = True
salle = (1, 0)

key_pressed = []

arrows = []


# Images

sounds_footstep = [pygame.mixer.Sound(
    f"assets/sounds/footsteps/{i}")
    for i in os.listdir("assets/sounds/footsteps")]

(pos_walls, pos_coffres, pos_portes, spikes, torches,
 spawnable) = None, None, None, None, None, None
