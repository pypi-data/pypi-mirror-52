"""
# gfs.py
Delete files with the grand-father-son scheme.
"""
#!/usr/bin/python3
import argparse
import json
import operator
import os
import time
from collections import OrderedDict
from math import ceil

from helputils.core import evenspread, listdir_fullpath, log
from six import iteritems

from . import __version__

day = 24 * 60 * 60
week = 7 * day
month = 30 * day
six_months = 6 * month
year = 365 * day
keep = {
    "day": 1,
    "week": 3,
    "month": 1,
    "six_months": 1,
    "year": 1,
    "older_one_year": 0
}


class GFSEraser():

    def __init__(self):
        self.times = {
            "day": list(),
            "week": list(),
            "month": list(),
            "six_months": list(),
            "year": list(),
            "older_one_year": list()
        }

    def sort_to_times(self, fn, age):
        if day >= age:
            self.times["day"].append((age, fn))
        elif day < age <= week:
            self.times["week"].append((age, fn))
        elif week < age <= month:
            self.times["month"].append((age, fn))
        elif month < age <= six_months:
            self.times["six_months"].append((age, fn))
        elif six_months < age <= year:
            self.times["year"].append((age, fn))
        elif year < age:
            self.times["older_one_year"].append((age, fn))

    def delete_gfs(self, directory, keep=keep, dry_run=False):
        """Delete files in given directory in gfs style.

        keep := Dictionary specifying how many # of files to keep for period of time
                keep = {
                   "day": 1,
                   "week": 7,
                   "month": 1,
                   "six_months": 1,
                   "year": 1,
                   "older_one_year": 0
                }

        Algorithm:
        - Get all backups from last week, apply evenspread and add results to exclude_list
          Analog for last month, 3 months, 6 months and 12 months.
        - Eavenly grab specified # of files from grouped times.
        - Delete all files that are not in exclude_list.
        """
        fns = listdir_fullpath(directory)
        now = time.time()
        for x in fns:
            age = now - os.path.getmtime(x)
            self.sort_to_times(x, age)
        # This works, because "age" is the first item of our tuple
        sorted_times = OrderedDict(sorted(self.times.items(), key=operator.itemgetter(1)))
        exclude = list()
        for k, v in iteritems(sorted_times):
            # evenspread doesn't care about the items time, but only about the order, so give it a sorted list by time
            if not v:
                continue
            for age, fn in evenspread(v, keep[k]):
                exclude.append(fn)
        log.info("Excluded: %s\n" % len(exclude))
        for x in fns:
            if x not in exclude:
                log.info("Deleting %s" % x )
                if not dry_run:
                    os.remove(x)


def main():
    description = "%s\n\nVersion: helputils.gfs %s" % (__doc__, __version__)
    argp = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    argp.add_argument(
        "-k", 
        required=True,
        help="Specify the keep rule. " \
        "Example: `-k {'day':1,'week':7,'month':1,'six_months':1,'year':1,'older_one_year':0}`"
    )
    argp.add_argument(
        "-d", 
        required=True,
        help="Specify the directory to delete files in accordance with the keep rule."
    )
    argp.add_argument("-dry", action="store_true", help="Run without deleting anything.", default=False)
    arg = argp.parse_args()
    keep = json.loads(arg.k)
    GFSEraser().delete_gfs(arg.d, keep, arg.dry)
