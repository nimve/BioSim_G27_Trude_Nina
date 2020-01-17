# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import inspect
import numpy as np
from .landscapes import Savannah, Jungle, Ocean, Mountain, Desert
from .animals import Herbivore, Carnivore
import src.biosim.animals as animals

class Island:
    # ta høyde for store og små bokstaver
    land_dict = {'S': Savannah, 'J': Jungle,
                 'O': Ocean, 'M': Mountain, 'D': Desert}

    def str_to_dict(self, txt):
        # burde ha check_edges som en egen funksjon?
        # print(txt)
        txt = txt.split('\n')
        if txt[-1] == '\n':
            txt = txt.pop()
        #self.check_letters(txt)
        self.check_edges(txt)
        #self.check_letters(txt)
        valid = ['O', 'S', 'J', 'D', 'M']
        for row in txt:
            for letter in row:
                if letter not in valid:
                    raise ValueError

        y = 0
        dict = {}
        for row in txt:
            x = 0
            for letter in row:
                dict[(y, x)] = self.land_dict[letter]()
                x += 1
            y += 1
        return dict


    def check_letters(self, txt):
        valid = ['O', 'S', 'J', 'D', 'M']
        length_line = []
        for line in txt:
            length_line.append(len(line))
            for letter in txt:
                if letter not in valid:
                    raise ValueError
                if [length for length in length_line] != len(line):
                    raise ValueError


    def check_edges(self, txt):

        left_column = [line[0] for line in txt]
        right_column = [line[-1] for line in txt]
        to_check = [txt[0], txt[-1], left_column, right_column]
        for list in to_check:
            for element in list:
                if element != 'O':
                    raise ValueError



    def __init__(self, txt=None):
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        if txt is None:
            txt = open('rossum.txt').read()  # med \n som siste argument
        self.map = self.str_to_dict(txt)


    def all_cells(self, myfunc):
        for cell in self.map.values():
            getattr(cell, myfunc)()

    def all_animals(self, myfunc):
        for cell in self.map.values():
            for species in cell.pop:
                for animal in cell.pop[species]:
                    getattr(animal, myfunc)()

    def place_animals(self, input_list):
        for placement_dict in input_list:
            pos = placement_dict['loc'] # bør flytte resten til celle?
            self.map[pos].place_animals(placement_dict['pop'])

    def migration(self): # husk filtering
        for pos, cell in self.map.items():
            if type(cell) == Ocean or type(cell) == Mountain:
                pass
            else:
                y, x = pos
                adjecent_pos = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)] # må ta høyde for edges
                map_list = [self.map[element] for element in adjecent_pos]
                for element in map_list:
                    if type(element) == Ocean or type(element) == Mountain:
                        map_list.remove(element)
                cell.migration(map_list)

    def update_num_animals(self):
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.map.values(): # bør kunne flyttes inn
            self.num_animals += cell.num_animals()
            for species in self.num_animals_per_species:
                self.num_animals_per_species[species] +=\
                    cell.num_animals_per_species()[species]

    def update_change(self):
        corpses = 0
        newborns = 0
        for cell in self.map.values():
            corpses += cell.corpses
            newborns += cell.newborns
        return corpses, newborns
