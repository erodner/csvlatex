import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', help='input csv file')
parser.add_argument('--rows')
parser.add_argument('--cols')


args = parser.parse_args()

import csv
import json
import collections

if not args.rows is None:
    rows = json.load(open(args.rows, 'r'), object_pairs_hook=collections.OrderedDict)
else:
    rows = {}

if not args.cols is None:
    cols = json.load(open(args.cols, 'r'), object_pairs_hook=collections.OrderedDict)
else:
    cols = {}

def strip_dict(d):
    for k in d:
        d[k] = d[k].strip()

def print_latex_table_row(arr):
    print (' & '.join(arr) + '\\\\')

def print_latex_table_header(arr):
    print ('\\begin{tabular}{l' + ('c' * (len(arr)-1)) + '}')
    print ('\\toprule')
    print_latex_table_row(arr)
    print ('\\midrule')

def print_latex_table_footer():
    print ('\\bottomrule')
    print ('\\end{tabular}')

with open(args.input, 'r') as f:
    csvf = csv.DictReader(f)
    first_col_name = csvf.fieldnames[0]
    
    if len(cols)>0:
        fields = cols.keys()
        fieldnames = cols.values()
    else:
        fields = csvf.fieldnames
        fieldnames = fields

    print_latex_table_header(fieldnames)

    for line in csvf:
        strip_dict(line)
        if len(rows)>0 and not line[first_col_name] in rows:
            continue
        if len(cols)>0:
            line = {k:line[k] for k in line if k in cols}
        values = [ line[k] for k in fields ]
        print_latex_table_row(values)

    print_latex_table_footer()

    
