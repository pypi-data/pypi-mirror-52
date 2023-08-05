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


class MethylationContextHistogram(StatisticHistogram):
    def __init__(self,args):
        StatisticHistogram.__init__(self, args)
        self.context_obs = collections.Counter() #(bismark_call_tag)=> observations


    def processRead(self,read):
        if not read.is_paired or not read.has_tag('XM') or not read.is_read1 or read.is_duplicate or read.has_tag('RR'):
            return

        tags = dict( read.tags )
        for tag in 'zhx':
            self.context_obs[tag] += tags.get(f's{tag}')
            self.context_obs[tag.upper()] += tags.get(f's{tag.upper()}')

    def __repr__(self):
        return f'Methylation status.'

    def get_df(self):
        x = self.context_obs
        return pd.DataFrame(
        {   'ratio':
            {
             'CpG':x['Z']/(x['z']+x['Z']),
             'CHG':x['X']/(x['x']+x['X']),
             'CHH':x['H']/(x['h']+x['H']) },
           'methylated':{
               'CpG':x['Z'],
             'CHG':x['X'],
             'CHH':x['H']
           },
         'unmethylated':{
             'CpG':x['z'],
             'CHG':x['x'],
             'CHH':x['h']
           }
        })

    def plot(self, target_path, title=None):

        df = self.get_df()
        ####### Methylation ratio plot:
        name ='methylation_pct'

        (df['ratio']*100).plot.bar()
        ax = plt.gca()
        for p in ax.patches:
            ax.annotate(
                f'{p.get_height():.1f}%',
                (p.get_x()+p.get_width()/2, p.get_height() * 1.005),
                va='bottom', ha='center')
        ax.set_ylim(0,110)
        ax.set_xlabel('Methylation context')
        ax.set_ylabel('% methylated')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.show()
        if title is not None:
            plt.title(title)
        plt.tight_layout()
        plt.savefig(target_path.replace('.png',f'.{name}.png'))


        ax.set_yscale('log')
        ax.set_ylim(0.01,110)

        plt.tight_layout()
        plt.savefig(target_path.replace('.png',f'.{name}.log.png'))
        plt.close()
        ########
        name ='methylation_absolute'

        (df[['methylated','unmethylated']]).plot.bar()
        ax = plt.gca()
        for p in ax.patches:
            ax.annotate(
                f'{p.get_height()}',
                (p.get_x()+p.get_width()/2, p.get_height() * 1.005),
                va='bottom', ha='center')

        ax.set_xlabel('Methylation context')
        ax.set_ylabel('Bases total')
        plt.tight_layout()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        if title is not None:
            plt.title(title)
        plt.tight_layout()
        plt.savefig(target_path.replace('.png',f'.{name}.png'))

        ax.set_yscale('log')
        plt.tight_layout()
        plt.savefig(target_path.replace('.png',f'.{name}.log.png'))
        plt.close()


    def to_csv(self, path):

        self.get_df().to_csv(path)
