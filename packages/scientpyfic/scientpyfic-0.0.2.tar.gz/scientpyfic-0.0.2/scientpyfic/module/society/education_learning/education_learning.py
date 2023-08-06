from .environment import Environment
from .health import Health
from .society import Society
from .technology import Technology

from scientpyfic.API import API


class EducationLearning:

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Society.md
  """
  def __init__(self, url, title, description, pub_date, body, journals):

    self._url = url
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

    self.environment = Environment(url, title, description, pub_date, body, journals)
    self.health = Health(url, title, description, pub_date, body, journals)
    self.society = Society(url, title, description, pub_date, body, journals)
    self.technology = Technology(url, title, description, pub_date, body, journals)

  def education_and_learning(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news from ScienceDaily about Education & Learning
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/education_learning.xml".format(self._url)
    result = API.get(url, name='EducationAndLearning', **options, **kwargs)

    return result
