#-*- coding: utf-8 -*-
from subprocess import Popen
from subprocess import PIPE
# Show error messages.
__DBG__ = False
#
#
def show_except(obj_except):
    print '<br>{}: {}: {}'.format(
        __name__, obj_except.__class__.__name__,
        obj_except.message)
#
#
def snmpwalk(host, community, mib, port=161):
    'snmpwalk(host, community, mib, port=161) -> []'
    cmd = 'snmpwalk -v 2c -On -c \'{0}\' \'{1}:{2}\' \'{3}\''
    cmd = cmd.format(community, host, port, mib)
    cmd_exec = Popen(cmd, shell=True, stdout=PIPE)
    cmd_exec.wait()
    res = cmd_exec.communicate()
    #
    res = res[0].rstrip('\n')
    res = res.split('\n')
    return res
#
#
def hex_to_string(string):
    corp_id = string[:8]
    part_id = string[8:]
    string = corp_id.decode('hex') + part_id
    #
    return string
#
#
def get_gpon_ifaces(host, community, port):
    try:
        res = snmpwalk(host, community, '.1.3.6.1.2.1.2.2.1.2', port)
        gpon = []
        #
        for item in res:
            item = item.split()
            item = item[-1]
            if item.startswith('gpon'):
                item = item.split('_')
                gpon.append(item[-1])
        #
        return gpon
    #
    except Exception as msg:
        if __DBG__: show_except(msg)
#
#
def get_gpon_unreg_sn(host, community, port):
    try:
        res = snmpwalk(host, community, '.1.3.6.1.4.1.3902.1012.3.13.3.1.2', port)
        sns = []
        for item in res:
            item = item.split()
            item = item[3:]
            sns.append(''.join(item))
        #
        sns = map(hex_to_string, sns)
        return sns
    #
    except Exception as msg:
        if __DBG__: show_except(msg)
#
#
def get_gpon_unreg_onu(host, community, port):
    try:
        res = snmpwalk(host, community, '.1.3.6.1.4.1.3902.1012.3.13.1.1.14', port)
        onus = []
        #
        for item in res:
            item = item.split()
            item = int(item[-1])
            onus.append(item)
        #
        if sum(onus): return onus
    #
    except Exception as msg:
        if __DBG__: show_except(msg)
#
#
def show_unreg_gpon_onus(host, community, port):
    onu_counts = get_gpon_unreg_onu(host, community, port)
    if not onu_counts: return None
    #
    onu_sn = get_gpon_unreg_sn(host, community, port)
    if not onu_sn: return None
    onu_sn.reverse()
    #
    ports = get_gpon_ifaces(host, community, port)
    if not ports: return None
    ports.reverse()
    #
    items = []
    for onu in onu_counts:
        port = ports.pop()
        #
        if onu:
            for it in range(1, onu + 1):
                sn = onu_sn.pop()
                items.append((port, it, sn))
    #
    return items
