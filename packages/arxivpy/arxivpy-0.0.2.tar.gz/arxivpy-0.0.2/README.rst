ArXiVPy
-----------------------

.. image:: https://github.com/monzita/arXivPy/blob/master/arxivpy.png

.. image :: https://img.shields.io/badge/0.0.1-arXivPy-green?style=flat-square

Find all papers from arXiv based on some query ( + option for downloading them ) 

.. image:: https://github.githubassets.com/images/icons/emoji/unicode/1f4f0.png


Installation
**********************

>>> pip install arxivpy

Documentation
**********************

Official documentation can be found `here <https://github.com/monzita/arxivpy/wiki>`_

Example usage
**********************

>>> from arxivpy.client import ArXivPyClient
>>>
>>> client = ArXivPyClient()
>>>
>>> quantum = client.simple(query='quantum computing', page=2, download=True,
>>>                         path='path', downloadonly=10)
>>>
>>>
>>> algorithms = client.advanced(term='algorithms',
>>>                              classification='computer_science', size=200)
>>>
>>>
>>>
>>> alg_ds = client.advanced(terms=[{term: 'algorithms', field: 'title'},
>>>                                 {term: 'data structures', field: 'title'}],
>>>                      classification='computer_science', size=200)
>>>

Licence
**********************

`MIT <https://github.com/monzita/arxivpy/LICENSE>`_