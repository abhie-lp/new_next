#!/usr/bin/python

import os
import re
from argparse import ArgumentParser
from glob import glob

DEFAULT_SEQUENCE = "_001"
parser = ArgumentParser(
    description="Create new file/folder by incrementing the sequence of the latest file/folder created",
    usage="newnext <filename>"
)

parser.add_argument("name", help="Name of the file/folder to create.")

args = parser.parse_args()
current_dir = os.path.abspath(os.path.curdir)
files = glob(f"{args.name}[\\.-_]*", )
if files:
    latest_file = max(files, key=os.path.getctime)
    escaped_basename = re.escape(args.name)
    sequence = re.search(rf"{escaped_basename}([-._]?)(\d+).*", latest_file)
    if sequence:
        separator, sequence = sequence.group(1), sequence.group(2)
        new_file = (args.name + separator +
                    str(int(sequence) + 1).zfill(len(sequence)))
    else:
        new_file = args.name + "_002"
    new_file = new_file + "." + latest_file.rsplit(".", 1)[1]
else:
    new_file = args.name + DEFAULT_SEQUENCE + ".txt"
try:
    open(new_file, "a").close()
    print(os.path.join(current_dir, new_file))
except Exception as e:
    print(e)
