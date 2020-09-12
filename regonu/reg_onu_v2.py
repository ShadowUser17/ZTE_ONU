#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from traceback import print_exc
from jinja2 import Template
from argparse import ArgumentParser


onu_types = {'1':'1ETH', '4':'4ETH'}
args = ArgumentParser()

args.add_argument('onu_iface', help='Example: 1/2/5:1')
args.add_argument('onu_sn', help='Example: ZTEGXXXXXXXX')

args.add_argument('-t', dest='onu_type', default='1', help='ONU type: 1/4')
args.add_argument('-m', dest='onu_mode', default='a', help='ONU type: a/h/t')
args.add_argument('-d', dest='onu_desc', default='-', help='ONU description.')
args.add_argument('-p', dest='onu_pvid', default='', help='Pvid for access/hybrid mode.')
args.add_argument('-v', dest='onu_tags', default='', help='Vlans for hybrid/trunk mode.')


try:
    args = args.parse_args()
    (olt_iface, onu_id) = args.onu_iface.split(':')

    onu_vlans = None
    if args.onu_mode == 'a':
        onu_vlans = args.onu_pvid

    elif args.onu_mode == 't':
        onu_vlans = args.onu_tags

    elif args.onu_mode == 'h':
        if not args.onu_tags:
            onu_vlans = args.onu_pvid

        elif args.onu_pvid:
            onu_vlans = (args.onu_pvid + ',' + args.onu_tags) 

    with open('zte_onu.jn2') as fd:
        template = Template(fd.read())

        print(template.render(
            olt_iface=olt_iface,
            onu_id=onu_id,
            onu_type=onu_types[args.onu_type],
            onu_sn=args.onu_sn,
            onu_iface=args.onu_iface,
            onu_desc=args.onu_desc,
            onu_mode=args.onu_mode,
            onu_pvid=args.onu_pvid,
            onu_vlans=onu_vlans,
            onu_tags=args.onu_tags
        ))

except Exception:
    print_exc()
