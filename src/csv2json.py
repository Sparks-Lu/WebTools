import os
import sys


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
        contents = []
        key = None
        for line in lines:
            # keep ending \t
            line = line.strip(' \n').replace('"', '\\"')
            if line.find('\t') >= 0:
                # new row
                values = line.split('\t')
                contents.append(values)
            else:
                # append to last row
                if len(contents) > 0:
                    contents[-1].append(line)
                else:
                    contents.append(line)

        # write json
        if fn_json is None:
            dn = os.path.dirname(fn_csv)
            if dn == '':
                dn = '.'
            fn_json = '{}/{}.json'.format(dn, os.path.basename(fn_csv))
        with open(fn_json, 'w', encoding='UTF-8') as f:
            for idx_row, r in enumerate(contents):
                line = '['
                if type(r) is str:
                    line = '["{}"'.format(r)
                else:
                    for idx_span, span in enumerate(r):
                        if idx_span == 0:
                            line += '"{}"'.format(span)
                        elif len(span) > 0:
                            line += ',"{}"'.format(span)
                if idx_row == len(contents) - 1:
                    # No comma and newline for last row in table
                    print('Will not output comma in last row.')
                    line += ']'
                else:
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

