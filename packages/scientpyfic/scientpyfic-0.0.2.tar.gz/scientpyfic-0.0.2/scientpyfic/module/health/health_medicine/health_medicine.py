from .business_industry import BusinessIndustry
from .diseases_conditionals.diseases_conditionals import DiseaseConditional
from .living_well import LivingWell
from .medical_topic import MedicalTopic
from .education_learning import EducationLearning

from scientpyfic.API import API

class HealthMedicine:

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Health.py
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

    self._url = "{}/health_medicine".format(url)
    self.business_industry = BusinessIndustry(self._url, title, description, pub_date, body, journals)
    self.diseases_conditionals = DiseaseConditional(self._url, title, description, pub_date, body, journals)
    self.living_well = LivingWell(self._url, title, description, pub_date, body, journals)
    self.medical_topics = MedicalTopic(self._url, title, description, pub_date, body, journals)
    self.education_learning = EducationLearning(self._url, title, description, pub_date, body, journals)

  def health_and_medicine(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest health and medicine news from ScienceDaily.

    :return: a list with health and medicine news.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}.xml".format(self._url)
    result = API.get(url, name='HealthMedicine', **options, **kwargs)
    return result