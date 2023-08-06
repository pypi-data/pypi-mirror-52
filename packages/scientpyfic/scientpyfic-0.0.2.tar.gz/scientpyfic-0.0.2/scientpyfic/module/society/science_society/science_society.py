from .business_industry import BusinessIndustry
from .culture import Culture
from .education_learning import EducationLearning
from .science_policy import SciencePolicy
from .social_issues import SocialIssues

class ScienceSociety:

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

    self.business_industry = BusinessIndustry(url, title, description, pub_date, body, journals)
    self.culture = Culture(url, title, description, pub_date, body, journals)
    self.education_learning = EducationLearning(url, title, description, pub_date, body, journals)
    self.science_policy = SciencePolicy(url, title, description, pub_date, body, journals)
    self.social_issues = SocialIssues(url, title, description, pub_date, body, journals)

  def science_society(self,title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news from ScienceDaily about science society.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/science_society.xml".format(self._url)
    result = API.get(url, name='ScienceSociety', **options, **kwargs)

    return result
