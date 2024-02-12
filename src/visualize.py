#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items:
    print(k,':',v)

categories = [item[0] for item in items[:10]][::-1]
values = [item[1] for item in items[:10]][::-1]

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Malgun Gothic'
if "country" in args.input_path:
    x_axis_label = "Country of Origin"
elif "lang" in args.input_path:
    x_axis_label = "Language of Origin"

x_pos = np.arange(len(categories))
plt.bar(x_pos, values)
plt.xticks(x_pos, categories)
plt.ylabel("Counts")
plt.xlabel(x_axis_label)
plt.title(f"Top 10 origins for Tweets tagged ${args.key}")
plt.savefig(f"{args.input_path}-{args.key}.png")
plt.close()

