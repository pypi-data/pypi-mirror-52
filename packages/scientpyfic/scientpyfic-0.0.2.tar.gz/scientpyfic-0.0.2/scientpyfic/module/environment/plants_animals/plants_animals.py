from .agriculture_food import AgricultureFood
from .animal import Animal
from .business_industry import BusinessIndustry
from .ecology import Ecology
from .education_learning import EducationLearning
from .life_science import LifeScience
from .microbes_more import MicrobesMore

from scientpyfic.API import API


class PlantsAnimals:

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Environment.py
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = "{}/plants_animals".format(url)
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

    self.agriculture_food = AgricultureFood(self._url, title, description, pub_date, body, journals)
    self.animals = Animal(self._url, title, description, pub_date, body, journals)
    self.business_industry = BusinessIndustry(self._url, title, description, pub_date, body, journals)
    self.ecology = Ecology(self._url, title, description, pub_date, body, journals)
    self.education_learning = EducationLearning(self._url, title, description, pub_date, body, journals)
    self.life_science = LifeScience(self._url, title, description, pub_date, body, journals)
    self.microbes_more = MicrobesMore(self._url, title, description, pub_date, body, journals)

  def plants_and_animals(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about plants and animals.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}.xml".format(self._url)
    result = API.get(url, name='PlantsAndAnimals', **options, **kwargs)

    return result
