#!/usr/bin/python3
# -*- coding:utf-8
"""
Akamai NetStorage API for Python
@author:vitaly.zuevsky@gmail.com
"""

import os
import hmac
import base64
import hashlib
import requests
from time import time
from pathlib import posixpath
from urllib.parse import quote
from secrets import token_urlsafe
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

class Client:
    
    def __init__(self, **kwargs):
        
        self.read_timeout = kwargs['read_timeout'] if 'read_timeout' in kwargs else 9
        self.conn_timeout = kwargs['conn_timeout'] if 'conn_timeout' in kwargs else 6
        self.retry_number = kwargs['retry_number'] if 'retry_number' in kwargs else 3
        
        self.url_safe_chars = kwargs['url_safe_chars'] if 'url_safe_chars' in kwargs else '/~'
    
    def _req(self, *args, **kwargs):
        
        timeout = (self.conn_timeout, self.read_timeout)
        
        err = None
        for _ in range(self.retry_number):
            try:
                return requests.request(*args, **kwargs, timeout=timeout)
                
            except Exception as e: err = e
            
        raise err

    def download(self, arl, key, keyname, saveto):
        
        # arl e.g. akamai://example-nsu.akamaihd.net/395007/my/path/special.log
        # saveto is an existing folder or a file target
    
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        path = quote(path, safe=self.url_safe_chars)
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        ha = "version=1&action=download"
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2}
        
        r = self._req('GET', url, headers=headers)
        
        if r.status_code == 200:
            
            saveto = os.path.normpath(os.path.expanduser(saveto))
            
            if os.path.isdir(saveto): saveto += os.sep + arl.split('/')[-1]
            
            with open(saveto, 'wb') as f: f.write(r.content)
            
        return r

    def upload(self, arl, key, keyname, file):
        
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        path = quote(path, safe=self.url_safe_chars)
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        ha = "version=1&action=upload"
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        file = os.path.expanduser(file)
        with open(file, 'rb') as f: data = f.read()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2,
                'Content-Length': str(len(data))}
        
        return self._req('PUT', url, headers=headers, data=data)

    def delete(self, arl, key, keyname):
        
        # no trailing slash for symlinks
        
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        path = quote(path, safe=self.url_safe_chars)
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        ha = "version=1&action=delete"
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2,
                'Content-Length': '0'}
        
        return self._req('PUT', url, headers=headers)

    def xdir(self, arl, key, keyname):
        
        # returns xml string in r.text, arl is a folder with or without trailing slash
        # e.g. akamai://example-nsu.akamaihd.net/395007/my/path/
    
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        path = quote(path, safe=self.url_safe_chars)
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        ha = "version=1&action=dir&format=xml"
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2}
        
        return self._req('GET', url, headers=headers)

    def xdu(self, arl, key, keyname):
        
        # returns xml string in r.text, arl is a folder with or without trailing slash
        # e.g. akamai://example-nsu.akamaihd.net/395007/my/path/
    
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        path = quote(path, safe=self.url_safe_chars)
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        ha = "version=1&action=du&format=xml"
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2}
        
        return self._req('GET', url, headers=headers)

    def mkdir(self, arl, key, keyname):
        
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        path = quote(path, safe=self.url_safe_chars)
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        ha = "version=1&action=mkdir"
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2,
                'Content-Length': '0'}
        
        return self._req('PUT', url, headers=headers)

    def mtime(self, arl, key, keyname, epoch):
        
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        path = quote(path, safe=self.url_safe_chars)
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        ha = "version=1&action=mtime&mtime=" + str(epoch)
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2,
                'Content-Length': '0'}
        
        return self._req('PUT', url, headers=headers)

    def quickdelete(self, arl, key, keyname):
        
        # Recursive folder remover - disabled in NetStorage by default
        
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        path = quote(path, safe=self.url_safe_chars)
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        ha = "version=1&action=quick-delete&quick-delete=imreallyreallysure"
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2,
                'Content-Length': '0'}
        
        return self._req('PUT', url, headers=headers)

    def rename(self, arl, key, keyname, uri):
        
        # all path folders must exist, moves under same CP code only
        # uri e.g. "/395007/mypath/dir-v-test/vtest2"
        # uri e.g. "../vtest" (relative to arl)
        
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        if not posixpath.commonprefix([path, uri]):
            
            p = path[:-1] if path.endswith('/') else path
            uri = posixpath.split(p)[0] + '/' + uri
            uri = posixpath.normpath(uri)
        
        path = quote(path, safe=self.url_safe_chars)
        
        ha = "version=1&action=rename&destination=" + quote_plus(uri)
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2,
                'Content-Length': '0'}
        
        return self._req('PUT', url, headers=headers)

    def rmdir(self, arl, key, keyname):
        
        # arl is a folder with or without trailing slash
        # e.g. akamai://example-nsu.akamaihd.net/395007/my/path/dir-v-test
        
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        path = quote(path, safe=self.url_safe_chars)
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        ha = "version=1&action=rmdir"
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2,
                'Content-Length': '0'}
        
        return self._req('PUT', url, headers=headers)

    def rmdir_rec(self, arl, key, keyname):
        
        # arl is a folder with or without trailing slash
        # e.g. akamai://example-nsu.akamaihd.net/395007/my/path/dir-v-test
        # Only recursive function here with many HTTP calls. May crash on stack overflow
        
        r = self.xdir(arl, key, keyname)
        if r.status_code != 200: return r
        
        xml = ET.fromstring(r.text)
        
        p = arl if arl.endswith('/') else arl + '/'
        
        for entry in xml:
            
            entry_arl = p + entry.attrib['name']
            
            if entry.attrib['type'] == 'dir':
                
                r = self.rmdir_rec(entry_arl, key, keyname)
            else:
                r = self.delete(entry_arl, key, keyname)
            
            if r.status_code != 200 and r.status_code != 404: return r
        
        return self.rmdir(arl, key, keyname)

    def stat(self, arl, key, keyname):
        
        # returns xml string in r.text, arl is a file, symlink or a folder with or without trailing slash
        # e.g. akamai://example-nsu.akamaihd.net/395007/my/path/
    
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        path = quote(path, safe=self.url_safe_chars)
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        ha = "version=1&action=stat&format=xml"
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2}
        
        return self._req('GET', url, headers=headers)

    def symlink(self, arl, key, keyname, target):
        
        # target e.g. "/395007/my/path/dir-v-test/vtest2"
        # target e.g. "../vtest/" (relative to arl)
        
        if arl.startswith("akamai://"): arl = arl[len("akamai://"):]
        
        host = arl.split('/')[0]
        path = arl[len(host):]
        
        serial = token_urlsafe(8)
        
        utc = str(round(time()))
        
        if not posixpath.commonprefix([path, target]):
            
            p = path[:-1] if path.endswith('/') else path
            target = posixpath.split(p)[0] + '/' + target
            target = posixpath.normpath(target)
        
        path = quote(path, safe=self.url_safe_chars)
        
        ha = "version=1&action=symlink&target=" + quote_plus(target)
        h1 = "5, 0.0.0.0, 0.0.0.0, " + utc + ", " + serial + ", " + keyname
        
        msg = h1 + path + "\nx-akamai-acs-action:" + ha + '\n'
        dig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
        
        h2 = base64.b64encode(dig).decode()
        
        url = "https://" + host + path
        headers = {
                'X-Akamai-ACS-Action': ha,
                'X-Akamai-ACS-Auth-Data': h1,
                'X-Akamai-ACS-Auth-Sign': h2,
                'Content-Length': '0'}
        
        return self._req('PUT', url, headers=headers)

#download(arl, key, keyname, '~/Downloads')
#upload(arl, key, keyname, file)
#delete(arl, key, keyname)
#print(xdir(arl, key, keyname).text)
#print(xdu(arl, key, keyname).text)
#mkdir(arl, key, keyname)
#mtime(arl, key, keyname, 988888888) # cannot change folders
#quickdelete(arl, key, keyname) # must be explicitly enabled by Akamai
#rename(arl, key, keyname, uri)
#rmdir(arl, key, keyname)
#rmdir_rec(arl, key, keyname)
# ^seen success with 404 (doubling on timeouts?) and empty folder staying with 409 (sync issue?) :
"""
while True:
    r = rmdir_rec().status_code
    if r == 200 or r == 404: break
"""
#print(stat(arl, key, keyname).text)
#symlink(arl, key, keyname, target) # no trailing slash in arl
#ns = Akamai(read_timeout=5)
