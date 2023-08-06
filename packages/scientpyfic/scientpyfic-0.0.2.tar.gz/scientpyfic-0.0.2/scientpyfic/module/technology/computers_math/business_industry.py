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

  def markets_and_finance(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about markets and finance.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/computers_math/markets_and_finance.xml".format(self._url)
    result = API.get(url, name='MarketsAndFinance', **options, **kwargs)

    return result


  def computers_and_internet(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list with latest news from ScienceDaily about computers and internet.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/computers_math/computers_and_internet.xml".format(self._url)
    result = API.get(url, name='ComputersAndInternet', **options, **kwargs)

    return result

