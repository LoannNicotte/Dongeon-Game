# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 18:45:40 2021

@author: loann
"""
import pygame
import item
import crafting
import os
import random as rdm
import fonctions_utiles as FU
import images as img


class inventaire:
    def __init__(self, screen):
        self.screen = screen
        self.crafts = crafting.Crafting()

        self.width = FU.convert(654)
        self.height = FU.convert(584)
        self.posx = (self.screen.get_width() - self.width) / 2
        self.posy = (self.screen.get_height() - self.height) / 2

        self.img = img.images_inv

        self.sound = [pygame.mixer.Sound(
            f"assets/sounds/inventory/{i}")
            for i in os.listdir("assets/sounds/inventory")]

        self.flou = img.flou

        self.equiped_lst = [["helmet", "gloves"], [
            "chestplate", "belt"], ["legs", "sheild"], ["feets", "weapons"]]

        self.equiped = {}
        self.init_stuff()

        self.none_equiped = img.images_none_equiped

        self.inventory = [[[None, (self.posx + FU.convert(25) +
                                   FU.convert(67) * i, self.posy +
                                   FU.convert(345) + FU.convert(67) * j)]
                           for i in range(8)] for j in range(3)]
        self.init_inventory()

        self.pos_display_part = (FU.convert(
            144) + self.posx, FU.convert(10) + self.posy)

        self.display_part = img.images_display_part

        self.crafting_table = [[[None, (self.posx + FU.convert(64) +
                                        FU.convert(67) * i, self.posy +
                                        FU.convert(41) + FU.convert(67) * j)]
                                for i in range(4)] for j in range(4)]

        self.crafted = None

        self.body = rdm.choice(["human", "zombie", "skeleton"])

        self.hand = None
        self.last_pos_hand = (None, (0, 0))

        self.part = 0

    def display(self, mouse):
        self.screen.blit(self.img[self.part], (self.posx, self.posy))

        if self.part == 0:
            if self.equiped.get("quiver")[0]:
                self.screen.blit(self.display_part.get(
                    self.equiped.get("quiver")[0].name), self.pos_display_part)

            self.screen.blit(self.display_part.get(
                self.body), (self.pos_display_part))

            helmet = self.equiped.get("helmet")[0]
            if self.body == "human" and not helmet:
                self.screen.blit(self.display_part.get(
                    "hair"), (self.pos_display_part))

            if (self.body == "human" and helmet and
                    helmet.name != "helmet_metal" and
                    helmet.name != "hood_chain"):
                self.screen.blit(self.display_part.get(
                    "hair"), (self.pos_display_part))

            for nom, value in self.equiped.items():
                if (value[1][0] < mouse[0] < value[1][0] + FU.convert(67) and
                        value[1][1] < mouse[1] < value[1][1] + FU.convert(67)):
                    self.screen.blit(self.flou, value[1])

                    if value[0]:
                        value[0].display_name(self.screen, mouse)

                if not value[0]:
                    self.screen.blit(self.none_equiped.get(nom), value[1])
                else:
                    value[0].display(self.screen, value[1], "inv")

                    if (nom == "quiver" or
                        (nom == "arrow" and
                         not self.equiped.get("weapons")[0]) or
                        (self.equiped.get("weapons")[0] and
                         ((nom == "sheild" and
                           (self.equiped.get("weapons")[0].name == "bow" or
                            self.equiped.get("weapons")[0].name == "dagger"))
                          or nom == "arrow" and
                          self.equiped.get("weapons")[0].name != "bow"))):
                        continue

                    self.screen.blit(self.display_part.get(
                        self.equiped.get(nom)[0].name), self.pos_display_part)

            for nom, value in self.equiped.items():
                if (value[1][0] < mouse[0] < value[1][0] + FU.convert(67) and
                    value[1][1] < mouse[1] < value[1][1] + FU.convert(67) and
                        value[0]):
                    value[0].display_name(self.screen, mouse)

        elif self.part == 1:
            for i in range(4):
                for j in range(4):
                    item, pos = self.crafting_table[i][j]

                    if (pos[0] < mouse[0] < pos[0] + FU.convert(67) and
                            pos[1] < mouse[1] < pos[1] + FU.convert(67)):
                        self.screen.blit(self.flou, pos)

                    if item:
                        item.display(self.screen, pos, "inv")

            for i in range(4):
                for j in range(4):
                    item, pos = self.crafting_table[i][j]
                    if (pos[0] < mouse[0] < pos[0] + FU.convert(67) and
                            pos[1] < mouse[1] < pos[1] + FU.convert(67) and item):
                        item.display_name(self.screen, mouse)

            if self.posx + FU.convert(437) <= mouse[0] <= self.posx + FU.convert(501) and self.posy + FU.convert(142) <= mouse[1] <= self.posy + FU.convert(206):
                self.screen.blit(
                    self.flou, (self.posx + FU.convert(437), self.posy + FU.convert(142)))

            if self.crafted:
                self.crafted.display(
                    FU.screen, (self.posx + FU.convert(437), self.posy + FU.convert(142)), "inv")

        elif self.part == 2:
            self.crafts.display(self.screen, mouse)

        if self.part != 2:
            for i in range(3):
                for j in range(8):
                    item, pos = self.inventory[i][j]
                    if (pos[0] < mouse[0] < pos[0] + FU.convert(67) and
                            pos[1] < mouse[1] < pos[1] + FU.convert(67)):
                        self.screen.blit(self.flou, pos)

                    if item:
                        item.display(self.screen, pos, "inv")

            for i in range(3):
                for j in range(8):
                    item, pos = self.inventory[i][j]
                    if (pos[0] < mouse[0] < pos[0] + FU.convert(67) and
                            pos[1] < mouse[1] < pos[1] + FU.convert(67) and item):
                        item.display_name(self.screen, mouse)

            if self.hand:
                self.hand.display(
                    self.screen, (mouse[0] - FU.convert(32),
                                  mouse[1] - FU.convert(32)), "inv")

    def set_part(self, mouse):
        if self.part != 0:
            if (self.posx + FU.convert(584) <= mouse[0] <=
                self.posx + FU.convert(634) and
                    self.posy + FU.convert(36) <= mouse[1] <=
                    self.posy + FU.convert(86)):
                self.part = 0
                self.reset_crafting()
                self.crafts.reset_cursor()

    def set_craft(self, mouse):
        if self.part == 0:
            if (self.posx + FU.convert(584) <= mouse[0] <=
                self.posx + FU.convert(634) and
                    self.posy + FU.convert(106) <= mouse[1] <=
                    self.posy + FU.convert(156)):

                self.part = 1

        elif self.part == 2:
            if (self.posx + FU.convert(584) <= mouse[0] <=
                self.posx + FU.convert(634) and
                    self.posy + FU.convert(91) <= mouse[1] <=
                    self.posy + FU.convert(141)):

                self.part = 1
                self.crafts.reset_cursor()

    def set_recipes(self, mouse):
        if self.part != 2:
            if (self.posx + FU.convert(584) <= mouse[0] <=
                self.posx + FU.convert(634) and
                    self.posy + FU.convert(161) <= mouse[1] <=
                    self.posy + FU.convert(211)):

                self.part = 2
                self.reset_crafting()

    def get_crafting_table(self):
        table = [[None for j in range(4)]for i in range(4)]
        for i in range(4):
            for j in range(4):
                item = self.crafting_table[i][j][0]
                if item:
                    table[i][j] = item.name

        return table

    def verif_craft(self):
        craft = self.crafts.craft(self.get_crafting_table())
        if craft:
            if craft in FU.item_class.get("item"):
                self.crafted = item.Item(craft, 1)
            if craft in FU.item_class.get("weapons"):
                self.crafted = item.Item_weapons(craft)
            if craft in FU.item_class.get("armor"):
                self.crafted = item.Item_armor(craft)

        else:
            self.crafted = None

    def get_armor(self):
        return_val = 0
        for nom, value in self.equiped.items():
            if (value[0] and nom == "chesplate" or nom == "feets" or
                    nom == "gloves" or nom == "helmet" or
                    nom == "legs") and value[0]:
                return_val += FU.armor_value.get(value[0].name)

        return return_val

    def aug_arrow(self, nb):
        arrow = self.equiped.get("arrow")[0]
        if not arrow:
            self.equiped["arrow"][0] = item.Item("arrow", 1)

        else:
            arrow.aug_quantity(nb)

    def dim_arrow(self, nb):
        arrow = self.equiped.get("arrow")[0]
        if arrow:
            arrow.dim_quantity(nb)

            if arrow.quantity <= 0:
                self.equiped["arrow"][0] = None

    def pick_item_inventory(self, x, y):
        self.last_pos_hand = ("inventory", (x, y))
        self.hand = self.inventory[y][x][0]
        self.inventory[y][x][0] = None

    def pick_item_equiped(self, x, y):
        self.sound[0].play()
        part = self.equiped_lst[y][x]
        self.last_pos_hand = ("equiped", (x, y))
        self.hand = self.equiped.get(part)[0]
        self.equiped[part][0] = None

    def drop_item_inventory(self, x, y):
        if self.hand:
            if 0 <= x <= 7 and 0 <= y <= 2 and not self.inventory[y][x][0]:
                self.inventory[y][x][0] = self.hand

            elif 0 <= x <= 7 and 0 <= y <= 2 and self.inventory[y][x][0]:
                if (self.inventory[y][x][0].type == "item" and
                        self.hand.name == self.inventory[y][x][0].name):
                    self.inventory[y][x][0].aug_quantity(self.hand.quantity)

                elif self.last_pos_hand[0] == "inventory":
                    temp = self.inventory[y][x][0]
                    self.inventory[y][x][0] = self.hand
                    self.inventory[self.last_pos_hand[1][1]
                                   ][self.last_pos_hand[1][0]][0] = temp

                elif self.inventory[y][x][0].type == self.hand.type:
                    self.equiped[self.hand.type][0] = self.inventory[y][x][0]
                    self.inventory[y][x][0] = self.hand

                elif self.last_pos_hand[0] == "crafting":
                    temp = self.inventory[y][x][0]
                    self.inventory[y][x][0] = self.hand
                    self.crafting_table[self.last_pos_hand[1][1]
                                        ][self.last_pos_hand[1][0]][0] = temp

                elif self.last_pos_hand[0] == "crafted":
                    if self.hand:
                        i = 0
                        while i < 3:
                            for j in range(8):
                                if not self.inventory[i][j][0]:
                                    self.inventory[i][j][0] = self.hand
                                    self.hand = None
                                    i = 3
                                    break
                            i += 1

                else:
                    self.equiped[self.hand.type][0] = self.hand

            else:
                if self.last_pos_hand[0] == "inventory":
                    self.inventory[self.last_pos_hand[1][1]
                                   ][self.last_pos_hand[1][0]][0] = self.hand

                elif self.last_pos_handt_pos_hand[0] == "crafting":
                    self.crafting_table[self.last_pos_hand[1][1]
                                        ][self.last_pos_hand[1][0]][0] = self.hand
                else:
                    self.equiped[self.hand.type][0] = self.hand

            self.hand = None

    def drop_item_equiped(self, x, y):
        if self.hand:
            self.sound[1].play()
            part = self.equiped_lst[y][x]
            if self.hand.type == part:
                if self.last_pos_hand[0] == "equiped":
                    self.equiped[self.hand.type][0] = self.hand

                else:
                    self.inventory[self.last_pos_hand[1][1]
                                   ][self.last_pos_hand[1][0]][0] = self.equiped[
                                       part][0]

                    self.equiped[part][0] = self.hand

            elif self.last_pos_hand[0] == "inventory":
                self.inventory[self.last_pos_hand[1][1]
                               ][self.last_pos_hand[1][0]][0] = self.hand

            else:
                self.equiped[self.hand.type][0] = self.hand

            self.hand = None

    def pick_item_crafting(self, x, y):
        self.last_pos_hand = ("crafting", (x, y))
        self.hand = self.crafting_table[y][x][0]
        self.crafting_table[y][x][0] = None
        self.verif_craft()

    def drop_item_crafting(self, x, y):
        if self.hand:
            if 0 <= x <= 3 and 0 <= y <= 3 and not self.crafting_table[y][x][0]:
                self.crafting_table[y][x][0] = self.hand

            elif 0 <= x <= 3 and 0 <= y <= 3 and self.crafting_table[y][x][0]:
                if (self.hand.name == self.crafting_table[y][x][0].name and
                        self.crafting_table[y][x][0].type == "item"):
                    self.crafting_table[y][x][0].aug_quantity(
                        self.hand.quantity)

                elif self.last_pos_hand[0] == "inventory":
                    temp = self.crafting_table[y][x][0]
                    self.crafting_table[y][x][0] = self.hand
                    self.inventory[self.last_pos_hand[1][1]
                                   ][self.last_pos_hand[1][0]][0] = temp

                elif self.last_pos_hand[0] == "crafting":
                    temp = self.crafting_table[y][x][0]
                    self.crafting_table[y][x][0] = self.hand
                    self.crafting_table[self.last_pos_hand[1][1]
                                        ][self.last_pos_hand[1][0]][0] = temp

                elif self.last_pos_hand[0] == "crafted":
                    if self.hand:
                        i = 0
                        while i < 3:
                            for j in range(8):
                                if not self.inventory[i][j][0]:
                                    self.inventory[i][j][0] = self.hand
                                    self.hand = None
                                    i = 3
                                    break
                            i += 1

            else:
                if self.last_pos_hand[0] == "inventory":
                    self.inventory[self.last_pos_hand[1][1]
                                   ][self.last_pos_hand[1][0]][0] = self.hand
                else:
                    self.crafting_table[self.last_pos_hand[1][1]
                                        ][self.last_pos_hand[1][0]][0] = self.hand

            self.hand = None
            self.verif_craft()

    def pick_item_crafted(self):
        if self.crafted:
            self.hand = self.crafted
            self.last_pos_hand = ("crafted", (0, 0))
            self.crafted = None

            for i in range(4):
                for j in range(4):
                    item = self.crafting_table[i][j][0]
                    if item:
                        if item.type == "item":
                            item.dim_quantity(1)
                            if item.quantity == 0:
                                self.crafting_table[i][j][0] = None
                        else:
                            self.crafting_table[i][j][0] = None

            self.verif_craft()

    def drop_1_item_inventory(self, x, y):
        if self.hand:
            if 0 <= x <= 7 and 0 <= y <= 2 and not self.inventory[y][x][0]:
                if self.hand.type != "item":
                    self.inventory[y][x][0] = self.hand
                    self.hand = None

                else:
                    if self.hand.quantity == 1:
                        self.inventory[y][x][0] = self.hand
                        self.hand = None

                    else:
                        self.inventory[y][x][0] = item.Item(
                            self.hand.name, 1)
                        self.hand.dim_quantity(1)
                        if self.hand.quantity == 0:
                            self.hand = None

            elif 0 <= x <= 7 and 0 <= y <= 2 and self.inventory[y][x][0]:
                if (self.inventory[y][x][0].type == "item" and
                        self.hand.name == self.inventory[y][x][0].name):
                    self.inventory[y][x][0].aug_quantity(1)
                    self.hand.dim_quantity(1)
                    if self.hand.quantity == 0:
                        self.hand = None

    def drop_1_item_crafting(self, x, y):
        if self.hand:
            if 0 <= x <= 3 and 0 <= y <= 3 and not self.crafting_table[y][x][0]:
                if self.hand.type != "item":
                    self.crafting_table[y][x][0] = self.hand
                    self.hand = None

                else:
                    if self.hand.quantity == 1:
                        self.crafting_table[y][x][0] = self.hand
                        self.hand = None

                    else:
                        self.crafting_table[y][x][0] = item.Item(
                            self.hand.name, 1)
                        self.hand.dim_quantity(1)
                        if self.hand.quantity == 0:
                            self.hand = None

            elif 0 <= x <= 3 and 0 <= y <= 3 and self.crafting_table[y][x][0]:
                if (self.crafting_table[y][x][0].type == "item" and
                        self.hand.name == self.crafting_table[y][x][0].name):
                    self.crafting_table[y][x][0].aug_quantity(1)
                    self.hand.dim_quantity(1)
                    if self.hand.quantity == 0:
                        self.hand = None

            self.verif_craft()

    def shift_item_inventory(self, x, y):
        part = self.inventory[y][x][0]
        if (isinstance(part, item.Item_armor) or
                isinstance(part, item.Item_weapons)):
            if self.equiped.get(part.type):
                temp = self.equiped.get(part.type)[0]
            else:
                temp = None
            self.equiped[part.type][0] = part
            self.inventory[y][x][0] = temp

        elif part and part.name == "arrow":
            self.aug_arrow(part.quantity)
            self.inventory[y][x][0] = None

        else:
            i = 0
            while i < 3:
                for j in range(8):
                    if not self.inventory[i][j][0]:
                        self.inventory[i][j][0] = self.inventory[y][x][0]
                        self.inventory[y][x][0] = None
                        i = 3
                        break
                i += 1

    def shift_item_equiped(self, x, y):
        part = self.equiped.get(self.equiped_lst[y][x])[0]
        if part:
            i = 0
            while i < 3:
                for j in range(8):
                    if not self.inventory[i][j][0]:
                        self.inventory[i][j][0] = part
                        self.equiped[part.type][0] = None
                        i = 3
                        break
                i += 1

    def shift_item_crafting(self, x, y):
        item = self.crafting_table[y][x][0]
        found = False
        if item:
            i = 0
            while i < 3 and not found:
                for j in range(8):
                    item_i = self.inventory[i][j][0]
                    if (item_i and item_i.name == item.name and
                            item.type == "item"):
                        self.inventory[i][j][0].aug_quantity(item.quantity)
                        self.crafting_table[y][x][0] = None
                        found = True
                        break
                i += 1

            if not found:
                i = 0
                while i < 3:
                    for j in range(8):
                        if not self.inventory[i][j][0]:
                            self.inventory[i][j][0] = item
                            self.crafting_table[y][x][0] = None
                            i = 3
                            break
                    i += 1

    def shift_item_crafted(self):
        item = self.crafted
        found = False
        if item:
            i = 0
            while i < 3 and not found:
                for j in range(8):
                    item_i = self.inventory[i][j][0]
                    if (item_i and item_i.name == item.name and
                            item.type == "item"):
                        self.inventory[i][j][0].aug_quantity(item.quantity)
                        self.crafted = None
                        found = True
                        break
                i += 1

            if not found:
                i = 0
                while i < 3:
                    for j in range(8):
                        if not self.inventory[i][j][0]:
                            self.inventory[i][j][0] = item
                            self.crafted = None
                            i = 3
                            break
                    i += 1

            for i in range(4):
                for j in range(4):
                    item = self.crafting_table[i][j][0]
                    if item:
                        if item.type == "item":
                            item.dim_quantity(1)
                            if item.quantity == 0:
                                self.crafting_table[i][j][0] = None
                        else:
                            self.crafting_table[i][j][0] = None

            self.verif_craft()

    def close_inv(self):
        self.reset_crafting()
        self.verif_craft()
        self.part = 0

    def reset_crafting(self):
        for i in range(4):
            for j in range(4):
                item = self.crafting_table[i][j][0]
                if item:
                    found = False
                    a = 0
                    while a < 3 and not found:
                        for b in range(8):
                            item_i = self.inventory[a][b][0]
                            if (item_i and item_i.name == item.name and
                                    item.type == "item"):
                                self.inventory[a][b][0].aug_quantity(
                                    item.quantity)
                                self.crafting_table[i][j][0] = None
                                found = True
                                break
                        a += 1

                    if not found:
                        a = 0
                        while a < 3:
                            for b in range(8):
                                if not self.inventory[a][b][0]:
                                    self.inventory[a][b][0] = item
                                    self.crafting_table[i][j][0] = None
                                    a = 3
                                    break
                            i += 1

    def reste_hand(self):
        if self.last_pos_hand[0] == "inventory":
            self.inventory[self.last_pos_hand[1][1]
                           ][self.last_pos_hand[1][0]][0] = self.hand

        elif self.last_pos_hand[0] == "equiped":
            self.equiped[self.hand.type][0] = self.hand

        elif self.last_pos_hand[0] == "crafting":
            self.crafting_table[self.last_pos_hand[1][1]
                                ][self.last_pos_hand[1][0]][0] = self.hand

        elif self.last_pos_hand[0] == "crafted":
            if self.hand:
                i = 0
                while i < 3:
                    for j in range(8):
                        if not self.inventory[i][j][0]:
                            self.inventory[i][j][0] = self.hand
                            self.hand = None
                            i = 3
                            break
                    i += 1

        self.verif_craft()
        self.hand = None

    def init_inventory(self):
        self.inventory[0][0][0] = item.Item_armor("helmet_leather")
        self.inventory[0][1][0] = item.Item_weapons("belt_rope")
        self.inventory[0][2][0] = item.Item_armor("helmet_chain")
        self.inventory[0][3][0] = item.Item_armor("hood_leather")
        self.inventory[0][4][0] = item.Item_armor("hood_chain")
        self.inventory[0][5][0] = item.Item_armor("feet_leather")
        self.inventory[0][6][0] = item.Item_armor(
            "chestplate_leather")
        self.inventory[0][7][0] = item.Item_armor(
            "chestplate_chain")

        self.inventory[1][0][0] = item.Item_armor(
            "chestplate_brown")
        self.inventory[1][1][0] = item.Item_armor(
            "chestplate_white")
        self.inventory[1][2][0] = item.Item_armor("legs_leather")
        self.inventory[1][3][0] = item.Item_weapons("dagger")
        self.inventory[1][4][0] = item.Item_weapons("spear")
        self.inventory[2][0][0] = item.Item("stick", 100)
        self.inventory[2][1][0] = item.Item("string", 100)
        self.inventory[2][2][0] = item.Item("rope", 50)
        self.inventory[2][3][0] = item.Item("rope", 50)
        self.inventory[2][4][0] = item.Item("rope", 50)
        self.inventory[2][5][0] = item.Item("rope", 50)

    def init_stuff(self):
        self.equiped = {"quiver": [item.Item_weapons("quiver"),
                                   (self.posx + FU.convert(442),
                                    self.posy + FU.convert(174))],
                        "feets": [item.Item_armor("feet_metal"),
                                  (self.posx + FU.convert(77),
                                   self.posy + FU.convert(241))],
                        "legs": [item.Item_armor("legs_metal"),
                                 (self.posx + FU.convert(77),
                                  self.posy + FU.convert(174))],
                        "chestplate": [item.Item_armor("chestplate_metal"),
                                       (self.posx + FU.convert(77),
                                        self.posy + FU.convert(107))],
                        "belt": [item.Item_weapons("belt_leather"),
                                 (self.posx + FU.convert(342),
                                  self.posy + FU.convert(107))],
                        "helmet": [item.Item_armor("helmet_metal"),
                                   (self.posx + FU.convert(77),
                                    self.posy + FU.convert(40))],
                        "gloves": [item.Item_armor("gloves"),
                                   (self.posx + FU.convert(342),
                                    self.posy + FU.convert(40))],
                        "arrow":  [item.Item("arrow", 20),
                                   (self.posx + FU.convert(442),
                                    self.posy + FU.convert(241))],
                        "weapons": [item.Item_weapons("bow"),
                                    (self.posx + FU.convert(342),
                                     self.posy + FU.convert(241))],
                        "sheild": [item.Item_weapons("sheild1"),
                                   (self.posx + FU.convert(342),
                                    self.posy + FU.convert(174))]}
