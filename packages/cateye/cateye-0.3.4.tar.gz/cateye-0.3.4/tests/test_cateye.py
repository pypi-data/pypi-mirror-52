#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_cateye
----------------------------------

Tests for `cateye` module.
"""

import unittest

from cateye import cateye

class TestCateye(unittest.TestCase):

    def setUp(self):
        pass

    def test_gen_path(self):
        base = 'test/path'
        code = 'ABC3'
        wanted = 'test/path'
        result = cateye.gen_path(base, code)
        self.assertEqual(wanted, result)

    def test_clean(self):
        s = 'Open wound to auricle of ear, without mention of complication'
        wanted = 'Open wound to auricle of ear, '
        result = cateye.clean(s)
        self.assertEqual(wanted, result)
        s = 'Diabetes mellitus without mention of complication, Type I'
        wanted = 'Diabetes mellitus  Type I'

    def test_tokenize(self):
        s = "Crohn's disease 克隆氏症"
        wanted = ['Crohn', 'disease', '克隆氏症']
        result = cateye.tokenize(s)
        self.assertEqual(wanted, result)

    def test_lemmatize(self):
        tokens = ['Best', 'TEST', 'case']
        wanted= ['best', 'test', 'case']
        result = cateye.lemmatize(tokens)
        self.assertEqual(wanted, result)

    def test_filterout(self):
        tokens = ['for', 'test', 'only']
        stopwords = ['for']
        wanted = ['test', 'only']
        result = cateye.filterout(tokens, stopwords)
        self.assertEqual(wanted, result)

    def test_ed1(self):
        token = 'abc'
        wanted = {'aabc', 'abbc', 'acbc', 'adbc', 'aebc',
                  'abca', 'abcb', 'abcc', 'abcd',
                  'ab', 'ac',
                  'aac', 'acc', 'adc', 'aec', 'afc', 'agc',
                  'acb'}
        result = cateye._ed1(token)
        self.assertTrue(wanted <= result)

    def tearDown(self):
        pass
