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
    def _loader(self, raw):
        raw = map(str.lstrip, raw.split('!'))
        self._raw = list(map(str.rstrip, raw))
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
    def parse_cfg(self):
        self._olt = self._parser(self._parser_olt)
        self._onu = self._parser(self._parser_onu)
        self._mng = self._parser(self._parser_mng)
        self._raw = ''
    #
    def load_from_string(self, raw): self._loader(raw)
    #
    def load_from_file(self, fname):
        with open(fname) as fd: self._loader(fd.read())
    #
    def find_from_sn(self, sn):
        onus = []
        #
        for olt in self._olt.keys():
            onu = list(filter(lambda item: item[-1] == sn, self._olt[olt]))
            if onu: onus.append((olt, onu[0]))
        #
        return onus
    #
    def get_by_sn(self, sn):
        onus = self.find_from_sn(sn)
        #
        items = []
        for (olt, onu) in onus:
            olt_port = olt
            onu_port = '{}:{}'.format(olt_port, onu[1])
            #
            olt = [self._olt[olt][0], onu]
            onu = self._onu[onu_port]
            mng = self._mng[onu_port]
            #
            items.append((olt, onu, mng))
        #
        return items
    #
    #@classmethod
    #def replace_port(self, old, new, obj): pass
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

