# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import inspect
from math import exp
import numpy as np
from pytest import approx
import random
import src.biosim.animals as animals
from .animals import Herbivore, Carnivore


class LandscapeCell:
    def __init__(self):
        self.f = 0
        self.species_to_class = dict(inspect.getmembers(animals, inspect.isclass))
        del self.species_to_class['Animal']
        self.pop = {'Herbivore': [], 'Carnivore': []}
        self.tot_w_herbivores = \
            sum([herbivore.weight for herbivore in self.pop['Herbivore']])

    def num_specimen(self, species):
        return len(self.pop[species])


    @property
    def num_animals_per_species(self):
        num_dict = {}
        for species in self.pop:
            num_dict[species] = len(self.pop[species])
        return num_dict

    @property
    def num_animals(self):
        total = 0
        for species in self.pop:
            total += len(self.pop[species])
        return total

    @property
    def rel_abundance(self):
        animal = Herbivore()
        animaltype = type(animal)
        fodder = 0
        if animaltype == Herbivore:
            fodder = self.f

        elif animaltype == Carnivore:
            fodder = self.tot_w_herbivores

        n = self.num_specimen(animaltype.__name__)

        return fodder / ((n + 1) * animal.F)


    @property
    def propensity(self):
        return self._propensity

    @propensity.setter
    def propensity(self, animal):
        if type(self) == Ocean:
            self._propensity = 0
        elif type(self) == Mountain:
            self._propensity = 0
        else:
            self._propensity = exp(animal.lambdah * self.rel_abundance)

    @property
    def likelihood(self):
        return self._likelihood

    @likelihood.setter
    def likelihood(self, total):
        self._likelihood = self._propensity / total


    def migration(self, map_list):
        for species in self.pop:
            for animal in self.pop[species]:
                if len(map_list) == 0:
                    pass
                elif len(map_list) == 1:
                    animal.move(self, map_list[0])
                else:
                    new_cell = self.new_cell(animal, map_list)
                    animal.move(self, new_cell)

    def new_cell(self, animal, map_list):
        for cell in map_list:
            cell.propensity = animal # setter verdi
        total_propensity = sum([cell.propensity for cell in map_list])
        for cell in map_list:
            cell.likelihood = total_propensity
        if not sum([cell.likelihood for cell in map_list]) == approx(1):
            print('Probabilities do not add up: ', sum([cell.likelihood for cell in map_list]))
        upper_limits = np.cumsum([cell.likelihood for cell in map_list])
        r = random.random()
        for i in range(len(upper_limits)):
            if r <= upper_limits[i]:
                return map_list[i]

    def place_animals(self, pop_list):
        for individual_dict in pop_list:
            if individual_dict['species'] not in self.pop:
                self.pop[individual_dict['species']] = []
            new_animal = eval(individual_dict['species'])(individual_dict)
            self.pop[individual_dict['species']].append(new_animal)
            if individual_dict['species'] == 'Herbivore':
                self.tot_w_herbivores += new_animal.weight

    def replenish(self):
        pass

    def feeding(self):
        for species in self.pop:
            self.pop[species] = sorted(self.pop[species], key=lambda x: getattr(x, 'phi'))
        for herbivore in self.pop['Herbivore']:
            herbivore.feeding(self)
        for carnivore in self.pop['Carnivore']:
            carnivore.feeding(self)

    def procreation(self):
        for species, pop_list in self.pop.items():
            copy = pop_list
            for animal in copy:
                n = self.num_specimen(species)
                if n >= 2:
                    if animal.fertile(n):
                        newborn = type(animal)()
                        if animal.weight >= animal.zeta * (newborn.weight + animal.sigma_birth):
                            q = len(pop_list)
                            self.pop[species].append(newborn)
                            if len(pop_list) <= q:
                                print('Pop list not updated')
                            animal.weight -= animal.zeta * newborn.weight
                            if animal.weight <0:
                                print('animal weight too small after birth')

    def dying(self):
        for species in self.pop:
            self.pop[species] = [animal for animal in self.pop[species] if not animal.dies()]

class Savannah(LandscapeCell):
    params = {'f_max': 300.0, 'alpha': 0.3}
    params_set = False

    def __init__(self, param_dict=None):
        super().__init__()
        if self.params_set is False:
            for param in self.params:
                exec("self.%s = %s" % (param, self.params[param]))
            self.f = self.f_max


    @classmethod
    def set_parameter(cls, new_params):
        print (cls.params)
        if new_params is not None:
            cls.params.update(new_params)
        for param in cls.params:
            exec("cls.%s = %s" % (param, cls.params[param]))
        cls.params_set = True

    def replenish(self):
        self.f = self.alpha * (self.f_max - self.f) + self.f




class Jungle(LandscapeCell):
    params = {'f_max': 800.0}
    params_set = False

    def __init__(self, param_dict=None):
        super().__init__()
        if self.params_set is False:
            for param in self.params:
                exec("self.%s = %s" % (param, self.params[param]))
            self.f = self.f_max


    @classmethod
    def set_parameter(cls, new_params):
        if new_params is not None:
            cls.params.update(new_params)
        for param in cls.params:
            exec("cls.%s = %s" % (param, cls.params[param]))
        cls.params_set = True


    def replenish(self):
        self.f = self.f_max


class Desert(LandscapeCell):
    def __init__(self):
        super().__init__()
        self.f = 0


class Ocean(LandscapeCell):
    def __init__(self):
        super().__init__()


class Mountain(LandscapeCell):
    def __init__(self):
        super().__init__()
