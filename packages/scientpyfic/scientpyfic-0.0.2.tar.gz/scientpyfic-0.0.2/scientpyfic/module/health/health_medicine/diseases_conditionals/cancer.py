from scientpyfic.API import API

class Cancer:

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

  def cervical_cancer(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about cervical cancer from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/cervical_cancer.xml".format(self._url)
    result = API.get(url, name='CervicalCancer', **options, **kwargs)
    return result

  def bladder_cancer(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about bladder cancer in ScienceDaily.

    :return: a list with news about bladder cancer
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }
    url = "{}/bladder_cancer.xml".format(self._url)
    result = API.get(url, name='BladderCancer', **options, **kwargs)
    return result

  def multiple_myeloma(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about multiple myeloma in ScienceDaily.

    :return: a list with news about myeloma cancer
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }
    url = "{}/multiple_myeloma.xml".format(self._url)
    result = API.get(url, name='MultipleMyeloma', **options, **kwargs)
    return result

  def brain_tumor(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about brain tumor in ScienceDaily.

    :return: a list with news about brain tumor
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }
    url = "{}/brain_tumor.xml".format(self._url)
    result = API.get(url, name='BrainTumor', **options, **kwargs)
    return result

  def colon_cancer(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about colon cancer in ScienceDaily.

    :return: a list with news about colon cancer
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/colon_cancer.xml".format(self._url)
    result = API.get(url, name='ColonCancer', **options, **kwargs)
    return result

  def breast_cancer(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about breast cancer in ScienceDaily.

    :return: a list with news about breast cancer
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/breast_cancer.xml".format(self._url)
    result = API.get(url, name='BreastCancer', **options, **kwargs)
    return result

  def ovarian_cancer(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about ovarian cancer in ScienceDaily.

    :return: a list with news about ovarian cancer
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }
    url = "{}/ovarian_cancer.xml".format(self._url)
    result = API.get(url, name='OvarianCancer', **options, **kwargs)
    return result

  def lung_cancer(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about lung cancer in ScienceDaily.

    :return: a list with news about lung cancer
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/lung_cancer.xml".format(self._url)
    result = API.get(url, name='LungCancer', **options, **kwargs)
    return result