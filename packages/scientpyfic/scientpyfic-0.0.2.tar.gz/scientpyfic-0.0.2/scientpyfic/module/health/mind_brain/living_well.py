from scientpyfic.API import API

class LivingWell:

  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = url
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

  def child_development(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about child development from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/child_development.xml".format(self._url)
    result = API.get(url, name='ChildDevelopment', **options)

    return result

  def stress(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about stress from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/stress.xml".format(self._url)
    result = API.get(url, name='Stress', **options)

    return result

  def consumer_behavior(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about consumer behavior from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/consumer_behavior.xml".format(self._url)
    result = API.get(url, name='ConsumerBehavior', **options)

    return result

  def spirituality(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about spirituality from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/spirituality.xml".format(self._url)
    result = API.get(url, name='Spirituality', **options)

    return result

  def dieting_and_weight_control(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about dieting and weight control from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/diet_and_weight_loss.xml".format(self._url)
    result = API.get(url, name='DietingAndWeightControl', **options)

    return result

  def nutrition_research(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about nutrition research from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/nutrition.xml".format(self._url)
    result = API.get(url, name='NutritionResearch', **options)

    return result

  def behavior(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about behavior from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/behavior.xml".format(self._url)
    result = API.get(url, name='Behavior', **options)

    return result

  def caregiving(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about caregiving from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/caregiving.xml".format(self._url)
    result = API.get(url, name='Caregiving', **options)

    return result

  def parenting(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about parenting from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/parenting.xml".format(self._url)
    result = API.get(url, name='Parenting', **options)

    return result

  def anger_management(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about anger management from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/anger_management.xml".format(self._url)
    result = API.get(url, name='AngerManagement', **options)

    return result

  def gender_difference(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about gender difference from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/gender_difference.xml".format(self._url)
    result = API.get(url, name='GenderDifference', **options)

    return result

  def racial_issues(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about racial issues from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/racial_issues.xml".format(self._url)
    result = API.get(url, name='RacialIssue', **options)

    return result

  def relationships(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about relationships from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/relationships.xml".format(self._url)
    result = API.get(url, name='Relationship', **options)

    return result