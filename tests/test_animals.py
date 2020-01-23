# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import pytest
import random
import src.biosim.animals as ani
import src.biosim.landscapes as land
import src.biosim.simulation as sim


class BaseTestAnimal:
    AnimalType = ani.Animal

    @pytest.fixture
    def ex_ani(self):
        yield self.AnimalType()

    @pytest.fixture
    def ex_fit_ani(self):
        ani = self.AnimalType()
        ani.weight = 90
        yield ani

    @pytest.fixture
    def ex_unfit_ani(self):
        ani = self.AnimalType()
        ani.weight = 0
        yield ani

    @pytest.fixture
    def ex_jungle(self):
        yield land.Jungle()


    def test_isinstance(self, ex_ani):
        assert isinstance(ex_ani, ani.Animal)

    def test_set_params(self, ex_ani):
        different_params = {'a_half': 123, 'gamma': 456 }
        ex_ani.set_params(different_params)
        assert ex_ani.a_half == 123
        assert ex_ani.gamma == 456

    def test_initial_age(self, ex_ani):
        assert ex_ani.age == 0

    def test_aging(self, ex_ani):
        ex_ani.aging()
        ex_ani.aging()
        assert ex_ani.age == 2

    def test_phi(self, ex_ani):
        assert 0 < ex_ani.phi < 1

    def test_weightloss(self, ex_ani):
        remembered_w = ex_ani.weight
        ex_ani.weightloss()
        assert 0 <= ex_ani.weight < remembered_w

    def test_dying(self, mocker, ex_fit_ani, ex_unfit_ani):
        mocker.patch('numpy.random.random', return_value=1)
        survivor = ex_fit_ani
        assert survivor.dies() is False
        mocker.patch('numpy.random.random', return_value=0)
        dying_ani = ex_unfit_ani
        assert dying_ani.dies()

    def test_movable(self, mocker, ex_fit_ani, ex_unfit_ani):
        mocker.patch('numpy.random.random', return_value=0)
        fit_ani = ex_fit_ani
        assert fit_ani.movable()
        mocker.patch('numpy.random.random', return_value=1)
        unfit_ani = ex_fit_ani
        assert unfit_ani.movable() is False


class TestHerbivore(BaseTestAnimal):
    AnimalType = ani.Herbivore

    @pytest.fixture
    def ex_herbivore(self):
        yield ani.Herbivore()

    def test_get_rel_abundance(self, ex_herbivore, ex_jungle):
        assert type(ex_herbivore.get_rel_abundance(ex_jungle)) == float
        assert 0 < ex_herbivore.get_rel_abundance(ex_jungle)

class TestCarnivore(BaseTestAnimal):
    AnimalType = ani.Carnivore

    @pytest.fixture
    def ex_carnivore(self):
        yield ani.Carnivore()

    def test_get_rel_abundance(self, ex_ani, ex_carnivore,
                               ex_jungle):
        ex_jungle.population['Herbivore'].append(ani.Herbivore())
        assert type(ex_carnivore.get_rel_abundance(ex_jungle)) == float
        assert 0 < ex_carnivore.get_rel_abundance(ex_jungle)






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
def example_herbivore():
    default_params = ani.Herbivore.params.copy()
    yield ani.Herbivore()
    ani.Herbivore.params = default_params


@pytest.fixture
def example_carnivore():
    default_params = ani.Carnivore.params.copy()
    yield ani.Carnivore()
    ani.Herbivore.params = default_params


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
def example_map():
    return """OOOO\nOJJO\nOOOO"""

class TestAnimal:

    def test_herbivore(self, example_herbivore):
        """
        Checks if instance of herbivore can be created and is instance of
        the animal class
        """
        assert isinstance(example_herbivore, ani.Animal)

    def test_carnivore(self, example_carnivore):
        """
        Checks if instance of carnivore can be created and is instance
        of the animal class
        """
        assert isinstance(example_carnivore, ani.Animal)

    def test_aging(self, example_herbivore):
        """
        Checks if age of a given instance increases by call of instance.aging
        """
        old_age = example_herbivore.age
        example_herbivore.aging()
        assert example_herbivore.age > old_age

    def test_weightloss(self, example_herbivore):
        """
        Checks if weight of an instance decreases by call of
        instance.weightloss()
        """
        old_weight = example_herbivore.weight
        example_herbivore.weightloss()
        assert example_herbivore.weight < old_weight

    def test_herbivore_feeding(self, example_herbivore, example_savannah):
        """
        Checks if weight of an instance increases by call of
        instance.feeding(F)
        given initial parameter value F specific for that instance.
        """
        previous_weight = example_herbivore.weight
        example_herbivore.feeding(example_savannah)
        assert previous_weight < example_herbivore.weight

    def test_place_animal(self, input_list, example_map):
        i = sim.BioSim(example_map, input_list, None)
        herbivore_list = i.map[(1, 1)]
        assert len(herbivore_list.population['Herbivore']) == 2

    def test_tot_w_herbivores(self, input_list, example_map):
        i = sim.BioSim(example_map, input_list, None)
        c = i.map[(1, 1)]
        assert c.tot_w_herbivores == 22.8

    def test_migration(self, example_carnivore):
        cell1, cell2 = land.Savannah(), land.Savannah()
        cell1.population["Carnivore"].append(example_carnivore)
        example_carnivore.move(cell1, cell2)
        assert len(cell2.population["Carnivore"]) == 1

    def test_little_fodder(self, example_herbivore):
        herbivore = example_herbivore
        herbivore_weight_if_not_limited = (herbivore.weight + herbivore.beta *
                                           herbivore.F)
        savannah = land.Savannah()
        savannah.f = random.randint(0, (herbivore.F - 1))
        savannah.feeding()
        assert herbivore.weight < herbivore_weight_if_not_limited

    def test_check_procreation(self, example_carnivore):
        random.seed(999)
        example_carnivore.weight = 45
        assert example_carnivore.fertile(90)

    def test_parameter_change(self, example_carnivore):
        old_parameter = example_carnivore.params["w_birth"]
        example_carnivore.params["w_birth"] = 10
        assert example_carnivore.params["w_birth"] is not old_parameter

    def test_value_error_raised_placement_mountain_ocean(self):
        test_map = 'OOOO\nOMDO\nOOO'
        input = [{'loc': (1, 1), 'pop': [{'species': 'Herbivore', 'age': 10,
                                          'weight': 12.5}]}]
        with pytest.raises(ValueError):
            sim.BioSim(test_map, input, None)
