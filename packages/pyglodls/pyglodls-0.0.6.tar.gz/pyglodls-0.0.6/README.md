#### To install:
`$ pip install pyglodls`

#### Usage
```python
>>> import pyglodls
>>> s = pyglodls.search('search query')
>>> s
[
<Torrent(title='result 1')>,
<Torrent(title='result 2')>
]
>>> s[0].title
u'result 1'
>>> s[0].size
123.4
>>> s[0].seeds
234
>>> s[0].leechers
456
>>> s[0].magnet
u'magnet:?xt=urn:btih:......'
```
#### Optional parameters
See glodls.py for all permissible values for these parameters.
```python
pyglodls.search('search query',
                category=CATEGORY.ALL,
                status=STATUS.ACTIVE_TRANSFERS,
                source=SOURCE.LOCAL_PLUS_EXTERNAL,
                language=LANGUAGE.ALL,
                sort=SORT.ADDED,
                order=ORDER.DESCENDING)
```
