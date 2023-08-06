from urllib.parse import urljoin, urlparse, urlunparse
from posixpath import normpath
import re

def url_join(domain, url):
    '''
    url 拼接
    url = 'http://karpathy.github.io/2014/07/03/feature-learning-escapades/'
    url_join(url, '../assets/nips2012.jpeg')
    'http://karpathy.github.io/2014/07/03/assets/nips2012.jpeg'
    url_join(url, './assets/nips2012.jpeg')
    'http://karpathy.github.io/2014/07/03/feature-learning-escapades/assets/nips2012.jpeg'
    url_join(url, '/assets/nips2012.jpeg')
    'http://karpathy.github.io/assets/nips2012.jpeg'
    url_join(url,'http://karpathy.github.io/assets/nips2012.jpeg')
    'http://karpathy.github.io/assets/nips2012.jpeg'
    '''
    if not url.startswith('.') and not url.startswith('/'):
        return url
    url1 = urljoin(domain, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))


def remove_tags(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }
    re_doctype = re.compile('<!DOCTYPE.*?>')
    re_nav = re.compile('<nav.+</nav>')
    re_cdata = re.compile('//<!\[CDATA\[.*//\]\]>', re.DOTALL)
    re_script = re.compile(
        '<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.DOTALL | re.I)
    re_style = re.compile(
        '<\s*style[^>]*>.*?<\s*/\s*style\s*>', re.DOTALL | re.I)
    re_textarea = re.compile(
        '<\s*textarea[^>]*>.*?<\s*/\s*textarea\s*>', re.DOTALL | re.I)
    re_br = re.compile('<br\s*?/?>')
    re_h = re.compile('</?\w+.*?>', re.DOTALL)
    re_comment = re.compile('<!--.*?-->', re.DOTALL)
    re_space = re.compile(' +')
    s = re_cdata.sub('', htmlstr)
    s = re_doctype.sub('', s)
    s = re_nav.sub('', s)
    s = re_script.sub('', s)
    s = re_style.sub('', s)
    s = re_textarea.sub('', s)
    s = re_br.sub('', s)
    s = re_h.sub('', s)
    s = re_comment.sub('', s)
    s = re.sub('\\t', '', s)
    s = re_space.sub(' ', s)
    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(s)
    while sz:
        key = sz.group('name')
        try:
            s = re_charEntity.sub(CHAR_ENTITIES[key], s, 1)
            sz = re_charEntity.search(s)
        except KeyError:
            # 以空串代替
            s = re_charEntity.sub('', s, 1)
            sz = re_charEntity.search(s)
    return s

