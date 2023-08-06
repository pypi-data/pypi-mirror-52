# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import requests

__version__ = '0.0.2'


class LocomotiveApiError(Exception):

    def __init__(self, response, status_code):
        message = response.pop('error')
        super(LocomotiveApiError, self).__init__(message)
        self.status_code = status_code
        self.extra = response


class LocomotiveResource(object):

    def __init__(self, client):
        self.client = client
        self.call = self.client.call
        self.path = None

    def _path_with_slug(self, id_or_slug):
        return self._path + '/' + id_or_slug

    def search(self, page=1, per_page=80):
        return self.call(
            'get', self._path, {'page': page, 'per_page': per_page})

    def read(self, id_or_slug):
        return self.call('get', self._path_with_slug(id_or_slug))

    def write(self, id_or_slug, data):
        return self.call(
            'put',
            self._path_with_slug(id_or_slug),
            data={self._name: data})

    def create(self, data):
        return self.call('post', self._path, data={'content_entry': data})

    def delete(self, id_or_slug):
        return self.call('delete', self._path_with_slug(id_or_slug))


class LocomotiveContent(LocomotiveResource):
    _path = None
    _name = 'content_entry'

    def __init__(self, client, content_type):
        super(LocomotiveContent, self).__init__(client)
        self._path = '/content_types/%s/entries' % content_type


class LocomotiveAsset(LocomotiveResource):
    _path = '/content_assets'
    _name = 'content_asset'

    def write(self, id_or_slug, data):
        return self.call(
            'put', self._path_with_slug(id_or_slug),
            files={'source': (data['filename'], data['file'])})

    def create(self, data):
        return self.call(
            'post', self.path,
            files={'content_asset[source]': (data['filename'], data['file'])})


class LocomotiveSite(LocomotiveResource):
    _path = '/sites'
    _name = 'site'


class LocomotiveClient(object):

    def __init__(self, email, api_key, handle, url):
        self.api_key = api_key
        self.email = email
        self.handle = handle
        self.url = url + '/locomotive/api/v3'
        # TODO catch error
        r = requests.post(
            self.url + '/tokens.json', {
                'api_key': self.api_key,
                'email': self.email,
                })
        r.raise_for_status()
        self.token = r.json()['token']

    def header(self):
        return {
            'X-Locomotive-Account-Email': self.email,
            'X-Locomotive-Account-Token': self.token,
            'X-Locomotive-Site-Handle': self.handle,
            }

    def call(self, method, url, data=None, files=None):
        kwargs = {'headers': self.header()}
        if method == 'get':
            kwargs['params'] = data
        else:
            kwargs['json'] = data
            kwargs['files'] = files
        res = getattr(requests, method)(self.url + url, **kwargs)
        if res.status_code/100 != 2:
            raise LocomotiveApiError(res.json(), res.status_code)
        return res.json()

    def content(self, content_type):
        return LocomotiveContent(self, content_type)

    def asset(self):
        return LocomotiveAsset(self)

    def site(self):
        return LocomotiveSite(self)
