# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 22:54:05 2021

@author: loann
"""


class Animation:

    def __init__(self, images, x, y, ms, delay=100, mode=None):
        self.x = x
        self.y = y
        self.images = images
        self.n_image = 0
        self.delay = delay
        self.default_delay = self.delay
        self.last_play = ms
        self.mode = mode
        self.active = False

    def update(self, screen, ms):
        if self.mode == "spike":
            screen.blit(self.images[self.n_image], (self.x, self.y))
            if self.last_play + self.delay < ms:
                self.last_play = self.last_play + self.delay
                self.delay = self.default_delay
                self.n_image += 1
                self.active = False
                if self.n_image == len(self.images):
                    self.n_image = 0
                    self.delay = 2000
                    self.active = False
                elif self.n_image == 1:
                    self.delay = 1000
                    self.active = True

        else:
            screen.blit(self.images[self.n_image], (self.x, self.y))
            if self.last_play + self.delay < ms:
                self.last_play = self.last_play + self.delay
                self.delay = self.default_delay
                self.n_image += 1
                if self.n_image == len(self.images):
                    self.n_image = 0
