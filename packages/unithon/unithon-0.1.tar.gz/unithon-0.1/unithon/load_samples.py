#!/usr/bin/env python

# Copyright 2019 David Garcia
# See LICENSE for details.

__author__ = "David Garcia <dvid@usal.es>"


import pkg_resources
import pandas as pd


def load_csv_test_data():
    resource_package = __name__
    resource_path = '/'.join(('data', 'test.csv'))

    if pkg_resources.resource_exists(resource_package, resource_path):
        return pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError
