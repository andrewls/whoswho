# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import nose
from nose.tools import *
import unittest

from whoswho import who, config

from nameparser.config.titles import TITLES as NAMEPARSER_TITLES
from nameparser.config.suffixes import SUFFIXES as NAMEPARSER_SUFFIXES


class TestFullNames(unittest.TestCase):

    def setUp(self):
        self.name = 'Robert Evan Liebowitz'

    def test_string(self):
        # Only relevant for python 2.X
        assert_true(who.match(self.name, str('Robert Liebowitz')))

    def test_unicode(self):
        name = self.name
        assert_true(who.match(name, 'attaché Robert Evan Liebowitz'))
        assert_true(who.match(name, 'Rōbért Èvān Lîęböwitz'))
        assert_false(who.match(name, 'Rōbért Èvān Lęîböwitz'))

    def test_name_and_initials(self):
        assert_true(who.match(self.name, 'R. Evan Liebowitz'))
        assert_true(who.match(self.name, 'Robert E. Liebowitz'))
        assert_true(who.match(self.name, 'R. E. Liebowitz'))

    def test_different_number_initials(self):
        assert_true(who.match(self.name, 'Robert Liebowitz'))
        assert_true(who.match(self.name, 'R. Liebowitz'))
        assert_false(who.match(self.name, 'Robert E. E. Liebowitz'))
        assert_false(who.match(self.name, 'R. E. E. Liebowitz'))
        assert_true(who.match('R.E.E. Liebowitz', 'R. E. E. Liebowitz'))

    def test_different_initials(self):
        assert_false(who.match(self.name, 'E. R. Liebowitz'))
        assert_false(who.match(self.name, 'E. Liebowitz'))
        assert_false(who.match(self.name, 'R. V. Liebowitz'))
        assert_false(who.match(self.name, 'O. E. Liebowitz'))

    def test_short_names(self):
        assert_true(who.match(self.name, 'Rob Liebowitz'))
        # TODO: Should these be true?
        assert_false(who.match(self.name, 'Bert Liebowitz'))
        assert_false(who.match(self.name, 'Robbie Liebowitz'))

    def test_suffixes(self):
        name = 'Robert Liebowitz Jr'
        assert_true(who.match(name, 'Robert Liebowitz'))
        assert_true(who.match(name, 'Robert Liebowitz Jr'))
        assert_true(who.match(name, 'Robert Liebowitz, PhD'))
        assert_false(who.match(name, 'Robert Liebowitz, Sr'))
        assert_false(who.match(name, 'Robert Liebowitz, Sr, PhD'))
        assert_true(who.match(name, 'Robert Liebowitz, Jr, PhD'))

    def test_equivalent_suffixes(self):
        name = 'Robert Liebowitz Jr'
        assert_true(who.match(name, 'Robert Liebowitz Jnr'))
        assert_false(who.match(name, 'Robert Liebowitz Snr'))

    def test_titles(self):
        name = 'Mr. Robert Liebowitz'
        assert_true(who.match(name, 'Robert Liebowitz'))
        assert_true(who.match(name, 'Sir Robert Liebowitz'))
        assert_true(who.match(name, 'Dr. Robert Liebowitz'))
        assert_false(who.match(name, 'Mrs. Robert Liebowitz'))


class TestConfig(unittest.TestCase):

    def test_titles_all_defined(self):
        """
        Check if list of titles is up to date with nameparser
        """
        all_titles = (
            config.MALE_TITLES |
            config.FEMALE_TITLES |
            config.GENDERLESS_TITLES
        )
        assert_equal(all_titles, NAMEPARSER_TITLES)

    def test_suffixes_all_defined(self):
        """
        Check if list of suffixes is up to date with nameparser
        """
        all_suffixes = (
            config.UNIQUE_SUFFIXES |
            config.MISC_SUFFIXES
        )
        assert_equal(all_suffixes, NAMEPARSER_SUFFIXES)


if __name__ == '__main__':
    nose.main()