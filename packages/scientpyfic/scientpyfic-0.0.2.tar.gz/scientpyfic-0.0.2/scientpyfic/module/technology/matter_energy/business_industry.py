from scientpyfic.API import API


class BusinessIndustry:

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

  def textiles_and_clothing(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about textiles and clothing.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/textiles_and_clothing.xml".format(self._url)
    result = API.get(url, name='TextilesAndClothing', **options, **kwargs)

    return result


  def engineering_and_construction(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about engineering and construction.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/engineering_and_construction.xml".format(self._url)
    result = API.get(url, name='EngineeringAndConstruction', **options, **kwargs)

    return result

  def energy_and_resources(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about energy and resources.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/energy_and_resources.xml".format(self._url)
    result = API.get(url, name='EnergyAndResources', **options, **kwargs)

    return result


  def telecommunications(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about telecommunications.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/telecommunications.xml".format(self._url)
    result = API.get(url, name='Telecommunications', **options, **kwargs)

    return result


  def automotive_and_transportation(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about automotive and transportation.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/automotive_and_transportation.xml".format(self._url)
    result = API.get(url, name='AutomotiveAndTransportation', **options, **kwargs)

    return result


  def aerospace(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about aerospace.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/aerospace.xml".format(self._url)
    result = API.get(url, name='Aerospace', **options, **kwargs)

    return result


  def consumer_electronics(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news from ScienceDaily about consumer electronics.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/consumer_electronics.xml".format(self._url)
    result = API.get(url, name='ConsumerElectronics', **options, **kwargs)

    return result
