from scientpyfic.API import API

class EducationAndLearning:

  def __init__(self, url, title, description, pub_date, body, journals):
    self._url = url
    self._title = title
    self._description = description
    self._pub_date = pub_date
    self._body = body
    self._journals = journals

  def dyslexia(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about dyslexia from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/dyslexia.xml".format(self._url)
    result = API.get(url, name='Dyslexia', **options)

    return result

  def educational_psychology(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about educational psychology from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/educational_psychology.xml".format(self._url)
    result = API.get(url, name='EducationalPsychology', **options)

    return result

  def k_12_education(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about k-12 education from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/k-12_education.xml".format(self._url)
    result = API.get(url, name='k12Education', **options)

    return result

  def numeracy(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about numeracy from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/numeracy.xml".format(self._url)
    result = API.get(url, name='Numeracy', **options)

    return result

  def brain_computer_interfaces(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about brain computer interfaces from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/brain-computer_interfaces.xml".format(self._url)
    result = API.get(url, name='BrainComputerInterfaces', **options)

    return result

  def learning_disorders(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about learning disorders from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/learning_disorders.xml".format(self._url)
    result = API.get(url, name='LearningDisorders', **options)

    return result

  def language_acquisition(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about language acquisition from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/language_acquisition.xml".format(self._url)
    result = API.get(url, name='LanguageAcquisition', **options)

    return result

  def music(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about music from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/music.xml".format(self._url)
    result = API.get(url, name='Music', **options)

    return result

  def creativity(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about creativity from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/creativity.xml".format(self._url)
    result = API.get(url, name='Creativity', **options)

    return result

  def infant_and_preschool_learning(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about infant and preschool learning from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/infant_and_preschool_learning.xml".format(self._url)
    result = API.get(url, name='InfantAndPreschoolLearning', **options)

    return result

  def literacy(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about lyteracy from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/literacy.xml".format(self._url)
    result = API.get(url, name='Literacy', **options)

    return result

  def intelligence(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about intelligence from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/intelligence.xml".format(self._url)
    result = API.get(url, name='Intelligence', **options)

    return result