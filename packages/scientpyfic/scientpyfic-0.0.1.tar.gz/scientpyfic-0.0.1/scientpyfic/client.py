from .module.environment.environment import Environment
from .module.health.health import Health
from .module.main.all import All
from .module.main.top import Top
from .module.quirky.quirky import Quirky
from .module.society.society import Society
from .module.technology.technology import Technology
from .module.main.most_popular import MostPopular
from .module.main.strange_offbeat import StrangeOffbeat

class ScientPyClient:

  URL = 'https://www.sciencedaily.com/rss'

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki
  """
  def __init__(self, title=True, description=True, pub_date=True, body=False, journals=False):
    self.all = All(self.URL, title, description, pub_date, body, journals)
    self.top = Top(self.URL, title, description, pub_date, body, journals)
    self.most_popular = MostPopular(self.URL, title, description, pub_date, body, journals)
    self.strange_offbeat = StrangeOffbeat(self.URL, title, description, pub_date, body, journals)
    self.health = Health(self.URL, title, description, pub_date, body, journals)
    self.environment = Environment(self.URL, title, description, pub_date, body, journals)
    self.quirky = Quirky(self.URL, title, description, pub_date, body, journals)
    self.society = Society(self.URL, title, description, pub_date, body, journals)
    self.technology = Technology(self.URL, title, description, pub_date, body, journals)