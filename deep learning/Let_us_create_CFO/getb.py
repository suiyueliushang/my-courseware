# -*- coding: UTF-8 -*-
import numpy as np
import os
import csv
from os.path import join


def getb(self):
    B = []
    if os.path.exists(join('label', str(self.id) + '.csv')):
        with open(join('label', str(self.id) + '.csv')) as f1:
            reader = csv.reader(f1)
            original = list(reader)
            for row in original:
                if '1024' not in row:
                    B.append(row)
    print(B)
    return B

