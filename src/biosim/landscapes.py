# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

from src.biosim.animals import Herbivore, Carnivore

class LandscapeCell:
    """Create landscape cells that can be replensihed and with a population of
    herbivore and carnivores. Placement, migration, feeding, procreation and
    death of the animals can be executed. """

    def __init__(self):
        self.params_set = False
        self.f = 0
        self.population = {'Herbivore': [], 'Carnivore': []}
        self.propensity = 0
        self.likelihood = 0

    @classmethod
    def set_params(cls, new_params=None):
        if new_params is not None:
            for param in new_params:
                if param not in cls.params:
                    raise ValueError
                if param == 'f_max' and new_params[param] < 0:
                    raise ValueError
            cls.params.update(new_params)
        for param in cls.params:
            setattr(cls, param, cls.params[param])
        cls.params_set = True

    def num_specimen(self, species):
        """Get the number of individuals of a species in the population of
        the cell.

        :param species: String with the name of the species
        :return: Integer signifying the number of individuals of the species.
        """
        return len(self.population[species])

    @property
    def tot_w_herbivores(self):
        return sum([herbivore.weight for herbivore in
                    self.population['Herbivore']])

    def migration(self, neighbours):
        """
        Move each animal if the conditions dictate so.

        :param neighbours: List of potential destinations for animal
        """
        for species in self.population:
            for animal in self.population[species]:
                if animal.movable():
                    animal.migrate(self, neighbours)

    def place_animals(self, placement_list):
        """
        Place animals at specific locations.

        :param pop_list: List of dictionaries, each dictionary specifying
        characteristics of the individual animal to be placed.
        """

        for individual_dict in placement_list:
            if individual_dict['age'] < 0:
                raise ValueError
            if individual_dict['weight'] <= 0:
                raise ValueError
            new_animal = eval(individual_dict['species'])(individual_dict)
            self.population[individual_dict['species']].append(new_animal)

    def replenish(self):
        """Replenish plant fodder if required. """
        pass

    def feeding(self):
        """ Carry out feeding of each animal in the cell. """

        for species in self.population:
            self.population[species] = sorted(self.population[species],
                                              key=lambda x: getattr(x, 'phi'))
        for herbivore in self.population['Herbivore']:
            herbivore.feeding(self)
        for carnivore in self.population['Carnivore']:
            carnivore.feeding(self)

    def procreation(self):
        """Carry out procreation of animals in the cell. """

        for species, pop_list in self.population.items():
            n = self.num_specimen(species)
            copy = pop_list
            for animal in copy:
                if n >= 2:
                    if animal.fertile(n):
                        animal.procreate(self)

    def dying(self):
        """
        Remove dying animals from population.
        """

        for species in self.population:
            if len(self.population[species]) > 0:
                self.population[species] =\
                    [animal for animal in self.population[species] if
                                            not animal.dies()]


class Savannah(LandscapeCell):
    """Create a savannah cell that can be replenshed. """

    params = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self, new_params=None):
        super().__init__()
        if not self.params_set:
            self.set_params()
            self.params_set = True

        self.f = self.f_max


    def replenish(self):
        """Replenish plant fodder at the start of every season. """

        self.f = self.alpha * (self.f_max - self.f) + self.f


class Jungle(LandscapeCell):
    """Create a jungle cell that can be replenished. """

    params = {'f_max': 800.0}

    def __init__(self, param_dict=None):
        super().__init__()
        if not self.params_set:
            self.set_params()

        self.f = self.f_max

    def replenish(self):
        """Replenish plant fodder at the start of every season. """

        self.f = self.f_max


class Desert(LandscapeCell):
    """Create a desert cell that animals can be in, but no plant fodder is
    available."""

    def __init__(self):
        super().__init__()
        self.f = 0


class Ocean(LandscapeCell):
    """Create an ocean cell that can't be replenished, and animals can't be
    placed in or move to. """

    def __init__(self):
        super().__init__()


class Mountain(LandscapeCell):
    """Create an mountain cell that can't be replenished, and animals can't be
        placed in or move to. """

    def __init__(self):
        super().__init__()
