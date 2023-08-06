from scientpyfic.API import API

class Vitamin:

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

  def vitamin(self, title=None, description=None, pub_date=None, body=None, journals=None):
    """
    Returns a list with latest news from ScienceDaily about vitamins.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }
    url = "{}/vitamins.xml".format(self._url)
    result = API.get(url, name='Vitamin', **options, **kwargs)
    return result

  def vitamin_a(self, title=None, description=None, pub_date=None, body=None, journals=None):
    """
    Returns a list with latest news from ScienceDaily about vitamin a.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }
    url = "{}/vitamin_a.xml".format(self._url)
    result = API.get(url, name='VitaminA', **options, **kwargs)
    return result

  def vitamin_e(self, title=None, description=None, pub_date=None, body=None, journals=None):
    """
    Returns a list with latest news from ScienceDaily about  vitamin e.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/vitamin_e.xml".format(self._url)
    result = API.get(url, name='VitaminE', **options, **kwargs)
    return result

  def vitamin_c(self, title=None, description=None, pub_date=None, body=None, journals=None):
    """
    Returns a list with latest news from ScienceDaily about vitamin c.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/vitamin_c.xml".format(self._url)
    result = API.get(url, name='VitaminC', **options, **kwargs)
    return result

  def vitamin_d(self, title=None, description=None, pub_date=None, body=None, journals=None):
    """
    Returns a list with latest news from ScienceDaily about vitamin d.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/vitamin_d.xml".format(self._url)
    result = API.get(url, name='VitaminD', **options, **kwargs)
    return result

  def vitamin_b(self, title=None, description=None, pub_date=None, body=None, journals=None):
    """
    Returns a list with latest news from ScienceDaily about vitamin b.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/vitamin_b.xml".format(self._url)
    result = API.get(url, name='VitaminB', **options, **kwargs)
    return result