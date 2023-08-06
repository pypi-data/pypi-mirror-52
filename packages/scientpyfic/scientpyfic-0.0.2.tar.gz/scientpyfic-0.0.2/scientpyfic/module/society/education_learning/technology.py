from scientpyfic.API import API


class Technology:

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

  def neural_interfaces(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about weird world.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/computers_math/neural_interfaces.xml".format(self._url)
    result = API.get(url, name='NeuralInterfaces', **options, **kwargs)

    return result


  def educational_technology(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about educational technology.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/computers_math/educational_technology.xml".format(self._url)
    result = API.get(url, name='EducationalTechnology', **options, **kwargs)

    return result

