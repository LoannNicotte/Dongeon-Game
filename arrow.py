# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 15:24:24 2021

@author: loann
"""
import pygame
import fonctions_utiles as FU
import math


class Arrow:
    def __init__(self, posx, posy, angle, ms):
        self.angle = angle
        self.img = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load("assets/player/arrow.png"), (FU.convert(31), 5)), -angle)
        self.rect = self.img.get_rect()
        self.rect.center = (posx, posy)
        self.points = []

        self.speed = 7
        self.travel = True
        self.shoot = ms

        self.x, self.y = self.rect.center

    def display(self, screen, player, inv, ms):

        if self.travel:
            self.x += math.cos(math.radians(self.angle)) * self.speed
            self.y += math.sin(math.radians(self.angle)) * self.speed

            self.rect.center = self.x, self.y

            for pos in self.points:
                pygame.draw.circle(screen, (130, 130, 130), (pos), 1)

            if (FU.get_pos_salle(self.rect.topleft[0], self.rect.topleft[1]) in FU.pos_walls or
                FU.get_pos_salle(self.rect.topright[0], self.rect.topright[1]) in FU.pos_walls or
                FU.get_pos_salle(self.rect.bottomright[0], self.rect.bottomright[1]) in FU.pos_walls or
                    FU.get_pos_salle(self.rect.bottomleft[0], self.rect.bottomright[1]) in FU.pos_walls):
                self.travel = False

        else:
            for x, y in [self.rect.topleft, self.rect.topright,
                         self.rect.bottomright, self.rect.bottomleft]:
                if (player.posx < x and player.posx + player.height > x and
                        player.posy < y and player.posy + player.width > y and self in FU.arrows):
                    self.kill()
                    inv.aug_arrow(1)

            if self.shoot + 10000 < ms and self in FU.arrows:
                self.kill()

        screen.blit(self.img, (self.rect.x, self.rect.y))
        self.points.append(self.rect.center)

        if len(self.points) > 5:
            self.points.pop(0)

    def display_hitbox(self, screen, ms):
        pygame.draw.rect(screen, (0, 0, 255), self.rect, 1)
        txt = FU.font_fps.render(str(ms - self.shoot), True, ((0, 0, 255)))
        screen.blit(txt, (self.rect.bottomright))

    def kill(self):
        FU.arrows.remove(self)
