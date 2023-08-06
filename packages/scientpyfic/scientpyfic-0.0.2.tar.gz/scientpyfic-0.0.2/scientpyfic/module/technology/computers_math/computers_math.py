from scientpyfic.API import API

from .business_industry import BusinessIndustry
from .computer_science import ComputerScience
from .education_learning import EducationLearning
from .mathematics import Mathematics

class ComputersMath:

  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = url
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

    self.business_industry = BusinessIndustry(url, title, description, pub_date, body, journals)
    self.computer_science = ComputerScience(url, title, description, pub_date, body, journals)
    self.education_learning = EducationLearning(url, title, description, pub_date, body, journals)
    self.mathematics = Mathematics(url, title, description, pub_date, body, journals)

  def computers_and_math(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news from ScienceDaily about computers & math.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/computers_math.xml".format(self._url)
    result = API.get(url, name='ComputersMath', **options, **kwargs)

    return result
