#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from cgi import FieldStorage
#
import auth
import menu
#
#
form = FieldStorage()
#
try:
    if form.getvalue('form_id', '') == 'auth':
        if auth.check_access(form):
            print menu.def_header
            auth.show_menu()
            #
        else: print menu.rdr_header
        #
    elif form.getvalue('form_id', '') == 'onu_add':
        print menu.def_header
        menu.by_onu_add(form)
        auth.show_menu()
        #
    elif form.getvalue('form_id', '') == 'onu_del':
        print menu.def_header
        menu.by_onu_del(form)
        auth.show_menu()
        #
    else: print menu.rdr_header
    #
except Exception as msg: menu.show_except(msg)
