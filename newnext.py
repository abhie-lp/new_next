#!/usr/bin/python

import os
import re
import shutil
from argparse import ArgumentParser
from glob import glob

DEFAULT_SEQUENCE = "_001"
parser = ArgumentParser(
    description="Create new file/folder by incrementing the sequence of the latest file/folder created",
    usage="newnext <filename>"
)

parser.add_argument("name", help="Name of the file/folder to create.")
parser.add_argument(
    "-c", "--copy", action="store", const="", nargs="?", type=str,
    help="By default copy the latest file or else the file given"
)

args = parser.parse_args()
current_dir = os.path.abspath(os.path.curdir)
files = glob(f"{args.name}[\\.-_]*", )
latest_file = None
if files:
    latest_file = max(files)
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

if args.copy is not None and latest_file:
    if args.copy == "":
        shutil.copy(latest_file, new_file)
    elif os.path.isfile(args.copy):
        shutil.copy(args.copy, new_file)
    else:
        parser.error(f"Given '{args.copy}' file to copy is not a file.")
else:
    open(new_file, "a").close()
print(os.path.join(current_dir, new_file))
