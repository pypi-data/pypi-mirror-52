from scientpyfic.API import API


class Physics:

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

  def albert_einstein(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about Albert Einstein.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/albert_einstein.xml".format(self._url)
    result = API.get(url, name='AlbertEinsteing', **options, **kwargs)

    return result


  def quantum_physics(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about quantum physics.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/quantum_physics.xml".format(self._url)
    result = API.get(url, name='QuantumPhysics', **options, **kwargs)

    return result


  def nature_of_water(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about nature of water.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/nature_of_water.xml".format(self._url)
    result = API.get(url, name='NatureOfWater', **options, **kwargs)

    return result


  def quantum_computing(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about quantum computing.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/quantum_computing.xml".format(self._url)
    result = API.get(url, name='QuantumComputing', **options, **kwargs)

    return result


  def ultrasound(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about ultrasound.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/ultrasound.xml".format(self._url)
    result = API.get(url, name='Ultrasound', **options, **kwargs)

    return result


  def acoustics(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about acoustics.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/acoustics.xml".format(self._url)
    result = API.get(url, name='Acoustics', **options, **kwargs)

    return result


  def optics(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about optics.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/nature_of_light.xml".format(self._url)
    result = API.get(url, name='Optics', **options, **kwargs)

    return result


  def physics(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about physics.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/physics.xml".format(self._url)
    result = API.get(url, name='Physics', **options, **kwargs)

    return result
