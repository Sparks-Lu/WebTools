import logging
import json
import requests

'''
Keep only used CSS based on coverage file exported from Chrome dev tools
'''
class CSSCleaner(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)


    def __del__(self):
        pass


    def clean(self, fn_coverage):
        css_used = []
        with open(fn_coverage, 'rb') as f:
            data = json.load(f)
            for data_url in data:
                url = data_url['url']
                if not url.endswith('.css'):
                    continue
                response = requests.get(url)
                if response.status_code != 200:
                    self._logger.error('GET %s error!' % url)
                    continue
                ranges = data_url['ranges']
                for r in ranges:
                    # start/end character in file
                    start = r['start']
                    end = r['end']
                    css_used.append(response.text[start : end + 1])
            css_used = ''.join(css_used)
            self._logger.info('CSS used: %s' % css_used)
            f.close()
        return css_used


def main():
    logging.basicConfig()
    import sys
    if len(sys.argv) < 2:
        print('Usage python {} fn_coverage'.format(__name__))
        return 0
    fn_coverage = sys.argv[1]
    cleaner = CSSCleaner()
    css_used = cleaner.clean(fn_coverage)
    fn_cleaned = 'cleaned.css'
    with open(fn_cleaned, 'w') as f:
        f.write(css_used)
        f.close()
        print('Wrote cleaned css to {}'.format(fn_cleaned))


if __name__ == '__main__':
        main()
