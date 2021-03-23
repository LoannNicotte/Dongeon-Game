# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 10:48:03 2021

@author: Lebobe Timothé
"""


import os
import pygame
import threading

import animation
import main
import images as img
import fonctions_utiles as FU


def convert(x):
    return round(x * screen.get_width() / 1920)


pygame.init()

screen = img.screen
clock = pygame.time.Clock()

pour_txt = pygame.font.SysFont(None, convert(42))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def load_sprites_player():

    sprite_size = {"bow": (13, 4), "hurt": (6, 1), "dagger": (
        6, 4), "spellcast": (7, 4), "spear": (8, 4), "walkcycle": (9, 4)}

    global nb

    nb = 0
    return_val = {}
    for anim in os.listdir("assets/player/players"):
        return_val[anim] = {}
        for part in os.listdir(f"assets/player/players/{anim}"):
            return_val[anim][part] = []
            for i in range(sprite_size.get(anim)[1]):
                temp = []
                for j in range(sprite_size.get(anim)[0]):
                    temp.append(pygame.transform.scale(
                        pygame.image.load(
                            f"assets/player/players/{anim}/{part}")
                        .convert_alpha()
                        .subsurface((64 * j, 64 * i, 64, 64)),
                        (convert(128), convert(128))
                    ))
                    nb += 1
                return_val[anim][part].append(temp)

    nb += img.init_salles()
    nb += img.init_cursor()
    nb += img.init_spike()
    nb += img.init_torches_left()
    nb += img.init_torches_right()
    nb += img.init_torches_up()
    nb += img.init_back_name()
    nb += img.init_img_armor()
    nb += img.init_img_coeur()
    nb += img.init_back_flou()
    nb += img.init_display_part()
    nb += img.init_none_equiped()
    nb += img.init_images_inv()
    nb += img.init_slimes()
    nb += img.init_portes()
    nb += img.init_image_craft()
    nb += img.init_item_craft()
    nb += img.init_item_recipes()

    print(nb)

    return return_val


def loading_page(run: bool = True) -> bool:
    clock.tick(100)

    time = pygame.time.get_ticks()

    screen.blit(sablier, (0, 0))

    chargement_anim.update(screen, time)

    pygame.draw.rect(screen, WHITE, [convert(
        60),  convert(870), convert(1800), convert(30)])
    pygame.draw.rect(screen, BLACK, [convert(62), convert(
        872), convert(1796) * nb / nb_image_max, convert(26)])

    pourcent = pour_txt.render(
        str(round(nb * 100 / nb_image_max)) + " %", True, (125, 125, 125))

    screen.blit(pourcent, ((screen.get_width() -
                            pourcent.get_width()) / 2,  convert(871)))

    clock.tick(100)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    return run


class Load_sprites_p(threading.Thread):

    def __init__(self):
        super().__init__()
        self.imgs = {}
        self.state = True

    def run(self) -> None:
        self.imgs = load_sprites_player()
        self.state = False


run = True

nb = 0

thread = Load_sprites_p()
thread.start()


sablier = pygame.transform.scale(
    pygame.image.load("assets/loading_screen.png").convert(),
    (convert(1920), convert(1080)))


images_chargement = [pygame.transform.scale(pygame.image.load(
    f"assets/chargement/{i}").convert_alpha(),
    (convert(200), convert(200))) for i in os.listdir("assets/chargement")]

chargement_anim = animation.Animation(
    images_chargement, screen.get_width() / 2 - convert(100),
    screen.get_height() / 2 - convert(200), pygame.time.get_ticks())

clock = pygame.time.Clock()

nb_image_max = 4886

while run:

    if nb >= nb_image_max and not thread.state:
        (FU.pos_walls, FU.pos_coffres, FU.pos_portes, FU.spikes,
         FU.torches, FU.spawnable) = FU.init_salle(FU.salle)
        main.game(thread.imgs)
        thread._stop()
        run = False

    else:
        run = loading_page(run)

pygame.quit()


if __name__ == "__main__":
    pass
