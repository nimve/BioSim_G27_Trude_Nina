# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"
import src.biosim.animals as ani
import src.biosim.landscapes as land
import src.biosim.simulation as sim
import pytest
import random

@pytest.fixture
def input_list():
    return [
        {'loc': (1, 1),
         'pop': [
         {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
         {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
         {'species': 'Carnivore', 'age': 14, 'weight': 10.3},
         {'species': 'Carnivore', 'age': 5, 'weight': 10.1}]},
        {'loc': (1, 2),
         'pop': [
          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
          {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
          {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]},
        {'loc': (1, 2),
         'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.6}]}]


@pytest.fixture
def example_savannah():
    params = land.Savannah.params.copy()
    yield land.Savannah()
    land.Savannah.params = params


@pytest.fixture
def example_jungle():
    params = land.Jungle.params.copy()
    yield land.Jungle()
    land.Jungle.params = params

@pytest.fixture
def example_herbivore():
    yield ani.Herbivore

@pytest.fixture
def example_map():
    return """OOOO\nOJJO\nOOOO"""


class BaseTestLandscapes:
    LandscapeType = land.LandscapeCell

    @pytest.fixture
    def ex_land(self):
        yield self.LandscapeType

    def test_instance(self, ex_land):
        assert isinstance(ex_land, land.LandscapeCell)

    def test_change_param_dict(self, ex_land):
        """
        Checks if a change of parameters actually applies to class instance
        and replaces standard values
        """
        original_dict = ex_land.f_max
        ex_land.set_params({'f_max': 900})
        assert ex_land.f_max is not original_dict

    def test_fodder(self, ex_land):
        """
        A test that tests if an instance of the landscape class, given a
        value under f_max replenishes itself if possible (increases the f
        value)
        """
        ex_land.f = 200.0
        ex_land.replenish()
        assert ex_land.f > 200.0


class TestSavannah(BaseTestLandscapes):
    LandscapeType = land.Savannah()


class TestJungle(BaseTestLandscapes):
    LandscapeType = land.Jungle()


class TestDesert(BaseTestLandscapes):
    LandscapeType = land.Desert()

class TestMountain():
    pass


