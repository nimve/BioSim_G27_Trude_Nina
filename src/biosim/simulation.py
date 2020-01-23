# -*- coding: utf-8 -*-


__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

"""
Implements a biological simulation of an island with population of herbivores
and carnivores. Landscape types consist of savannah, jungle, desert and
mountain, with surrounding ocean.
"""

from src.biosim.animals import Herbivore, Carnivore
from src.biosim.landscapes import Savannah, Jungle, Desert, Mountain, Ocean
from src.biosim.visualization import Visualization as Vis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class BioSim:
    """Define and run a biological simulation. """

    def __init__(
            self,
            island_map=None,
            ini_pop=None,
            seed=None,
            ymax_animals=None,
            cmax_animals=None,
            img_base=None,
            img_fmt=None
            ):

        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing
        animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal
        densities
        :param img_base: String with beginning of file name for figures,
        including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        """
        self.land_dict = {'S': Savannah, 'J': Jungle, 'O': Ocean, 'M':
                          Mountain, 'D': Desert}
        self.active = {Savannah: 0, Jungle: 0, Desert: 0}
        self._year = 0
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals

        self.num_years = 0
        self.vis_years = 0
        self.img_years = 0
        self.sim_years = 0

        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals

        self.num_animals_results = []
        self.per_species_results = []
        self.island_map = island_map
        self.map = self.str_to_dict(island_map)
        self.map_active = {key: value for (key, value) in self.map.items() if
                           type(value) in self.active}
        self.map_full = self.map.copy()
        self.map = self.map_active
        if ini_pop is not None:
            self.add_population(ini_pop)
        self.Vis = Vis(self, cmax_animals, ymax_animals, img_base, img_fmt)

    def str_to_dict(self, txt):
        """
        Turn string into dictionary if requirements for a map string are met.

        :param txt: String of letters, each signifying the type of landscape at
         corresponding location.
        :return: dict: Dictionary with tuples of y- and x-coordinate as keys,
        and instance of landscape class as values
        """
        txt = txt.split('\n')
        if not txt[-1].isalpha():
            txt.pop()
        self.check_txt(txt)
        y = 0
        dict = {}
        for row in txt:
            x = 0
            for letter in row:
                dict[(y, x)] = self.land_dict[letter]()
                x += 1
            y += 1
        return dict

    def check_txt(self, txt):
        """
        Check if string meets requirements for a map string.

        :param txt: String of letters
        """

        left_column = [line[0] for line in txt]
        right_column = [line[-1] for line in txt]
        to_check = [txt[0], txt[-1], left_column, right_column]
        for list in to_check:
            for element in list:
                if element != 'O':
                    raise ValueError
        for line in txt:
            if len(line) != len(txt[0]):
                raise ValueError
        for row in txt:
            for letter in row:
                if letter not in self.land_dict:
                    raise ValueError

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        self.name = species
        eval(species).set_params(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        self.land_dict[landscape].set_params(params)

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying charactersitics of
        individual animals to be added
        """
        for loc_dict in population:
            if loc_dict['loc'] not in self.map:
                raise ValueError
            loc = self.map[loc_dict['loc']]
            loc.place_animals(loc_dict['pop'])

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @year.setter
    def year(self, n):
        self._year += n

    @property
    def num_animals(self):
        """Total number of animals on island."""
        num_animals = 0
        for cell in self.map.values():
            num_animals += len(cell.population['Herbivore']) + \
                           len(cell.population['Carnivore'])
        return num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        _num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.map.values():
            for species in cell.population:
                _num_animals_per_species[species] += len(
                    cell.population[species])
        return _num_animals_per_species

    @property
    def animal_distribution(self):
        self.map_full.update(self.map)
        y = [cell[0] for cell in self.map_full]
        x = [cell[1] for cell in self.map_full]

        dictionary = {}
        for cell in self.map_full.values():
            herbivore = 0
            carnivore = 0
            for species in cell.population:
                if species == 'Herbivore':
                    herbivore += len(cell.population[species])
                if species == 'Carnivore':
                    carnivore += len(cell.population[species])
            dictionary[cell] = herbivore, carnivore

        herbivores = \
            [dictionary[cell][0] for cell in dictionary]
        carnivores = \
            [dictionary[cell][1] for cell in dictionary]

        data = {'Row': y, 'Col': x,
                'Herbivore': herbivores, 'Carnivore': carnivores}
        df = pd.DataFrame(data)
        return df

    def all_cells(self, myfunc):
        """
        Execute method for every active location.

        :param myfunc: Method to be executed
        """
        for cell in self.map.values():
            getattr(cell, myfunc)()

    def all_animals(self, myfunc):
        """
        Execute method for every individual animal.

        :param myfunc: Method to be executed.
        """

        for cell in self.map.values():
            for species in cell.population:
                for animal in cell.population[species]:
                    getattr(animal, myfunc)()

    def migration(self):
        """Execute migration step of annual cycle."""

        for pos, cell in self.map.items():
            if type(cell) == Ocean or type(cell) == Mountain:
                pass
            else:
                y, x = pos
                adjecent_pos = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
                map_list = [self.map[element] for element in adjecent_pos if
                            element in self.map]
                copy = map_list
                for element in copy:
                    if type(element) == Ocean or type(element) == Mountain:
                        map_list.remove(element)
                cell.migration(map_list)

    def one_year(self):
        """ Implement one annual cycle. """
        self.all_cells('replenish')
        self.all_cells('feeding')
        self.all_cells('procreation')
        self.migration()
        self.all_animals('aging')
        self.all_animals('weightloss')
        self.all_cells('dying')
        self.num_animals_results.append(self.num_animals)
        self.per_species_results.append(self.num_animals_per_species)
        self.year = 1

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
        (default: vis_years)

        Image files will be numbered consecutively.
        """
        self.num_years = num_years
        self.vis_years = vis_years
        self.img_years = img_years
        self.sim_years = 0

        self.num_animals_results = []
        self.per_species_results = []
        self.Vis.visualize(vis_years)

        while (self.sim_years < self.num_years):
            self.one_year()
            self.sim_years += 1
            self.Vis.update_graphics()
            self.Vis._save_graphics()
        #self.Vis.make_movie()
