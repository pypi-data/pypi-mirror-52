from scientpyfic.API import API


class EducationLearning:

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

  def public_health_education(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list about public health education from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/public_health_education.xml".format(self._url)
    result = API.get(url, name='PublicHealthEducation', **options, **kwargs)

    return result

  def medical_education_and_training(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list about medical education training from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/medical_education_and_training.xml".format(self._url)
    result = API.get(url, name='MedicalEducationTraining', **options, **kwargs)

    return result

  def patient_education_and_counseling(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns a list about patient education counseling from ScienceDaily.
    """
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/patient_education_and_counseling.xml".format(self._url)
    result = API.get(url, name='PatientEducationCounseling', **options, **kwargs)

    return result

