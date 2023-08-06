from scientpyfic.API import API


class Health:

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

  def workplace_health(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news from ScienceDaily about workplace health.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/health_medicine/workplace_health.xml".format(self._url)
    result = API.get(url, name='WorkplaceHealth', **options, **kwargs)

    return result


  def pharmaceuticals(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news from ScienceDaily about pharmaceuticals.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/health_medicine/pharmaceuticals.xml".format(self._url)
    result = API.get(url, name='Pharmaceuticals', **options, **kwargs)

    return result


  def cosmetics(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news from ScienceDaily about cosmetics.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/health_medicine/cosmetics.xml".format(self._url)
    result = API.get(url, name='Cosmetics', **options, **kwargs)

    return result


  def medical_devices(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news from ScienceDaily about medical devices.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/health_medicine/medical_devices.xml".format(self._url)
    result = API.get(url, name='MedicalDevices', **options, **kwargs)

    return result
