from scientpyfic.API import API


class Chemistry:

  """
  For more information check the official documentation:
    https://github.com/monzita/scientpyfic/wiki/Technology.md
  """
  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = url
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals


  def biochemistry(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about biochemistry.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/biochemistry.xml".format(self._url)
    result = API.get(url, name='Biochemistry', **options, **kwargs)

    return result


  def inorganic_chemistry(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about inforganic chemistry.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/inorganic_chemistry.xml".format(self._url)
    result = API.get(url, name='InforganicChemistry', **options, **kwargs)

    return result


  def organic_chemistry(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about organic chemistry.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/organic_chemistry.xml".format(self._url)
    result = API.get(url, name='OrganicChemistry', **options, **kwargs)

    return result


  def chemistry(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about chemistry.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/chemistry.xml".format(self._url)
    result = API.get(url, name='Chemistry', **options, **kwargs)

    return result


  def thermodynamics(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about thermodynamics.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/thermodynamics.xml".format(self._url)
    result = API.get(url, name='Thermodynamics', **options, **kwargs)

    return result
