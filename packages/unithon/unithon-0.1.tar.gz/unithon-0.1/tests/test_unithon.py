#!/usr/bin/env python

# Copyright 2019 David Garcia
# See LICENSE for details.

__author__ = "David Garcia <dvid@usal.es>"

import pytest

from unithon import load_samples
import unithon


def test_unithon():
    test = load_samples.load_csv_test_data()
    print('exito')


if __name__ == '__main__':
    test_unithon()
