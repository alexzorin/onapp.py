"""
    @Author 	Alex Zorin
    @License	MIT

    Python Module for OnApp 3.x Clouds' API
"""

import httplib
import base64
import json


class OnAppConnection:
    def __init__(self, dashboard_host='', email='', api_key=''):
        self._auth = base64.encodestring('%s:%s' % (email, api_key))
        self._conn = httplib.HTTPSConnection(dashboard_host, 443)
        self._conn.connect()

    def makerequest(self, method='GET', page='/', data=None):
        headers = {
            'Authorization': ('Basic %s' % self._auth).replace('\n', ''),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        self._conn.request(method, page, data, headers)
        res = self._conn.getresponse()

        asJson = None
        v = res.read()

        try:
            asJson = json.loads(v)
        except Exception, e:
            raise RuntimeError('%s: %s' % (e, v))

        if res.status < 200 or res.status > 299:
            raise OnAppError(message='Non-2xx API response', data=asJson)
        else:
            return asJson

    def getversion(self):
        resp = self.makerequest('GET', '/version.json')
        if 'version' in resp:
            return resp['version'];
        else:
            raise OnAppError(message='Version not in response', data=resp)


class OnAppError(Exception):
    def __init__(self, message='', data=None):
        self.message = message
        self.data = data

    def __str__(self):
        return '%s: %s' % (self.message, repr(self.data))

class OnAppVirtualMachines:
    def __init__(self, base):
        self.base = base

    def list(self, limit=None,page=None):
        args = ''
        if limit is not None and page is not None:
            args += 'per_page=%d&page=%d' % (limit, page)
            
        res = self.base.makerequest('GET', '/virtual_machines.json?%s' % args)
        return res
