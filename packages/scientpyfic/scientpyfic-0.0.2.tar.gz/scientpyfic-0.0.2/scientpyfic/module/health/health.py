from .health_medicine.health_medicine import HealthMedicine
from .living_well.living_well import LivingWell
from .mind_brain.mind_brain import MindBrain

class Health:

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Health.py
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self.health_medicine = HealthMedicine(url, title, description, pub_date, body, journals)
    self.living_well = LivingWell(url, title, description, pub_date, body, journals)
    self.mind_brain = MindBrain(url, title, description, pub_date, body, journals)