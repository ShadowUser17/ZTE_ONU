#-*- coding: utf-8 -*-
from telnetlib import Telnet
from time import sleep
from cgi import escape
#
from snmp import show_except
from cfg_data import zte_host
from cfg_data import zte_port
from cfg_data import zte_user
from cfg_data import zte_pass
#
def_header = '''\
Status: 200 OK
Content-Type: text/html
'''
#
rdr_header = '''\
Status: 302 Moved
Location: /
'''
#
#
def telnet_exec(host, cmds, timeout=2):
    try:
        telnet = Telnet()
        host, port = host
        #telnet.debuglevel = 1
        telnet.open(host, port)
        #
        for item in cmds:
            telnet.write(item.encode() + b'\x0d\x0a')
            sleep(timeout)
            #
        else: telnet.close()
        #
    except Exception as msg: print show_except(msg)
#
#
def onu_add(olt_num, onu_num, onu_sn, vlan, onu_type='1ETH', desc='', save='', host = (zte_host, zte_port), user = zte_user, passwd = zte_pass):
    '''host = (ip, port),
olt_num = rack/slot/port,
onu_num = 1-128,
onu_type = 1/4ETH'''
    cmd_onu = [
        user, passwd,
        'configure terminal',
        #############################
        'interface gpon-olt_{0}'.format(olt_num),
        'onu {0} type {1} sn {2}'.format(onu_num, onu_type, onu_sn),
        'exit',
        #############################
        'interface gpon-onu_{0}:{1}'.format(olt_num, onu_num),
        'sn-bind enable sn',
        'description {0}'.format(desc),
        'tcont 1 name unlim profile unlim',
        'gemport 1 name unlim tcont 1',
        'service-port 1 vport 1 user-vlan {0} vlan {0}'.format(vlan),
        'exit',
        #############################
        'pon-onu-mng gpon-onu_{0}:{1}'.format(olt_num, onu_num),
        'gemport 1 flow 1'
    ]
    # Type: 1ETH
    cmd_onu.append('vlan port eth_0/1 mode tag vlan {0}'.format(vlan))
    #
    # Type: 4ETH
    if onu_type == '4ETH':
        for item in range(2, 5):
            cmd_onu.append('vlan port eth_0/{0} mode tag vlan {1}'.format(item, vlan))
    #
    cmd_onu.append('end')
    if save: cmd_onu.append('write')
    #
    telnet_exec(host, cmd_onu)
#
#
def onu_del(olt_num, onu_num, save='', host = (zte_host, zte_port), user = zte_user, passwd = zte_pass):
    '''host = (ip, port),
olt_num = rack/slot/port,
onu_num = 1-128,
onu_type = 1/4ETH'''
    cmd_onu = [
        user, passwd,
        'configure terminal',
        #############################
        'interface gpon-olt_{0}'.format(olt_num),
        'no onu {0}'.format(onu_num),
        'end'
    ]
    #
    if save: cmd_onu.append('write')
    telnet_exec(host, cmd_onu)
#
#
def by_onu_add(form):
    try:
        onu_str = escape(form.getvalue('onu_string', ''))
        olt_iface, onu_sn = onu_str.split(':')
        #
        onu_num = escape(form.getvalue('onu_num', ''))
        onu_type = escape(form.getvalue('onu_type', ''))
        vlan = escape(form.getvalue('vlan', ''))
        desc = escape(form.getvalue('desc', 'None'))
        save = escape(form.getvalue('save_conf', ''))
        #
        onu_add(olt_iface, onu_num, onu_sn, vlan, onu_type, desc, save)
        #
    except Exception as msg: show_except(msg)
#
#
def by_onu_del(form):
    try:
        olt_iface = escape(form.getvalue('olt_iface', ''))
        onu_num = escape(form.getvalue('onu_num', ''))
        save = escape(form.getvalue('save_conf', ''))
        #
        onu_del(olt_iface, onu_num, save)
        #
    except Exception as msg: show_except(msg)
