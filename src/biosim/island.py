# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


# import animal.py
import numpy as np
from math import exp
import random
from landscapes import Savannah, Jungle, Ocean, Mountain, Desert
from animals import Herbivore, Carnivore, bubble_sort_animals


class Cell:
    land_dict = {'S': Savannah, 'J': Jungle, 'O': Ocean, 'M': Mountain,
                     'D': Desert}


    def __init__(self, y, x, letter):
        self.landscape = self.land_dict[letter]()
        # self.y = y
        # self.x = x
        self.pos = (y, x) # using this
        self.pop = []
        self.tot_w_herbivores = sum([animal.weight for animal in self.pop if type(animal)==Herbivore])

    def num_specimen(self, species):  # privat? burde kanskje være utenfor?
        n = 0
        for animal in self.pop:
            if type(animal) == species:
                n += 1
        return n

    def get_rel_abundance(self, animal): # er noe kluss med at fodder avhenger av art
        if type(animal) == Herbivore:
            fodder = self.landscape.f
        if type(animal) == Carnivore:
            fodder = self.tot_w_herbivores
        N = self.num_specimen(type(animal))
        return fodder / ((N + 1) * animal.F)

class AdjacentCell(Cell):
    total_propensity = 0
    total_probability = 0
    remembered_limit = 0

    def __init__(self, y, x, letter):
        super().__init__(y, x, letter)
        self.propensity = None
        self.probability = None
        self.lower_limit = 0
        self.upper_limit = 0

class Island:
    land_dict = {'S': Savannah, 'J': Jungle,
                 'O': Ocean, 'M': Mountain, 'D': Desert}
    def string_to_array(self, txt):
        # bør kanskje importeres
        if txt[-1] is not "\n":
            txt += "\n"
        line, lines = [], []
        y, x = 0, 0
        for letter in txt:
            if letter in self.land_dict:
                line.append(letter)
                x += 1
            if letter == "\n":
                lines.append(line)
                line = []
                y += 1
                x = 0
        return np.asarray(lines)

    def check_edges(self):
        left_column = [line[0] for line in self.map]
        right_column = [line[-1] for line in self.map]
        to_check = [self.map[0], self.map[-1], left_column, right_column]
        for list in to_check:
            for element in list:
                if element != 'O':
                    raise ValueError



    def get_propensity(self, animal, rel_abund):
        """
        if type(cell) == Mountain or type(cell) == Ocean: # unødvendig fordi de ikke ble lagt til i adj-lista?
            return 0

        else:
        """
        return exp(animal.lambdah * rel_abund)

    def __init__(self, txt=None):
        if txt is None:
            txt = open('rossum.txt').read()
            if txt[-1] == "\n":
                #legg inn noe som fjerner siste element hvis det er formen vi vil ha det på senere
                pass
        self.map = self.string_to_array(txt) # array of one-letter-strings
        self.check_edges()
        # creating array of cells
        island_line = []
        island_lines = []
        for y, line in enumerate(self.map):
            for x, letter in enumerate(line):
                island_line.append(Cell(y, x, letter))
            island_lines.append(island_line)
            island_line = []
        self.map = np.array(island_lines)

    def place_animals(self, input_list):
        ani_dict = {'Herbivore': Herbivore, 'Carnivore': Carnivore}
        for placement_dict in input_list:
                y, x = placement_dict['loc']
                for individual in placement_dict['pop']:
                    self.map[y][x].pop.append(ani_dict[individual['species']](individual))

    def remove_animal(self, cell, animal):
        cell.pop.remove(animal)

    def choose_new_cell(self, cell, animal):
        AdjacentCell.total_propensity = 0
        AdjacentCell.total_probability = 0
        active = {Savannah: 'S', Jungle : 'J', Desert : 'D'}
        # N = cell.num_specimen(type(animal))
        adj_cells = []
        y, x = cell.pos
        possible_cells = [self.map[y-1][x], self.map[y+1][x], self.map[y][x-1], self.map[y][x+1]]
        for element in possible_cells:
            if type(element.landscape)==Ocean:
                possible_cells.remove(element)
            elif type(element.landscape) == Mountain:
                possible_cells.remove(element)
        if len(possible_cells) == 0:
            return False
        elif len(possible_cells) == 1:
            return possible_cells[0]
        total_propensity = 0
        temp_dict = {}
        for element in possible_cells:
            rel_abund = element.get_rel_abundance(animal)
            temp_dict[element] ={'propensity': exp(animal.lambdah * rel_abund)}
        total_propensity = sum([temp_dict[element]['propensity'] for element in temp_dict])
        keys = temp_dict.keys()
        for key in keys:
            temp_dict[key]['probability'] = temp_dict[key]['propensity'] / total_propensity
        remembered_limit = 0
        for key in keys:
            temp_dict[key]['lower_limit'] = remembered_limit
            temp_dict[key]['upper_limit'] = remembered_limit + temp_dict[key]['probability']
            remembered_limit = temp_dict[key]['upper_limit']
            # print('Lower: ', temp_dict[key]['lower_limit'], 'Upper: ', temp_dict[key]['upper_limit'])
        number = round(random.random(), 7)
        for key in keys:
            if temp_dict[key]['lower_limit'] < number < temp_dict[key]['upper_limit']:
                return key


    def move_animal(self, old_cell, new_cell, animal):
        new_cell.pop.append(animal)
        old_cell.pop.remove(animal)