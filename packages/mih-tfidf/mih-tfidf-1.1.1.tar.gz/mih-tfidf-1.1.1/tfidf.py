# encoding: utf-8

import itertools
import numpy  as np
import pandas as pd

from collections import Counter


class TFIDF(object):


    def flatten(self, l):

        return list(itertools.chain.from_iterable(l))



    def tf(self, doces):

        d    = self.flatten(doces)
        d_tf = pd.DataFrame.from_dict(Counter(d), orient='index').\
                reset_index().rename(columns={'index':'term', 0:'tf'})

        return d_tf



    def idf(self, doces):

        d     = self.flatten(pd.Series(doces).apply(np.unique))
        d_idf = pd.DataFrame.from_dict(Counter(d), orient='index').\
                reset_index().rename(columns={'index':'term', 0:'df'})

        d_idf['idf'] = len(doces) / d_idf['df']

        return d_idf



    def tfidf(self, doces):

        d_tf  = self.tf(doces)
        d_idf = self.idf(doces)

        d_tfidf = pd.merge(d_tf, d_idf, on='term')
        d_tfidf['tfidf'] = d_tfidf.tf * d_tfidf.idf
        d_tfidf = d_tfidf.sort_values(by='tfidf', ascending=False)

        return d_tfidf



    def top(self, doces, ratio):
        """
        Parameters
        ----------
        ratio : int or float
            int means num, float [0, 1] means ratio, float > 1, int(ratio)
        """

        d_tfidf = self.tfidf(doces)

        if ratio < 1:
            ratio = ratio * d_tfidf.shape[0]

        ratio = int(ratio)

        return d_tfidf.head(ratio)
