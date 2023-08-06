from .business_industry.business_industry import BusinessIndustry
from .education_learning.education_learning import EducationLearning
from .science_society.science_society import ScienceSociety

class Society:

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Society.md
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self.business_industry = BusinessIndustry(url, title, description, pub_date, body, journals)
    self.education_learning = EducationLearning(url, title, description, pub_date, body, journals)
    self.science_society = ScienceSociety(url, title, description, pub_date, body, journals)