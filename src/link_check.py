import sys
import urllib
from urllib import request, parse
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
from collections import deque


class LinkChecker(HTMLParser):
    SEARCH_ATTRS = set(['href', 'src'])
    AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
            'AppleWebKit/537.36 (KHTML, like Gecko) ' \
            'Chrome/60.0.3112.113 Safari/537.36'


    def __init__(self, verbose=False):
        super().__init__()
        self._verbose = verbose


    def check(self, url_start):
        self._url_start = url_start
        self._checked_links = set()
        self._pages_to_get = deque()
        self._pages_to_get.appendleft(self._url_start)
        '''Loop through remaining pages, looking for HTML responses'''
        while self._pages_to_get:
            page = self._pages_to_get.pop()
            req = request.Request(page, headers={'User-Agent': LinkChecker.AGENT})
            res = request.urlopen(req)
            if 'html' in res.headers['content-type']:
                with res as f:
                    body = f.read().decode('utf-8', errors='ignore')
                    self.feed(body)


    def handle_starttag(self, tag, attrs):
        '''
        Override parent method and check tag for our attributes
        '''
        for attr in attrs:
            # ('href', 'http://google.com')
            if attr[0] in LinkChecker.SEARCH_ATTRS and \
               attr[1] not in self._checked_links:
                self._handle_link(attr[1])


    def _handle_link(self, link):
        '''
        Send a HEAD request to the link, catch any pesky errors
        '''
        if not bool(urlparse(link).netloc):  # relative link?
            link = urljoin(self._url_start, link)
        try:
            req = request.Request(link, headers={'User-Agent': LinkChecker.AGENT},
                                  method='HEAD')
            status = request.urlopen(req).getcode()
        except urllib.error.HTTPError as e:
            print('HTTPError: {} - {}'.format(e.code, link))  # (e.g. 404, 501, etc)
        except urllib.error.URLError as e:
            print('URLError: {} - {}'.format(e.reason, link))  # (e.g. conn. refused)
        except ValueError as e:
            print('ValueError {} - {}'.format(e, link))  # (e.g. missing protocol http)
        else:
            if self._verbose:
                print('{} - {}'.format(status, link))
        if self._url_start in link:
            self._pages_to_get.appendleft(link)
        self._checked_links.add(link)


def main():
    # check for verbose tag
    # enable this as a script, e.g., 'https://healeycodes.com/ v'
    lc = LinkChecker()
    url_root = sys.argv[1]
    lc.check(url_root)


if __name__ == '__main__':
    main()

