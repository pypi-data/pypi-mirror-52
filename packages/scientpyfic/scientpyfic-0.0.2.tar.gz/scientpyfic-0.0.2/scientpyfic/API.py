import requests
from bs4 import BeautifulSoup as bs

from scientpyfic.random_user_agent import random_headers
from .exception import PageErrorException

class API:

  @classmethod
  def get_journals(cls, journals):
    result = []
    if not journals is None:
      for journal in journals.find_all('li'):
        result.append(type('Journal', (object,), { 'journal': journal.get_text() }))

    return result

  @classmethod
  def get_content(cls, content):
    result = content.get_text() if not content is None else ""
    return result

  @classmethod
  def get(cls, url, name, title=None, pub_date=None, description=None, 
    body=None, journals=None, **kwargs):
    page = requests.get(url, headers=random_headers())

    if page.status_code != requests.codes.ok:
      raise PageErrorException(page.content.decode('utf-8', 'ignore'))

    soup = bs(page.content, "xml")

    latest = True
    if 'latest' in kwargs:
      latest = kwargs['latest']

    results = []
    _title, _description, _pub_date, _body, _journals = [ None ] * 5
    for item in soup.find_all('item'):

      _description = item.description.get_text() if description else None
      _pub_date = item.pubDate.string if pub_date else None
      _title = item.title.string if title else None

      if (body or journals) and latest:
        guid = item.guid.string
        response = requests.get(guid, headers=random_headers())
        
        html_content = bs(response.content, "html.parser")

        if body:
          text = html_content.find('div', attrs={'id': 'text'})
          _body = API.get_content(text)

        if journals:
          journals = html_content.find('div', attrs={'id': 'journal_references'})
          _journals = API.get_journals(journals)

        if type(latest) is int:
          latest = latest - 1

      obj = type(name, (object,), { 'title': _title, 'description': _description, 'pub_date': _pub_date,
        'body': _body, 'journals': _journals})
      results.append(obj)

    return results