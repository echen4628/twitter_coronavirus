#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths',nargs='+',required=True)
parser.add_argument('--output_path',required=True)
parser.add_argument('--keys',nargs='+',required=True)
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import re
import pandas as pd
import pdb
def extract_date(filename):
    match = re.search(r'\d{2}-\d{2}-\d{2}', filename)
    if match:
        date = match.group()
        year, month, day = date.split('-')
        formatted_date = f'20{year}-{month}-{day}'
        return formatted_date
    else:
        return None


# load each of the input paths
data = defaultdict(lambda: defaultdict(int))
# first key is the hashtag and the second level key is the date
for i, path in enumerate(args.input_paths):
    date = extract_date(path)
    with open(path) as f:
        tmp = json.load(f)
        for key in args.keys:
            if key in tmp.keys(): 
                key_total = sum(tmp[key].values())
                data[key][date] += key_total

# write the output path
#with open(args.output_path,'w') as f:
#    f.write(json.dumps(total))

# plot
df = pd.DataFrame(data)

df.index = pd.to_datetime(df.index)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()
df.plot(ax=ax)
#for key in args.keys:
#    ax.plot(total[key].keys(),total[key].values()) 
#pdb.set_trace()
#ax.set_xticks(np.arange(len(all_dates))[::10])
#ax.set_xticklabels(list(all_dates.values())[::10], rotation=45)
ax.set_xlabel("Dates")
ax.set_ylabel("Counts")
ax.set_title("Daily Covid Related Tweet Frequency in 2020")
plt.xticks(rotation=45)
fig.savefig(f"{args.output_path}.png")

plt.close(fig)
