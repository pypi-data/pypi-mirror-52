from .computers_math.computers_math import ComputersMath
from .matter_energy.matter_energy import MatterEnergy
from .space_time.space_time import SpaceTime

class Technology:
  
  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Technology.md
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self.computers_math = ComputersMath(url, title, description, pub_date, body, journals)
    self.matter_energy = MatterEnergy(url, title, description, pub_date, body, journals)
    self.space_time = SpaceTime(url, title, description, pub_date, body, journals)