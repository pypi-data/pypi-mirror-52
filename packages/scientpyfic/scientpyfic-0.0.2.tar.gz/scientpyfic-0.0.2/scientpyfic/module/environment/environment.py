from .earth_climate.earth_climate import EarthClimate
from .fossils_ruins.fossils_ruins import FossilsRuins
from .plants_animals.plants_animals import PlantsAnimals

class Environment:


  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Environment.py
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self.earth_climate = EarthClimate(url, title, description, pub_date, body, journals)
    self.plants_animals = PlantsAnimals(url, title, description, pub_date, body, journals)
    self.fossils_ruins = FossilsRuins(url, title, description, pub_date, body, journals)
