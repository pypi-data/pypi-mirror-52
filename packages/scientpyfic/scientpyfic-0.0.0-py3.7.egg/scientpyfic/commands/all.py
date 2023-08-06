from requests import get
from bs4 import BeautifulSoup as bs

from scientpyfic.random_user_agent import random_headers

class All:

  @classmethod
  def exec(cls, url, number_of_news=0, format_display='pb%t', tlen=0, dlen=0):
    line_delimeter = '-'*10

    page = get(url, headers=random_headers())
    soup = bs(page.content, "xml")

    list_size = int(number_of_news) if int(number_of_news) > 0 else len(soup.find_all('item'))
    print('\n')
    for item in soup.find_all('item')[:list_size]:
      description_size = int(dlen) if int(dlen) > 0 else len(item.description.get_text())
      title_size = int(tlen) if int(tlen) > 0 else len(item.title.string)

      description = item.description.get_text()[:description_size]
      pub_date = item.pubDate.string
      title = item.title.string[:title_size]

      if format_display == 'pb%t':
        print("{}: {}\n{}\n".format(pub_date, title, line_delimeter))
      elif format_display == 'pb%t%d':
        print("{}: {}\n{}\n{}\n".format(pub_date, title, description, line_delimeter))
      elif format_display == 'pb%d':
        print("{}: {}\n{}\n".format(pub_date, description, line_delimeter))
      elif format_display == 'd%pb':
        print("{}: {}\n{}\n".format(description, pub_date, line_delimeter))
      elif format_display == 't':
        print("{}: {}\n{}\n".format(pub_date, description, line_delimeter))
      elif format_display == 'pb':
        print("{}\n{}\n".format(pub_date, line_delimeter))
      elif format_display == 'd':
        print("{}\n{}\n".format(description, line_delimeter))