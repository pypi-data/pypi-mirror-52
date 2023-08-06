from .business_industry import BusinessIndustry
from .chemistry import Chemistry
from .electricity import Electricity
from .energy_technology import EnergyTechnology
from .engineering import Engineering
from .physics import Physics

from scientpyfic.API import API


class MatterEnergy:

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Technology.md
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = "{}/matter_energy".format(url)
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

    self.business_industry = BusinessIndustry(self._url, title, description, pub_date, body, journals)
    self.chemistry = Chemistry(self._url,  title, description, pub_date, body, journals)
    self.electricity = Electricity(self._url,  title, description, pub_date, body, journals)
    self.energy_technology = EnergyTechnology(self._url,  title, description, pub_date, body, journals)
    self.engineering = Engineering(self._url,  title, description, pub_date, body, journals)
    self.physics = Physics(self._url, title, description, pub_date, body, journals)


  def matter_energy(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news from ScienceDaily about matter energy.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}.xml".format(self._url)
    result = API.get(url, name='MatterEnergy', **options, **kwargs)

    return result
