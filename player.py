# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 20:09:42 2021

@author: loann
"""
import pygame
import os
import math
import arrow


import images as img
import fonctions_utiles as FU


class Player:

    def __init__(self, inventaire, imgs):
        self.inventaire = inventaire

        self.posx = FU.screen.get_width() / 2
        self.posy = FU.screen.get_height() / 2
        self.width = FU.convert(128)
        self.height = FU.convert(128)
        self.speed = 4

        self.imgs = imgs

        self.vie = 3
        self.max_vie = 3

        self.armor = 0
        self.max_armor = 7

        self.armored = False
        self.direction = 2
        self.move = False

        self.last_image = 0
        self.n_image = 0

        self.last_anim = None
        self.last_image_bow = 0
        self.last_image_spear = 0
        self.last_image_dagger = 0

        self.last_sound = 0
        self.n_sound = 0

        self.img_coeur = img.images_coeur
        self.img_armor = img.images_armor

        self.bow_effect = pygame.mixer.Sound("assets/sounds/bow_shoot.mp3")

    def display(self, screen, ms, inv):
        if not self.move:

            weapons = self.inventaire.equiped.get("weapons")[0]
            if not weapons:
                anim = "walkcycle"
                self.last_anim = "walkcycle"
                self.n_image = 0
            else:
                anim = weapons.name
                if self.last_anim != anim:
                    self.last_anim = anim
                    self.n_image = 0
                if not inv:
                    if anim == "bow":
                        pygame.mouse.set_cursor(
                            (24, 24), (0, 0), *FU.target_cursor)
                        mouse = pygame.mouse.get_pos()

                        x = mouse[0] + 12 - (self.posx + self.width / 2)
                        y = mouse[1] + 12 - (self.posy + self.height / 2)
                        angle = math.degrees(math.atan2(y, x))

                        if -45 <= angle <= 45:
                            self.direction = 3
                        elif 45 <= angle <= 135:
                            self.direction = 2
                        elif 135 <= angle or -135 >= angle:
                            self.direction = 1
                        else:
                            self.direction = 0

                        if (pygame.mouse.get_pressed()[0] and
                            self.n_image <= 8 and
                                self.inventaire.equiped.get("arrow")[0]):
                            if (self.last_image_bow + 100 < ms and
                                    self.n_image < 8):
                                self.last_image_bow = ms
                                self.n_image += 1

                        elif 8 <= self.n_image < 12:
                            if self.last_image_bow + 100 < ms:
                                if self.n_image == 8:
                                    self.shoot(angle, ms)
                                self.last_image_bow = ms
                                self.n_image += 1

                        else:
                            self.n_image = 0

                    elif anim == "dagger":
                        if (pygame.mouse.get_pressed()[0] and
                                self.n_image == 0):
                            self.n_image += 1

                        if (self.n_image > 0 and
                                self.last_image_spear + 100 < ms):
                            self.last_image_spear = ms
                            self.n_image += 1

                            if self.n_image == 6:
                                self.n_image = 0

                    elif anim == "spear":
                        if (pygame.mouse.get_pressed()[0] and
                                self.n_image == 0):
                            self.n_image += 1

                        if (self.n_image > 0 and
                                self.last_image_dagger + 100 < ms):
                            self.last_image_dagger = ms
                            self.n_image += 1

                            if self.n_image == 7:
                                self.n_image = 0

                else:
                    self.n_image = 0
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

        else:
            anim = "walkcycle"
            self.last_anim = "walkcycle"

        try:
            if (self.direction != 0 and
                    self.inventaire.equiped.get("quiver")[0]):
                screen.blit(
                    self.imgs.get(anim).get("quiver.png")
                    [self.direction][self.n_image], (self.posx, self.posy))

            screen.blit(
                self.imgs.get(anim).get(f"{self.inventaire.body}.png")
                [self.direction][self.n_image], (self.posx, self.posy))

            helmet = self.inventaire.equiped.get("helmet")[0]
            if self.inventaire.body == "human" and not helmet:
                screen.blit(self.imgs.get(anim).get("hair.png")[self.direction]
                            [self.n_image], (self.posx, self.posy))

            if (self.inventaire.body == "human" and helmet and
                    helmet.name != "helmet_metal" and
                    helmet.name != "hood_chain"):
                screen.blit(self.imgs.get(anim).get("hair.png")[self.direction]
                            [self.n_image], (self.posx, self.posy))

            for nom, value in self.inventaire.equiped.items():
                if (value[0] and nom != "quiver"):
                    if (anim == "walkcycle" and nom != "weapons" and
                            nom != "arrow"):
                        screen.blit(
                            self.imgs.get(anim).get(f"{value[0].name}.png")
                            [self.direction][self.n_image],
                            (self.posx, self.posy))

                    elif (anim == "spear" and nom != "arrow"):
                        screen.blit(
                            self.imgs.get(anim).get(f"{value[0].name}.png")
                            [self.direction][self.n_image],
                            (self.posx, self.posy))

                    elif (anim == "bow" and nom != "sheild"):
                        screen.blit(
                            self.imgs.get(anim).get(f"{value[0].name}.png")
                            [self.direction][self.n_image],
                            (self.posx, self.posy))

                    elif (anim == "dagger" and nom != "sheild" and
                          nom != "arrow"):
                        screen.blit(
                            self.imgs.get(anim).get(f"{value[0].name}.png")
                            [self.direction][self.n_image],
                            (self.posx, self.posy))

                    elif ((anim == "hurt" or anim == "spellcast") and
                          nom != "sheild" and nom != "arrow" and
                          nom != "weapons"):
                        screen.blit(
                            self.imgs.get(anim).get(f"{value[0].name}.png")
                            [self.direction][self.n_image],
                            (self.posx, self.posy))

            if (self.direction == 0 and
                    self.inventaire.equiped.get("quiver")[0]):
                screen.blit(self.imgs.get(anim).get("quiver.png")
                            [self.direction][self.n_image],
                            (self.posx, self.posy))

        except IndexError:
            self.n_image = 0

        for i in range(7):
            if i < int(self.vie):
                img = self.img_coeur[0]
            elif self.vie - i == 0.5:
                img = self.img_coeur[3]
            elif i < self.max_vie:
                img = self.img_coeur[1]
            else:
                img = self.img_coeur[2]
            screen.blit(
                img, (FU.convert(30) + FU.convert(55) * i, FU.convert(50)))

            if i < int(self.inventaire.get_armor()):
                img = self.img_armor[1]
            elif self.armor - i == 0.5:
                img = self.img_armor[0]
            else:
                img = self.img_armor[2]

            screen.blit(
                img, (FU.convert(30) + FU.convert(55) * i, FU.convert(110)))

    def display_hitbox(self, screen):
        pygame.draw.rect(screen,  (255, 0, 0), [
                         self.posx, self.posy, self.width, self.height], 1)

        center = self.get_center_screen()
        pygame.draw.circle(screen, (255, 0, 0),
                           (center[0], center[1]), 2)

    def move_up(self, ms):
        self.direction = 0

        a = FU.get_pos_salle(self.posx, self.posy - 7)
        b = FU.get_pos_salle(self.posx + self.width, self.posy - 7)
        if a not in FU.pos_walls and b not in FU.pos_walls:
            self.posy -= self.speed

        self.next_image(ms)

    def move_down(self, ms):
        self.direction = 2

        a = FU.get_pos_salle(self.posx, self.posy + self. height + 7)
        b = FU.get_pos_salle(self.posx + self.width,
                             self.posy + self.height + 7)
        if a not in FU.pos_walls and b not in FU.pos_walls:
            self.posy += self.speed

        self.next_image(ms)

    def move_right(self, ms):
        self.direction = 3

        a = FU.get_pos_salle(self.posx + self.width + 7, self.posy)
        b = FU.get_pos_salle(self.posx + self.width + 7,
                             self.posy + self.height / 2)
        c = FU.get_pos_salle(self.posx + self.width +
                             7, self.posy + self.height)
        if(a not in FU.pos_walls and b not in FU.pos_walls and
                c not in FU.pos_walls):
            self.posx += self.speed

        self.next_image(ms)

    def move_left(self, ms):
        self.direction = 1

        a = FU.get_pos_salle(self.posx - 7, self.posy)
        b = FU.get_pos_salle(self.posx - 7, self.posy + self. height / 2)
        c = FU.get_pos_salle(self.posx - 7, self.posy + self.height)
        if (a not in FU.pos_walls and b not in FU.pos_walls and
                c not in FU.pos_walls):
            self.posx -= self.speed

        self.next_image(ms)

    def next_image(self, ms):
        if self.last_image + 50 < ms:
            self.last_image = ms
            self.n_image += 1
            if self.n_image == 9:
                self.n_image = 1

        if self.last_sound + 300 < ms:
            FU.sounds_footstep[self.n_sound].play()
            self.last_sound = ms
            self.n_sound += 1
            if self.n_sound == 4:
                self.n_sound = 0

    def get_center_salle(self):
        return FU.get_pos_salle(self.posx + self.width / 2,
                                self.posy + self.height - FU.convert(12))

    def get_center_screen(self):
        return (self.posx + self.width / 2, self.posy + self.height / 2)

    def take_damage(self, damage):
        if self.armored:
            damage /= 2

        self.vie -= damage

    def shoot(self, angle, ms):
        FU.arrows.append(arrow.Arrow(self.posx + self.width /
                                     2, self.posy + self.height / 2,
                                     angle, ms))
        self.inventaire.dim_arrow(1)
        self.bow_effect.play()
