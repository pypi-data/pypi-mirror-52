#!/usr/bin/env python

"""Convert a CSV confustion matrix to a JSON confusion matrix."""

# core modules
import csv

# 3rd party modules
import numpy as np

# internal modules
import clana.io


def main(input_csv, output_json):
    cm = read_csv_cm(input_csv)
    clana.io.write_cm(output_json, cm)


def read_csv_cm(input_csv):
    cm_lists = []
    with open(input_csv, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in spamreader:
            cm_lists.append([int(el) for el in row])
    return np.array(cm_lists)


main(
    "/home/moose/GitHub/supaiku/aggregate_cm.csv", "/home/moose/GitHub/supaiku/cm.json"
)
