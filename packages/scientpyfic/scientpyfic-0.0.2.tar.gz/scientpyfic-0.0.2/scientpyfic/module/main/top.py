from scientpyfic.API import API

class Top:

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Top.py
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = url
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

  def top(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest top news from ScienceDaily.

    :return: list with latest news, where each object has fields title, description and pub_date.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/top.xml".format(self._url)
    result = API.get(url, name='TopNews', **options, **kwargs)
    return result

  def science(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest top science news from ScienceDaily.

    :return: list with latest news, where each object has fields title, description and pub_date.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/top/science.xml".format(self._url)
    result = API.get(url, name='TopScienceNews', **options, **kwargs)
    return result

  def health(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest top health from ScienceDaily.

    :return: list with latest news, where each object has fields title, description and pub_date.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/top/health.xml".format(self._url)
    result = API.get(url, name='TopHealthNews', **options, **kwargs)
    return result

  def technology(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest top technology from ScienceDaily.
    :return: list with latest news, where each object has fields title, description and pub_date.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/top/technology.xml".format(self._url)
    result = API.get(url, name='TopTechnologyNews', **options, **kwargs)
    return result

  def environment(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest top environment news from ScienceDaily.

    :return: list with latest news, where each object has fields title, description and pub_date.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/top/environment.xml".format(self._url)
    result = API.get(url, name='TopEnvironmentNews', **options, **kwargs)
    return result

  def society(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest top society news from ScienceDaily.

    :return: list with latest news, where each object has fields title, description and pub_date.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/top/society.xml".format(self._url)
    result = API.get(url, name='TopSocietyNews', **options, **kwargs)
    return result