#!/usr/bin/env python3
from traceback import print_exc
from collections import OrderedDict
from re import compile as re_compile
from sys import stdout
#
#
class ParseZTE:
    _parser_olt = re_compile('interface gpon-olt_(\d+/\d+/\d+)')
    _parser_onu = re_compile('interface gpon-onu_(\d+/\d+/\d+:\d+)')
    _parser_mng = re_compile('pon-onu-mng gpon-onu_(\d+/\d+/\d+:\d+)')
    #
    def __init__(self):
        self._raw = ''
        self._olt = ''
        self._onu = ''
        self._mng = ''
    #
    def load_from_file(self, fname):
        with open(fname) as fd:
            tmp = fd.read()
            tmp = map(str.lstrip, tmp.split('!'))
            self._raw = list(map(str.rstrip, tmp))
    #
    def _parser(self, regex):
        raw = iter(self._raw)
        data = OrderedDict()
        #
        for item in raw:
            iface = regex.findall(item)
            #
            if iface:
                item = map(str.split, item.split('\n'))
                item = list(map(list, item))
                data[iface[0]] = item
        #
        return data
    #
    def parse(self):
        self._olt = self._parser(self._parser_olt)
        self._onu = self._parser(self._parser_onu)
        self._mng = self._parser(self._parser_mng)
        self._raw = ''
    #
    @classmethod
    def print(self, obj, fd=stdout):
        obj = '\n'.join(map(' '.join, obj))
        print(obj + '\n!', file=fd)
    #
    @property
    def cfg_olt(self): return self._olt
    #
    @property
    def cfg_onu(self): return self._onu
    #
    @property
    def cfg_mng(self): return self._mng

