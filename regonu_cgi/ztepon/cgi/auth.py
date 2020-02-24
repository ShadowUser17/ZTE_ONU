#-*- coding: utf-8 -*-
from cgi import escape
from cfg_data import users
from cfg_data import zte_host
from cfg_data import snmp_community
from cfg_data import snmp_port
#
from snmp import get_gpon_ifaces
from snmp import show_unreg_gpon_onus
#
#
def check_access(form):
    login = escape(form.getvalue('login', ''))
    passwd = escape(form.getvalue('passwd', ''))
    #
    db_pass = users.get(login, '')
    if passwd == db_pass: return True
    else: return False
#
#
def show_menu():
    # Form1 (Append ONU)
    print '''<html>
<head><meta charset="UTF-8"><title>Manage: {}</title></head>
<body><br><br><table align="center"><tr><td><fieldset>
<legend>Append ONU</legend>
<form action="/cgi/handler.py" method="POST">
<input type="hidden" name="form_id" value="onu_add">
<table>'''.format(zte_host)
    ########################
    # Unregistered ONUs:
    onus = show_unreg_gpon_onus(zte_host, snmp_community, snmp_port)
    if onus:
        print '''<tr><td>Select ONU: </td>
<td><select name="onu_string">'''
        #
        for item in onus:
            iface, _, onu_sn = item
            print '\t<option value="{iface}:{onu_sn}">P:{iface} ({onu_sn})</option>'.format(iface=iface, onu_sn=onu_sn)
            #
    else:
        print '''<tr><td>ONU String: </td>
<td><input type="text" name="onu_string" required>'''
    ########################
    print '''</select></td></tr>
<tr><td>ONU Number: </td>
<td><input type="text" name="onu_num" required></td></tr>
<tr><td>ONU Type: </td>
<td><select name="onu_type">
    <option value="1ETH">Port: 1</option>
    <option value="4ETH">Port: 4</option>
</select></td></tr>
<tr><td>Vlan ID: </td>
<td><input type="text" name="vlan" required></td></tr>
<tr><td>Description: </td>
<td><input type="text" name="desc"></td></tr>
<tr><td>Save and Submit: </td>
<td><input type="checkbox" name="save_conf" value="off">
<input type="submit" value="Submit"></td></tr>
</table></form></fieldset></td></tr>'''
    #
    # Form2 (Delete ONU)
    print '''</table>
<br><br><table align="center"><tr><td><fieldset>
<legend>Delete ONU</legend>
<form action="/cgi/handler.py" method="POST">
<input type="hidden" name="form_id" value="onu_del"><table>'''
    ########################
    # GPON Interface
    print '<tr><td>GPON Interface:</td>'
    gpon = get_gpon_ifaces(zte_host, snmp_community, snmp_port)
    if gpon:
        print '<td><select name="olt_iface">'
        for item in gpon: print '\t<option value="{0}">{0}</option>'.format(item)
        print '</select></td></tr>'
        #
    else: print '<td><input type="text" name="olt_iface" required></td></tr>'
    ########################
    # ONU Number
    print '''<tr><td>ONU Number:</td>
<td><input type="text" name="onu_num" required></td></tr>'''
    ########################
    # Save and submit
    print '''<tr align="left"><td>Save and submit:</td><td>
<input type="checkbox" name="save_conf">
<input type="submit" value="Submit">
</td></tr></table></form></fieldset></td></tr>
</table></body></html>'''
