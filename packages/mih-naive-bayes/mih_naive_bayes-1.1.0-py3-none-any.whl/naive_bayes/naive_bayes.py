# encoding: utf-8

import itertools
import numpy   as np
import pandas  as pd
import _pickle as pickle

from collections import Counter


class NaiveBayes(object):


    def __init__(self):

        self._logprior      = {}
        self._loglikelihood = None
        self._V             = None
        self._C             = None


    def flatten(self, l):

        return list(itertools.chain.from_iterable(l))


    def logprior(self, C):

        c = Counter(C)

        # @deprecated
        # p = np.log2(c.values()) - np.log2(len(C))
        p = np.log2(list(c.values())) - np.log2(len(C))

        # @deprecated
        # self._logprior = {c.keys()[i]:p[i] for i in range(len(c.keys()))}
        self._logprior = {list(c.keys())[i]:p[i] for i in range(len(list(c.keys())))}


    def V(self, D):

        D_flatten = self.flatten(D)
        self._V = np.unique(D_flatten)


    def cwords(self, D, C):
        """ make dict{c:[w]}
        """

        c_full = Counter(C)

        c_words = {i:[] for i in c_full.keys()}

        for i in range(len(C)):
            c_words[C[i]].append(D[i])

        # @deprecated
        # for k, v in c_words.iteritems():
        for k, v in c_words.items():
            c_words[k] = self.flatten(v)

        return c_words, c_full


    def loglikelihood(self, D, C):

        c_words, c_full = self.cwords(D, C)

        # num of words in each class
        # @deprecated
        # c_count = {k:len(v) for k, v in c_words.iteritems()} 
        c_count = {k:len(v) for k, v in c_words.items()} 

        # each word counts in each class
        c_part = {c:Counter(c_words[c]) for c in c_full.keys()}

        # log likelihood
        len_V = len(self._V)

        self._loglikelihood = {c:{} for c in c_full.keys()}

        # for c, cnt in c_part.iteritems():
        # @deprecated
        for c, cnt in c_part.items():
            denominator = np.log2(c_count[c] + len_V)

            c_part_count = c_part[c]
            
            for w in c_part[c].keys():
                self._loglikelihood[c][w] = np.log2(c_part_count.get(w,0)+1.) - denominator

            for w in set(self._V)-set(c_part_count.keys()):
                self._loglikelihood[c][w] = -denominator



    def likelihood(self):

        # @deprecated
        # return np.sum([v.values() for v in self._loglikelihood.values()])
        return np.sum([list(v.values()) for v in self._loglikelihood.values()])



    def cunique(self, C):

        self._C = np.unique(C)


    def fit(self, D, C):

        self.logprior(C)
        self.V(D)
        self.loglikelihood(D, C)
        self.cunique(C)


    def predict(self, D):

        score = [[self._logprior.get(c,0) + sum([self._loglikelihood[c].get(w,0) for w in d]) for c in self._C] for d in D]
        idx   = np.argmax(score, axis=1)
        c     = self._C[idx].tolist()

        return c


    def save(self, fn):

        with open(fn, 'wb') as f:
            pickle.dump(self.__dict__, f)


    def load(self, fn):

        with open(fn, 'rb') as f:
            self.__dict__.update(pickle.load(f))
