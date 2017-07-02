#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import time
import requests


class ManaGer(object):
    def __init__(self, server_url, kernel_version):
        self.server_url = server_url
        self.kernel_version = kernel_version

    def version(self):
        url = self.server_url + '/elivepatch/api/v1.0/agent'
        r = requests.get(url)
        print(r.text)
        print(r.json())

    def send_file(self, send_file, name_file, api):
        url = self.server_url+ api
        # we are sending the file and the UserID
        # The server is dividing user by UserID
        # UserID is generated with python UUID
        # TODO: add the UserID in the json location instead of headers
        headers = {'UserID': 'test-00001'}
        files = {'file': (name_file, open(send_file, 'rb'), 'multipart/form-data', {'Expires': '0'})}
        payload = {
            "KernelVersion" : ("aaaa", 'application/json', {'Expires': '0'}),
            "LivepatchStatus" : ("not known", 'application/json', {'Expires': '0'}),
            "UserID" : ("test-00001",'application/json', {'Expires': '0'})
            }
        r = requests.post(url, files=files, headers=headers)
        print('send file: ' + str(r.json()))
        r_dict = r.json()
        return r_dict



    def build_livepatch(self):
        url = self.server_url+'/elivepatch/api/v1.0/build_livepatch'
        payload = {
            'KernelVersion': self.kernel_version,
            'LivepatchStatus' : 'no idea',
            'UserID' : 'test-0000'
        }
        r = requests.post(url, json=payload)
        # print(r.text)
        print(r.json())

    def get_livepatch(self):
        from io import BytesIO
        url = self.server_url+'/elivepatch/api/v1.0/get_livepatch'
        payload = {
            'KernelVersion': self.kernel_version,
            'LivepatchStatus' : 'no idea',
            'UserID' : 'test-0000'
        }
        r = requests.get(url, json=payload)
        if r.status_code == requests.codes.ok:  # livepatch returned ok
            b= BytesIO(r.content)
            with open('myfile.ko', 'wb') as out:
                out.write(r.content)
            r.close()
            print(b)
        else:
            r.close()
            time.sleep(5)
            return self.get_livepatch()  # try to get the livepatch again
