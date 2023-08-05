#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .statistic import StatisticHistogram
import singlecellmultiomics.pyutils as pyutils
import collections
import pandas as pd

import matplotlib
matplotlib.rcParams['figure.dpi'] = 160
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class DataTypeHistogram(StatisticHistogram):
    def __init__(self,args):
        StatisticHistogram.__init__(self, args)
        self.histogram = collections.Counter()

    def processRead(self,read):
        if read.has_tag('MX'):
            self.histogram[read.get_tag('MX')]+=1
        else:
            self.histogram["Not demultiplexed"]+=1

        if read.has_tag('dt'):
            self.histogram[read.get_tag('dt')]+=1
        
    def __repr__(self):
        rt = 'Rejection reasons:'
        for dataType, obs in self.histogram.most_common():
            rt += f'{dataType}\t:\t{obs}\n'
        return rt
    def __iter__(self):
        return iter(self.histogram.most_common())

    def plot(self, target_path, title=None):
        df = pd.DataFrame.from_dict({'DataType':dict(self)}).T

        df.plot.bar(figsize=(10,4)).legend(bbox_to_anchor=(1, 0.98))
        if title is not None:
            plt.title(title)

        plt.tight_layout()
        plt.subplots_adjust(right=0.6)
        plt.savefig(target_path)

        ax = plt.gca()
        ax.set_yscale('log')
        plt.savefig(target_path.replace('.png','.log.png'))
        plt.close()
