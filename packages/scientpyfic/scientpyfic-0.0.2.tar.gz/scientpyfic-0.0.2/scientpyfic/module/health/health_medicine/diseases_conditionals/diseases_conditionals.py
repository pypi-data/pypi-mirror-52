from .cancer import Cancer
from .cold_flu import ColdAndFlu
from .heart_health import HeartHealth

from scientpyfic.API import API

class DiseaseConditional:

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

    self.cancer = Cancer(url, title, description, pub_date, body, journals)
    self.cold_flu = ColdAndFlu(url, title, description, pub_date, body, journals)
    self.heart_health = HeartHealth(url, title, description, pub_date, body, journals)

  def bladder_disorders(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about bladder disorders in ScienceDaily.

    :return: a list with news about bladder disorders 
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/bladder_disorders.xml".format(self._url)
    result = API.get(url, name='BladderDisorder', **options, **kwargs)
    return result

  def copd(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about COPD in ScienceDaily.

    :return: a list with news about COPD
    """

    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }
    url = "{}/copd.xml".format(self._url)
    result = API.get(url, name='COPD', **options, **kwargs)
    return result

  def ebola(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about ebola in ScienceDaily.

    :return: a list with news about ebola
    """

    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/ebola.xml".format(self._url)
    result = API.get(url, name='Ebola', **options, **kwargs)

    return result

  def irritable_bowel_syndrome(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about irritable bowel syndrome in ScienceDaily.

    :return: a list with news about irritable bowel syndrome
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/irritable_bowel_syndrome.xml".format(self._url)
    result = API.get(url, name='IrritableBowelSyndrome', **options, **kwargs)
    return result

  def restless_leg_syndrome(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about restless leg syndrome in ScienceDaily.

    :return: a list with news about restless leg syndrome
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/restless_leg_syndrome.xml".format(self._url)
    result = API.get(url, name='ReslessLegSyndrome', **options, **kwargs)
    return result

  def cerebral_palsy(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about cerebral palsy in ScienceDaily.

    :return: a list with news about cebral palsy
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/cerebral_palsy.xml".format(self._url)
    result = API.get(url, name='CerebralPalsy', **options, **kwargs)
    return result

  def malaria(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about malaria in ScienceDaily.

    :return: a list with news about malaria
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/malaria.xml".format(self._url)
    result = API.get(url, name='Malaria', **options, **kwargs)
    return result

  def prostate_health(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about prostate health in ScienceDaily.

    :return: a list with news about prostate health
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/prostate_health.xml".format(self._url)
    result = API.get(url, name='ProstateHealth', **options, **kwargs)
    return result

  def birth_defects(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about birth defects in ScienceDaily.

    :return: a list with news about birth defects
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/birth_defects.xml".format(self._url)
    result = API.get(url, name='BirthDefects', **options, **kwargs)
    return result

  def eating_disorder_research(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about eating disorder in ScienceDaily.

    :return: a list with news about eating disorder
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/eating_disorders.xml".format(self._url)
    result = API.get(url, name='EatingDisorderResearch', **options, **kwargs)
    return result

  def pneumonia(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about pneumonia in ScienceDaily.

    :return: a list with news about pneumonia
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/cerebral_palsy.xml".format(self._url)
    result = API.get(url, name='Pneumonia', **options, **kwargs)
    return result

  def infectious_diseases(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about infectious disease in ScienceDaily.

    :return: a list with news about infectious disease
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/infectious_diseases.xml".format(self._url)
    result = API.get(url, name='InfectiousDiseases', **options, **kwargs)
    return result

  def alzheimers_research(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about alzheimer in ScienceDaily.

    :return: a list with news about alzheimer
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/alzheimer's.xml".format(self._url)
    result = API.get(url, name='AlzheimersResearch', **options, **kwargs)
    return result

  def allergy(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Latest news about allergy in ScienceDaily.

    :return: a list with news about allergy
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/allergy.xml".format(self._url)
    result = API.get(url, name='Allergy', **options, **kwargs)
    return result

  def epilepsy_research(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about epilepsy research from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/epilepsy.xml".format(self._url)
    result = API.get(url, name='EpilepsyResearch', **options, **kwargs)
    return result

  def fibromyalgia(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about fibromyalgia from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/fibromyalgia.xml".format(self._url)
    result = API.get(url, name='Fibromyalgia', **options, **kwargs)
    return result


  def gastrointestinal_problems(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about gastrointestinal problems from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/gastrointestinal_problems.xml".format(self._url)
    result = API.get(url, name='GastrointestinalProblems', **options, **kwargs)
    return result


  def mumps_measles_rubella(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about mups, measles & rubella from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/mumps,_measles,_rubella.xml".format(self._url)
    result = API.get(url, name='MumpsMeaslesRubella', **options, **kwargs)
    return result


  def obesity(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about obesity from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/obesity.xml".format(self._url)
    result = API.get(url, name='Obesity', **options, **kwargs)
    return result


  def thyroid_disease(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about thyroid disease from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/thyroid_disease.xml".format(self._url)
    result = API.get(url, name='ThyroidDisease', **options, **kwargs)
    return result


  def triglycerides(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about triglycerides from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/triglycerides.xml".format(self._url)
    result = API.get(url, name='Triglycerides', **options, **kwargs)
    return result


  def tuberculosis(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about tuberculosis from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/tuberculosis.xml".format(self._url)
    result = API.get(url, name='Tuberculosis', **options, **kwargs)
    return result


  def insomnia_research(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about insomina research from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/insomnia.xml".format(self._url)
    result = API.get(url, name='InsomniaResearch', **options, **kwargs)
    return result


  def hormone_disorders(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about hormone disorders from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/hormone_disorders.xml".format(self._url)
    result = API.get(url, name='HormoneDisorders', **options, **kwargs)
    return result


  def joint_pain(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about joint pain from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/joint_pain.xml".format(self._url)
    result = API.get(url, name='JointPain', **options, **kwargs)
    return result


  def ulcers(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about ulcers from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/ulcers.xml".format(self._url)
    result = API.get(url, name='Ulcers', **options, **kwargs)
    return result


  def colitis(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about colitis from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/colitis.xml".format(self._url)
    result = API.get(url, name='Colitis', **options, **kwargs)
    return result


  def cystic_fibrosis(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about cystic fibrosis from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/cystic_fibrosis.xml".format(self._url)
    result = API.get(url, name='CysticFibrosis', **options, **kwargs)
    return result


  def asthma(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about asthma from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/asthma.xml".format(self._url)
    result = API.get(url, name='Asthma', **options, **kwargs)
    return result


  def erectile_dysfunction(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about erectile dysfunction from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/erectile_dysfunction.xml".format(self._url)
    result = API.get(url, name='ErectileDysfunction', **options, **kwargs)
    return result


  def lyme_disease(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about lyme disease from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/lyme_disease.xml".format(self._url)
    result = API.get(url, name='LymeDisease', **options, **kwargs)
    return result


  def multiple_sclerosis_research(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about multiple sclerosis research from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/multiple_sclerosis.xml".format(self._url)
    result = API.get(url, name='MultipleSclerosisResearch', **options, **kwargs)
    return result


  def mental_health_research(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about mental health research from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/mental_health.xml".format(self._url)
    result = API.get(url, name='MentalHealthResearch', **options, **kwargs)
    return result


  def urology(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about urology from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/urology.xml".format(self._url)
    result = API.get(url, name='Urology', **options, **kwargs)
    return result


  def lung_disease(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about lung disease from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/lung_disease.xml".format(self._url)
    result = API.get(url, name='LungDisease', **options, **kwargs)
    return result


  def crohns_disease(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about crohn's disease from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/crohn's_disease.xml".format(self._url)
    result = API.get(url, name='CrohnsDisease', **options, **kwargs)
    return result


  def parkinsons_research(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about parkinson's research from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/parkinson's_disease.xml".format(self._url)
    result = API.get(url, name='ParkinsonsResearch', **options, **kwargs)
    return result


  def attention_deficit_disorder(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about attention deficit disorder from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/add_and_adhd.xml".format(self._url)
    result = API.get(url, name='AttentionDeficitDisorder', **options, **kwargs)
    return result


  def down_syndrome(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about down syndrome from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/down's_syndrome.xml".format(self._url)
    result = API.get(url, name='DownSyndrome', **options, **kwargs)
    return result


  def hiv_and_aids(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about HIV and aids from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/hiv_and_aids.xml".format(self._url)
    result = API.get(url, name='HivAndAids', **options, **kwargs)
    return result


  def hair_loss(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about hair loss from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/hair_loss.xml".format(self._url)
    result = API.get(url, name='HairLoss', **options, **kwargs)
    return result


  def herpes(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about herpes from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/herpes.xml".format(self._url)
    result = API.get(url, name='Herpes', **options, **kwargs)
    return result


  def anemia(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about anemia from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/anemia.xml".format(self._url)
    result = API.get(url, name='Anemia', **options, **kwargs)
    return result


  def arthritis(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about arthritis from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/arthritis.xml".format(self._url)
    result = API.get(url, name='Arthritis', **options, **kwargs)
    return result


  def blood_clots(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about blood clots from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/blood_clots.xml".format(self._url)
    result = API.get(url, name='BloodClots', **options, **kwargs)
    return result


  def chronic_fatigue_syndrome(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about chronic farigue syndrome from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/chronic_fatigue_syndrome.xml".format(self._url)
    result = API.get(url, name='ChronicFatigueSyndrome', **options, **kwargs)
    return result


  def lupus(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about lupus from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/lupus.xml".format(self._url)
    result = API.get(url, name='Lupus', **options, **kwargs)
    return result


  def muscular_dystrophy(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about muscular dystrophy from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/muscular_dystrophy.xml".format(self._url)
    result = API.get(url, name='MuscularDystrophy', **options, **kwargs)
    return result


  def psoriasis(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about psoriasis from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/psoriasis.xml".format(self._url)
    result = API.get(url, name='Psoriasis', **options, **kwargs)
    return result


  def sleep_disorder_research(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about sleep disorder research from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/sleep_disorders.xml".format(self._url)
    result = API.get(url, name='SleepDisorderResearch', **options, **kwargs)
    return result


  def headache_research(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about headace research from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/headaches.xml".format(self._url)
    result = API.get(url, name='HeadacheResearch', **options, **kwargs)
    return result


  def hypertension(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about hypertension from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/hypertension.xml".format(self._url)
    result = API.get(url, name='Hypertension', **options, **kwargs)
    return result


  def neuropathy(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about neuropathy from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/neuropathy.xml".format(self._url)
    result = API.get(url, name='Neuropathy', **options, **kwargs)
    return result


  def liver_disease(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about liver disease from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/liver_disease.xml".format(self._url)
    result = API.get(url, name='LiverDisease', **options, **kwargs)
    return result


  def sickle_cell_anemia(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about sickle cell anemia from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/sickle_cell_anemia.xml".format(self._url)
    result = API.get(url, name='SickleCellAnemia', **options, **kwargs)
    return result


  def amyotrophic_lateral_sclerosis(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about amyotrophic lateral sclerosis from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/amyotrophic_lateral_sclerosis.xml".format(self._url)
    result = API.get(url, name='AmyotrophicLateralSclerosis', **options, **kwargs)
    return result


  def diabetes(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about diabetes from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/diabetes.xml".format(self._url)
    result = API.get(url, name='Diabetes', **options, **kwargs)
    return result

  def hearing_loss(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about hearing loss from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/hearing_loss.xml".format(self._url)
    result = API.get(url, name='HearingLoss', **options, **kwargs)
    return result


  def osteoporosis(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about osteoporosis from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/osteoporosis.xml".format(self._url)
    result = API.get(url, name='Osteoporosis', **options, **kwargs)
    return result


  def kidney_disease(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about kidney disease from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/kidney_disease.xml".format(self._url)
    result = API.get(url, name='KidneyDisease', **options, **kwargs)
    return result


  def heartburn(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about heartburn from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/heartburn.xml".format(self._url)
    result = API.get(url, name='Heartburn', **options, **kwargs)
    return result


  def diseases_and_conditions(self, title=None, description=None, pub_date=None, body=None, journals=None, **kwargs):
    """
    Returns latest news about diseases and condition from ScienceDaily.
    """
   
    options = {
      'title': title if not title is None else self._title,
      'description': description if not description is None else self._description,
      'pub_date': pub_date if not pub_date is None else self._pub_date,
      'body': body if not body is None else self._body,
      'journals': journals if not journals is None else self._journals
    }

    url = "{}/diseases_and_conditions.xml".format(self._url)
    result = API.get(url, name='DiseasesAndConditions', **options, **kwargs)
    return result
