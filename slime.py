# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:12:36 2021
@author: loann
"""
import fonctions_utiles as FU
import random as rdm
import math
import images as img


import pygame


class Slime:
    def __init__(self, screen, ms):
        self.name = "slime"
        self.screen = screen
        self.len = FU.convert(128)

        pos = rdm.choice(FU.spawnable)
        pos = FU.get_pos_screen(pos[0], pos[1])
        self.posx = pos[0] - FU.convert(self.len) * 5/12
        self.posy = pos[1] - self.len / 2 - FU.convert(64) * 1/6
        self.anim_jump = False
        self.anim_roulade = False
        self.anim_shoot = False
        self.anim_death = False

        self.dead = False

        self.couleur = rdm.randint(0, 3)

        self.angle = 0

        self.last_jump = ms
        self.last_shoot = ms

        self.images = img.images_slime
        self.current_img = self.images[0 + 5 * self.couleur][0]
        self.rect = self.current_img.get_rect()

        self.n_image = 0
        self.last_play = ms

    def display(self, ms):
        if self.anim_death:
            self.current_img = self.images[4 + 5 * self.couleur][self.n_image]

        elif self.anim_shoot:
            self.current_img = self.images[3 + 5 * self.couleur][self.n_image]

        elif self.anim_roulade:
            self.current_img = self.images[1 + 5 * self.couleur][self.n_image]

        elif self.anim_jump:
            self.current_img = self.images[2 + 5 * self.couleur][self.n_image]

        else:
            self.current_img = self.images[0 + 5 * self.couleur][self.n_image]

        self.screen.blit(self.current_img, (self.posx, self.posy))

        if self.last_play + 80 < ms:
            self.n_image += 1
            self.last_play = ms
            coef = 6
            if self.anim_death:
                pass

            elif self.anim_roulade and not self.anim_shoot:
                self.posy += FU.convert(10)

            elif self.anim_jump and not self.anim_shoot:
                distance = (-(coef/80000) * ((80 * self.n_image) ** 2) +
                            coef/100 * (80 * self.n_image))

                self.posx += math.cos(math.radians(self.angle)
                                      ) * FU.convert(distance)
                self.posy += math.sin(math.radians(self.angle)
                                      ) * FU.convert(distance)

            if self.n_image == 10:
                if self.anim_death:
                    self.dead = True
                self.anim_jump = False
                self.anim_roulade = False
                self.anim_shoot = False
                self.n_image = 0

    def display_hitbox(self):
        pygame.draw.rect(self.screen, (255, 0, 0), [self.posx + self.len * 1/3,
                                                    self.posy + self.len * 2/3,
                                                    self.len * 1/3,
                                                    self.len * 1/3], 1)

        pygame.draw.rect(self.screen, (0, 0, 255), [
                         self.posx, self.posy, self.len, self.len], 1)

        pygame.draw.circle(self.screen, (255, 0, 0),
                           (self.get_center_screen()[0],
                            self.get_center_screen()[1]), 2)

    def shoot(self, player, ms):
        self.n_image = 0
        self.anim_shoot = True

        self.last_shoot = ms

        player.take_damage(1)

    def jump(self, ms):
        self.n_image = 0
        self.anim_jump = True
        self.last_jump = ms
        self.angle = rdm.randint(0, 360)

        movex = math.cos(math.radians(self.angle)) * FU.convert(90)
        movey = math.sin(math.radians(self.angle)) * FU.convert(90)

        pts = [FU.get_pos_salle(self.posx + self.len * 1/3 + movex,
                                self.posy + self.len * 2/3 + movey),
               FU.get_pos_salle(self.posx + self.len * 1/3 + movex,
                                self.posy + self.len + movey),
               FU.get_pos_salle(self.posx + self.len * 2/3 + movex,
                                self.posy + self.len * 2/3 + movey),
               FU.get_pos_salle(self.posx + self.len * 2/3 + movex,
                                self.posy + self.len + movey)]

        go = True

        for i in pts:
            if i in FU.pos_walls:
                go = False

        while not go:
            go = True

            self.angle = rdm.randint(0, 360)

            movex = math.cos(math.radians(self.angle)) * FU.convert(90)
            movey = math.sin(math.radians(self.angle)) * FU.convert(90)

            pts = [FU.get_pos_salle(self.posx + self.len * 1/3 + movex,
                                    self.posy + self.len * 2/3 + movey),
                   FU.get_pos_salle(self.posx + self.len * 1/3 + movex,
                                    self.posy + self.len + movey),
                   FU.get_pos_salle(self.posx + self.len * 2/3 + movex,
                                    self.posy + self.len * 2/3 + movey),
                   FU.get_pos_salle(self.posx + self.len * 2/3 + movex,
                                    self.posy + self.len + movey)]

            for i in pts:
                if i in FU.pos_walls:
                    go = False

    def roulade(self):
        self.n_image = 0
        self.anim_roulade = True

    def death(self):
        self.n_image = 0
        self.anim_death = True
        self.anim_death = True

    def get_center_screen(self):
        return self.posx + self.len / 2, self.posy + self.len * 5 / 6
