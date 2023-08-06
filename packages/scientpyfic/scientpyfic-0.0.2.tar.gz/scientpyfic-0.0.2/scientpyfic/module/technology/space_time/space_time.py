from .astronomy import Astronomy
from .cosmology import Cosmology
from .solar_system import SolarSystem
from .space_exploration import SpaceExploration

from scientpyfic.API import API

class SpaceTime:


  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Technology.md
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = "{}/space_time".format(url)

    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

    self.astronomy = Astronomy(self._url, title, description, pub_date, body, journals)
    self.cosmology = Cosmology(self._url, title, description, pub_date, body, journals)
    self.solar_system = SolarSystem(self._url, title, description, pub_date, body, journals)
    self.space_exploration = SpaceExploration(self._url, title, description, pub_date, body, journals)


  def space_time(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about space & time.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}.xml".format(self._url)
    result = API.get(url, name='SpaceTime', **options, **kwargs)

    return result
