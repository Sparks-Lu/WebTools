import os
import sys
import collections


class CSV2JSON(object):
    def __init__(self):
        pass


    def __del__(self):
        pass


    def convert(self, fn_csv, fn_json=None):
        lines = []
        with open(fn_csv, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            f.close()
        if len(lines) == 0:
            return

        # parse csv
        contents = collections.OrderedDict()
        key = None
        for line in lines:
            # keep ending \t
            line = line.strip(' \n').replace('"', '\\"')
            if line.find('\t') >= 0:
                key, value = line.split('\t')
                contents[key] = value
            elif key is not None:
                # append to last key
                contents[key] = contents[key] + '\t' + line

        # write json
        if fn_json is None:
            dn = os.path.dirname(fn_csv)
            if dn == '':
                dn = '.'
            fn_json = '{}/{}.json'.format(dn, os.path.basename(fn_csv))
        with open(fn_json, 'w', encoding='UTF-8') as f:
            for k in contents.keys():
                line = '["'
                line += k
                line += '"'
                values = contents[k].split('\t')
                for v in values:
                    if len(v) > 0:
                        line += ',"{}"'.format(v)
                line += '],\n'
                f.write(line)
            f.close()
            print('JSON was written as {} successfully.'.format(fn_json))


def main():
    cj = CSV2JSON()
    if len(sys.argv) < 2:
        print('Usage: python {} <csv_filename>'.format(__file__))
        return
    fn_input = sys.argv[1]
    cj.convert(fn_input)


if __name__ == '__main__':
    main()

