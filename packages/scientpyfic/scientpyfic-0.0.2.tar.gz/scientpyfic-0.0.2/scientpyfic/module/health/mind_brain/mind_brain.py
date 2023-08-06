from .disorder_and_syndrome import DisorderAndSyndrome
from .education_and_learning import EducationAndLearning
from .illegal_drug import IllegalDrug
from .living_well import LivingWell
from .mental_health import MentalHealth
from .neuroscience import Neuroscience
from .psychiatry import Psychiatry
from .psychology import Psychology


class MindBrain:

  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = "{}/mind_brain".format(url)
    self.disorders_syndromes = DisorderAndSyndrome(self._url, title, description, pub_date, body, journals)
    self.education_learning = EducationAndLearning(self._url, title, description, pub_date, body, journals )
    self.illegal_drugs = IllegalDrug(self._url, title, description, pub_date, body, journals)
    self.living_well = LivingWell(self._url, title, description, pub_date, body, journals)
    self.mental_health = MentalHealth(self._url, title, description, pub_date, body, journals)
    self.neuroscience = Neuroscience(self._url, title, description, pub_date, body, journals)
    self.psychiatry = Psychiatry(self._url, title, description, pub_date, body, journals)
    self.psychology = Psychology(self._url, title, description, pub_date, body, journals)

  def mind_brain(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about mind brain from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}.xml".format(self._url)
    result = API.get(url, name='MindBrain', **options)

    return result