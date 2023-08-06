# -*- coding: utf-8 -*-

# regtest
# -------
# regression test enhancement for the Python unittest framework.
# 
# Author:   sonntagsgesicht
# Version:  0.1, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/regtest
# License:  Apache License 2.0 (see LICENSE file)


from inspect import stack
from json import load, dump
from logging import getLogger, NullHandler
from os.path import exists, sep
from os import remove, mkdir
from unittest import TestCase

logger = getLogger('regtest')
logger.addHandler(NullHandler())

# Allows isinstance(foo, basestring) to work in Python 3
try:
    basestring
except NameError:
    basestring = str


class _ignore_(object):
    pass


class MissingAssertValueError(KeyError):
    pass


class LeftoverAssertValueError(KeyError):
    pass


class RegressionTestCase(TestCase):
    _folder_per_class = True

    @property
    def foldername(self):
        if self.__class__._folder_per_class:
            return self._data_foldername + sep + self._testcase_foldername
        else:
            return self._data_foldername

    @property
    def filenames(self):
        return list(self.full_filename(m) for m in self.testmethodnames)

    @property
    def testmethodnames(self):
        return list(m for m in dir(self) if m.startswith('test'))

    def full_filename(self, filename):
        if self.__class__._folder_per_class:
            return self.foldername + sep + str(filename) + self._file_extenstion
        else:
            return self.foldername + sep + self._testcase_foldername + '.' + str(filename) + self._file_extenstion

    def __init__(self, *args, **kwargs):
        super(RegressionTestCase, self).__init__(*args, **kwargs)
        self._last_results = dict()
        self._new_results = dict()
        self._data_foldername = '.'
        self._testcase_foldername = self.__class__.__name__
        self._file_extenstion = '.json'
        self._prudent = True

    def bePrudent(self, be=True):
        """ better log error than raise it """
        self._prudent = be

    def clearResults(self):
        """ remove all test data files in test case folder """
        for file_name in self.filenames:
            if exists(file_name):
                remove(file_name)

    def setUp(self):
        self.readResults()

    def tearDown(self):
        self.writeResults()

    def setFileName(self, filename):
        self._testcase_foldername = filename

    def setFolderName(self, foldername):
        self._data_foldername = foldername

    def readResults(self):
        logger.debug('read from %s' % self.foldername)
        for test_method in self.testmethodnames:
            file_name = self.full_filename(test_method)
            if exists(file_name):
                with open(file_name) as data_file:
                    self._last_results[test_method] = load(data_file)

    def writeResults(self):
        logger.debug('write to %s' % self.foldername)

        # validate all values have been used
        for key in self._new_results:
            leftover = self._last_results.get(key)
            if leftover:
                args = self.__class__.__name__, key, repr(leftover)
                msg = 'requested less values than available for %s.%s: %s' % args
                if self._prudent:
                    raise LeftoverAssertValueError(msg)
                else:
                    logger.warning(msg)
                    self._last_results.pop(key)

        # write new results
        if not exists(self.foldername):
            mkdir(self.foldername)

        for k, v in list(self._new_results.items()):
            file_name = self.full_filename(k)
            with open(file_name, 'w') as data_file:
                dump(v, data_file, indent=2)

    def logResults(self, filename=None, foldername=None):
        if filename is None:
            filename = self.__class__.__name__ + '.log'
        if foldername is None:
            foldername = self._data_foldername
        filename = foldername + sep + filename
        if not filename is not self.foldername:
            raise ValueError("file %s not found in folder %s." % (filename, self.foldername))
        logger.debug('log to %s' % filename)

        last_results = dict()
        if exists(filename):
            with open(filename) as data_file:
                last_results = load(data_file)

        for k, v in list(self._new_results.items()):
            if k not in last_results:
                last_results[k] = v

        with open(filename, 'w') as data_file:
            dump(last_results, data_file, indent=2)

    def assertAlmostRegressiveEqual(self, new, places=7, msg=None, delta=None, key=()):
        self._write_new(new, key)
        last = self._read_last(key)
        if last is not _ignore_:
            self._log_assert_call(last, new, places, msg, delta)
            return super(RegressionTestCase, self).assertAlmostEqual(last, new, places, msg, delta)

    def assertRegressiveEqual(self, new, msg=None, key=()):
        self._write_new(new, key)
        last = self._read_last(key)
        if last is not _ignore_:
            self._log_assert_call(last, new, msg)
            return super(RegressionTestCase, self).assertEqual(last, new, msg)

    def _log_assert_call(self, *args, **kwargs):
        test_method = self.__class__.__name__ + '.' + RegressionTestCase._gather_method('test')
        assert_method = RegressionTestCase._gather_method('assert')
        pp = lambda k, v: '%s: %s' % (str(k), repr(v))
        kwargs = tuple(map(pp, kwargs))
        args = ', '.join(map(repr, args + kwargs))
        logger.info('%s %s(%s)' % (test_method.ljust(20), assert_method, args))

    @staticmethod
    def _gather_method(name):
        m = None
        for line in reversed(stack()):
            if line[3].lower().startswith(name.lower()):
                m = line[3]
        if m is None:
            raise KeyError
        return m

    def _get_testmethod(self):
        return self._gather_method('test')

    def _read_last(self, key=()):
        testmethod = self._get_testmethod()
        key = key if key else testmethod
        if testmethod in self._last_results:
            if key in self._last_results[testmethod]:
                if self._last_results[testmethod][key]:
                    last = self._last_results[testmethod][key].pop(0)
                    if isinstance(last, basestring):
                        last = str(last)  # .encode('ascii', 'ignore')  # 2to3 20190916
                    return last
            msg = 'requested more values than available for %s.%s.%s' % (self.__class__.__name__, testmethod, key)
            if self._prudent:
                raise MissingAssertValueError(msg)
            else:
                logger.warning(msg)
                self._last_results.pop(key)
        return _ignore_

    def _write_new(self, new, key=()):
        testmethod = self._get_testmethod()
        key = key if key else testmethod
        if testmethod not in self._new_results:
            self._new_results[testmethod] = dict()
        if key not in self._new_results[testmethod]:
            self._new_results[testmethod][key] = list()
        self._new_results[testmethod][key].append(new)
