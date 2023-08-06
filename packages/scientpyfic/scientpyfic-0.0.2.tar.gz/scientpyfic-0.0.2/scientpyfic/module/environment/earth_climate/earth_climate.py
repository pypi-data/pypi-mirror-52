from .business_industry import BusinessIndustry
from .earth_science import EarthScience
from .education_learning import EducationLearning
from .environmental_issues import EnvironmentalIssue
from .environmental_science import EnvironmentalScience
from .natural_disaster import NaturalDisaster

from scientpyfic.API import API

class EarthClimate:
  
  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Environment.py
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = "{}/earth_climate".format(url)
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

    self.business_industry = BusinessIndustry(self._url, title, description, pub_date, body, journals)
    self.earth_science = EarthScience(self._url, title, description, pub_date, body, journals)
    self.education_learning = EducationLearning(self._url, title, description, pub_date, body, journals)
    self.environmental_issues = EnvironmentalIssue(self._url, title, description, pub_date, body, journals)
    self.environmental_science = EnvironmentalScience(self._url, title, description, pub_date, body, journals)
    self.natural_disasters = NaturalDisaster(self._url, title, description, pub_date, body, journals)


  def earth_climate(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about earth climate.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}.xml".format(self._url)
    result = API.get(url, name='EarthClimate', **options, **kwargs)

    return result
