# Copyright (C) 2018 Semicon Networks
# Author: Hans Roh <hansroh@gmail.com>

import os
import sys
import subprocess
from getpass import getpass
from hashlib import md5
import os, struct
from rs4.termcolor import tc
from rs4 import ifaces

ENCRYPTED = None
LICENSE_FILE = None
POSITION = 0

def confugure (key, name = '.license'):
    global ENCRYPTED, LICENSE_FILE, POSITION
    ENCRYPTED = md5 (key.encode ()).hexdigest ()
    POSITION = (sum ([ord (c) for c in ENCRYPTED]) * 1978524790) % 1008
    LICENSE_FILE = os.path.join (os.path.dirname (os.path.join (os.getcwd (), sys.argv [0])), name)

def check_license (logger):
    global ENCRYPTED, LICENSE_FILE
    assert ENCRYPTED and LICENSE_FILE, 'call license.configure first'

    if not os.path.isfile (LICENSE_FILE):
        logger ("cannot find license", 'warn')
        return False
    try:
        hwid = ifaces.get_hwid ().lower ()
    except subprocess.CalledProcessError:
        logger ("cannot get hardware ID, maybe run wiht root permission", "warn")
        return False
    key = md5 ('{}:{}'.format (ENCRYPTED, hwid).encode ()).digest ()
    with open (LICENSE_FILE, 'rb') as f:
        data = f.read ()        
    s = sum (struct.unpack ('BBB', data [:3])) + 3 + POSITION
    if data [s:s + 16] != key:
        logger ("invalid license", "error")
        return False
    return True    

def create_license (logger, uuid = None):
    global ENCRYPTED, LICENSE_FILE
    assert ENCRYPTED and LICENSE_FILE, 'call license.configure first'

    if os.path.isfile (LICENSE_FILE):
        with open (LICENSE_FILE, 'rb') as f:
            data = f.read ()
        lns = struct.unpack ('BBB', data [:3])
        data = data [3:]
        name = data [:lns [0]].decode (); data = data [lns [0]:]
        org = data [:lns [1]].decode (); data = data [lns [1]:]
        contact = data [:lns [2]].decode (); data = data [lns [2]:]

        print (tc.info ("\nLicense Information\n"))
        print (tc.echo ("  Organization:"), org)
        print (tc.echo ("  Name:"), name)
        print (tc.echo ("  Contact:"), contact)
        print (tc.echo ("  License Status:"), check_license (logger) and 'valid' or 'invalid')        

        if input ('\nDo you want replace license? (n/y) ') != 'y':
            sys.exit ()

    print ()
    org, name, contact = None, None, None
    while not org:
        org = input ('Enter organization Name: ')
        if len (org.encode ()) > 64:
            print ('  too long, should be within 64 bytes')
            org = None
    while not name:
        name = input ('Enter name of person in charge: ')
        if len (name.encode ()) > 64:
            print ('  too long, should be within 64 bytes')
            name = None
    while not contact:
        contact = input ('Enter contact number: ')
        if len (contact.encode ()) > 32:
            print ('  too long, should be within 32 bytes')
            contact = None
            
    name = name.encode ()
    org = org.encode ()
    contact = contact.encode ()

    premble = struct.pack ('B', len (name)) + struct.pack ('B', len (org)) + struct.pack ('B', len (contact)) + name + org + contact
    password = getpass('Enter key for creating license: ')
    if md5 (password.encode ()).hexdigest () != ENCRYPTED:
        return "incorrect key"
    try:
        hwid = uuid or ifaces.get_hwid ()
        hwid = hwid.lower ()
    except subprocess.CalledProcessError:
        return "cannot get hardware ID, maybe run wiht root permission"
    key = md5 ('{}:{}'.format (ENCRYPTED, hwid).encode ()).digest ()
    data = premble + os.urandom (POSITION) + key + os.urandom (1024 - 16 - POSITION)    
    with open (LICENSE_FILE, 'wb') as f:
        f.write (data)
    os.chmod (LICENSE_FILE, 0o644)
