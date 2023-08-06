from scientpyfic.API import API

class HeartHealth:

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Health.py
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = url
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

  def vioxx(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):    
    """
    Latest news about vioxx in ScienceDaily.

    :return: a list with news about vioxx
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/vioxx.xml".format(self._url)
    result = API.get(url, name='Vioxx', **options, **kwargs)
    return result

  def cholesterol(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about cholesterol in ScienceDaily.

    :return: a list with news about cholesterol
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/cholesterol.xml".format(self._url)
    result = API.get(url, name='Cholesterol', **options, **kwargs)
    return result

  def stroke_prevention(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about stroke prevention in ScienceDaily.

    :return: a list with news about stroke prevention
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/stroke.xml".format(self._url)
    result = API.get(url, name='StrokePrevention', **options, **kwargs)
    return result