from scientpyfic.API import API


class Society:

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

  def education_and_employment(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about education and employment.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/science_society/education_and_employment.xml".format(self._url)
    result = API.get(url, name='EducationAndEmployment', **options, **kwargs)

    return result


  def stem_education(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about stem education.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/science_society/stem_education.xml".format(self._url)
    result = API.get(url, name='StemEducation', **options, **kwargs)

    return result

  def poverty_and_learning(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily aboutpoverty and learning.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/science_society/poverty_and_learning.xml".format(self._url)
    result = API.get(url, name='PovertyLearning', **options, **kwargs)

    return result


  def educational_policy(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about educational policy.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/science_society/educational_policy.xml".format(self._url)
    result = API.get(url, name='EducationalPolicy', **options, **kwargs)

    return result
