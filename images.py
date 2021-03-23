# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 08:18:14 2021

@author: loann
"""

import pygame
import os

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((1366, 768))
screen = pygame.display.set_mode((1920, 1080))


def convert(x):
    return round(x * screen.get_width() / 1920)


def init_salles():
    global salles

    salles = [[pygame.transform.scale(
        pygame.image.load("assets/salles/0-0.png").convert(),
        (convert(1024), convert(1024)))],
        [pygame.transform.scale(
            pygame.image.load("assets/salles/0-1.png").convert(),
            (convert(1024), convert(1024)))]]

    return 2


def init_cursor():
    global cursor
    nb = 0
    cursor = []
    for i in range(3):
        cursor.append(pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/recipes_book/cursor{str(i)}.png").convert_alpha(), (convert(64), convert(102))))
        nb += 1

    return nb


def init_spike():
    global images_spikes
    nb = 0
    images_spikes = []
    for i in os.listdir("assets/spike"):
        images_spikes.append(pygame.transform.scale(pygame.image.load(
            f"assets/spike/{i}").convert_alpha(), (convert(64), convert(64))))
        nb += 1

    return nb


def init_torches_up():
    global images_torches_up
    nb = 0
    images_torches_up = []
    for i in os.listdir("assets/torches/torche_u"):
        images_torches_up.append(pygame.transform.scale(pygame.image.load(
            f"assets/torches/torche_u/{i}").convert_alpha(),
            (convert(14), convert(41))))
        nb += 1

    return nb


def init_torches_left():
    global images_torches_left
    nb = 0
    images_torches_left = []
    for i in os.listdir("assets/torches/torche_l"):
        images_torches_left.append(pygame.transform.scale(pygame.image.load(
            f"assets/torches/torche_l/{i}").convert_alpha(),
            (convert(14), convert(41))))
        nb += 1

    return nb


def init_torches_right():
    global images_torches_right
    nb = 0
    images_torches_right = []
    for i in os.listdir("assets/torches/torche_r"):
        images_torches_right.append(pygame.transform.scale(pygame.image.load(
            f"assets/torches/torche_r/{i}").convert_alpha(),
            (convert(14), convert(41))))
        nb += 1

    return nb


def init_back_name():
    global back_name
    back_name = pygame.image.load("assets/inventaire/back_name.png")

    return 1


def init_img_coeur():
    global images_coeur
    nb = 0
    images_coeur = []
    for i in os.listdir("assets/stats_player/coeurs"):
        images_coeur.append(pygame.transform.scale(
            pygame.image.load(f"assets/stats_player/coeurs/{i}"
                              ).convert_alpha(), (convert(45), convert(39))))
        nb += 1

    return nb


def init_img_armor():
    global images_armor
    nb = 0
    images_armor = []
    for i in os.listdir("assets/stats_player/armure"):
        images_armor.append(pygame.transform.scale(
            pygame.image.load(f"assets/stats_player/armure/{i}"
                              ).convert_alpha(), (convert(45), convert(45))))
        nb += 1

    return nb


def init_images_inv():
    global images_inv
    nb = 0
    images_inv = []
    for i in range(3):
        images_inv.append(pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/inventaire{str(i)}.png").convert_alpha(),
            (convert(654), convert(584))))
        nb += 1

    return nb


def init_back_flou():
    global flou
    flou = pygame.transform.scale(pygame.image.load(
        "assets/inventaire/flou.png").convert_alpha(),
        (convert(64), convert(64)))

    return 1


def init_none_equiped():
    global images_none_equiped
    nb = 0
    images_none_equiped = {}
    for nom in os.listdir("assets/inventaire/none_equiped"):
        images_none_equiped[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/none_equiped/{nom}").convert_alpha(),
            (convert(64), convert(64)))

        nb += 1

    return nb


def init_display_part():
    global images_display_part
    nb = 0
    images_display_part = {}
    for nom in os.listdir("assets/inventaire/display"):
        images_display_part[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/display/{nom}").convert_alpha(),
            (convert(195), convert(265)))

        nb += 1

    return nb


def init_slimes():
    global images_slime
    nb = 0
    image = pygame.image.load("assets/slime/slime_sprite.png")
    images_slime = [[]for i in range(20)]
    for i in range(20):
        for j in range(10):
            images_slime[i].append(pygame.transform.scale(image.subsurface(
                (32 * j, 32 * i, 32, 32)).convert_alpha(), (convert(128), convert(128))))
            nb += 1

    return nb


def init_portes():
    global images_porte
    images_porte = []
    for i in range(2):
        images_porte.append(pygame.transform.scale(pygame.image.load(
            f"assets/porte/porte{str(i)}.png").convert_alpha(),
            (convert(960), convert(1080))))
    return 2


def init_image_craft():
    global image_craft
    image_craft = pygame.transform.scale(pygame.image.load(
        "assets/inventaire/recipes_book/recipes.png").convert_alpha(),
        (convert(427), convert(241)))

    return 1


def init_item_craft():
    global images_item_craft
    nb = 0
    images_item_craft = {}
    for nom in os.listdir("assets/inventaire/recipes_book/items"):
        images_item_craft[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/recipes_book/items/{nom}").convert_alpha(),
            (convert(79), convert(79)))

        nb += 1

    return nb


def init_item_recipes():
    global images_item_recipes
    nb = 0
    images_item_recipes = {}
    for nom in os.listdir("assets/inventaire/recipes_book/items"):
        images_item_recipes[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/recipes_book/items/{nom}").convert_alpha(),
            (convert(50), convert(50)))

        nb += 1

    return nb
