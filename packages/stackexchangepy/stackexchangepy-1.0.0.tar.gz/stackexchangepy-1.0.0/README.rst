StackExchangePy
---------------

.. image:: https://s7.postimg.cc/k6s2galrf/pylogo.png  


.. image:: https://img.shields.io/badge/1.0.0-stackexchangepy-red?style=flat-square


Installation
***************

>>> pip install stackexchangepy

Documentation
***************

Documentation can be found `here <https://github.com/monzita/stackexchangepy/wiki>`_.

Example code
***************

>>> from stackexchangepy.client import StackExchangeClient
>>>
>>> client = StackExchangeClient(access_token='token', key='key')
>>>
>>>
>>> answers, _ = client.answers.all()
>>>
>>> # do something with answers
>>>
>>> posts, _ = client.posts.all()
>>>
>>> # do something with posts
>>>
>>> posts[0].post_id
1234567
>>> posts[0].score
100
>>> posts[0].type
question
>>>


Licence
***************

`GNU <https://github.com/monzita/stackexchangepy/LICENSE>`_
