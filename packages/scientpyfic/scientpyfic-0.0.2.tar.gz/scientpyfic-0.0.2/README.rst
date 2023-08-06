ScientPYfic
---------------

.. image:: https://github.com/monzita/scientpyfic/blob/master/scientpyfic.png

Get the latest news from ScienceDaily. 

.. image:: https://github.githubassets.com/images/icons/emoji/unicode/1f4f0.png

Installation
**********************

>>> pip install scientpyfic

Documentation
**********************

Can be seen `here <https://github.com/monzita/scientpyfic/wiki>`_

Example usage
**********************
  
>>> from scientpyfic.client import ScientPyClient
>>>
>>>
>>> client = ScientPyClient()
>>>
>>> all = client.all.all()
>>>
>>> for news in all:
>>>   # news.title
>>>   # news.description
>>>   # news.pub_date
>>>
>>> 
>>> top = client.top.top(body=True, journals=True)
>>>
>>> for news in top:
>>>   # news.title
>>>   # news.description
>>>   # news.pub_date
>>>   # news.body
>>>   # news.journals

Licence
**********************

`MIT <https://github.com/monzita/scientpyfic/LICENSE>`_