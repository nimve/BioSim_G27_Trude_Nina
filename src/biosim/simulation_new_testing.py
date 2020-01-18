# -*- coding: utf-8 -*-

"""
"""
import pandas as pd
from src.biosim.island import Island as isl
from src.biosim.animals import Animal, Herbivore, Carnivore
from src.biosim.run import Run
from src.biosim.landscapes import Savannah, Jungle, Mountain, Desert, Ocean
__author__ = ""
__email__ = ""


class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'
        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}
        If img_base is None, no figures are written to file.
        Filenames are formed as
            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        pass

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.
        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        pass

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
        (default: vis_years)
        Image files will be numbered consecutively.
        """
        pass

    def add_population(self, population):
        """
        Add a population to the island
        :param population: List of dictionaries specifying population
        """
        self.Island().place_animals(population)
        pass

    @property
    def year(self):
        """Last year simulated."""
        return self.year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self.num_animals_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count
        per species for each cell on island."""
        data = {'Population': self.num_animals, 'Herbivores':
                self.num_animals_per_species['Herbivore'], 'Carnivores':
                self.num_animals_per_species['Carnivore']}
        return pd.DataFrame(data)

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass

if __name__ == '__main__':
