from .anthropology import Anthropology
from .archaeology import Archaeology
from .evolution import Evolution
from .paleontology import Paleontology

from scientpyfic.API import API


class FossilsRuins:

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Environment.py
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = "{}/fossils_ruins".format(url)
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

    self.anthropology = Anthropology(self._url, title, description, pub_date, body, journals)
    self.archaeology = Archaeology(self._url, title, description, pub_date, body, journals)
    self.evolution = Evolution(self._url, title, description, pub_date, body, journals)
    self.paleontology = Paleontology(self._url, title, description, pub_date, body, journals)

  def fossils_and_ruins(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about fossils and ruins.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}.xml".format(self._url)
    result = API.get(url, name='FossilsAndRuins', **options, **kwargs)

    return result