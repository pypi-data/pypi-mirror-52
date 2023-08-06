from scientpyfic.API import API


class BusinessIndustry:

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

  def media_and_entertainment(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about media and entertainment.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/science_society/media_and_entertainment.xml".format(self._url)
    result = API.get(url, name='MediaAndEntertainment', **options, **kwargs)

    return result


  def retail_and_services(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about retail and services.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/science_society/retail_and_services.xml".format(self._url)
    result = API.get(url, name='WeirdWorld', **options, **kwargs)

    return result


  def industrial_relations(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about industrial relations.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/science_society/industrial_relations.xml".format(self._url)
    result = API.get(url, name='IndustrialRelation', **options, **kwargs)

    return result


  def security_and_defense(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about security and defense.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/science_society/security_and_defense.xml".format(self._url)
    result = API.get(url, name='SecurityAndDefense', **options, **kwargs)

    return result


  def travel_and_recreation(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about travel and recreation.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/science_society/travel_and_recreation.xml".format(self._url)
    result = API.get(url, name='TravelAndRecreation', **options, **kwargs)

    return result