from scientpyfic.API import API

class ColdAndFlu:

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

  def influenza(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about influenza in ScienceDaily.

    :return: a list with news about influenza
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/influenza.xml".format(self._url)
    result = API.get(url, name='Influenza', **options, **kwargs)

    return result

  def swine_flu(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about sline flu in ScienceDaily.

    :return: a list with news about swine flu
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/swine_flu.xml".format(self._url)
    result = API.get(url, name='SwineFlu', **options, **kwargs)

    return result

  def cold_and_flu(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about cold and flu in ScienceDaily.

    :return: a list with news about cold and flu
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/cold_and_flu.xml".format(self._url)
    result = API.get(url, name='ColdAndFlu', **options, **kwargs)

    return result

  def bird_flu(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about bird flu in ScienceDaily.

    :return: a list with news about bird flu
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/bird_flu.xml".format(self._url)
    result = API.get(url, name='BirdFlu', **options, **kwargs)

    return result