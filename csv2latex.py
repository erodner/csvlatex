import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', help='input csv file')
parser.add_argument('--rows')
parser.add_argument('--cols')
parser.add_argument('--colformats')

args = parser.parse_args()

import csv
import json
import collections

def load_json_dict(fn):
    if not fn is None:
        my_dict = json.load(open(fn, 'r'), object_pairs_hook=collections.OrderedDict)
    else:
        my_dict = {}
    return my_dict

rows = load_json_dict(args.rows)
cols = load_json_dict(args.cols)
colformats = load_json_dict(args.colformats)


def strip_dict(d):
    for k in d:
        d[k] = d[k].strip()

def print_latex_table_row(arr):
    print (' & '.join(arr) + '\\\\')

def print_latex_table_header(arr):
    print ('\\begin{tabular}{l' + ('c' * (len(arr)-1)) + '}')
    print ('\\toprule')
    arrn = [ '\\textbf{' + v + '}' for v in arr ]
    print_latex_table_row(arrn)
    print ('\\midrule')

def print_latex_table_footer():
    print ('\\bottomrule')
    print ('\\end{tabular}')

with open(args.input, 'r') as f:
    csvf = csv.DictReader(f)
    first_col_name = csvf.fieldnames[0].strip()
    
    if len(cols)>0:
        fields = cols.keys()
        fieldnames = cols.values()
    else:
        fields = csvf.fieldnames
        fieldnames = fields

    print_latex_table_header(fieldnames)

    for line in csvf:
        strip_dict(line)
        if len(rows)>0:
            if not line[first_col_name] in rows:
                continue
            else:
                line[first_col_name] = rows[line[first_col_name]]
        if len(cols)>0:
            line = {k:line[k] for k in line if k in cols}

        values = []
        for k in fields:
            if k in colformats:
                try:
                    values.append(colformats[k].format(line[k]))
                except ValueError:
                    values.append(colformats[k].format(float(line[k])))
            else:
                values.append(line[k])
        print_latex_table_row(values)

    print_latex_table_footer()

    
