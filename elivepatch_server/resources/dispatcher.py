#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later


import re

import os
import werkzeug
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, fields, marshal

from elivepatch_server.resources.livepatch import PaTch

pack_fields = {
    'KernelVersion': fields.String,
    'UUID': fields.String

}

packs = {
    'id': 1,
    'KernelVersion': None,
    'UUID': None
}


def check_uuid(uuid):
    """
    Check uuid is in the correct format
    :param uuid:
    :return:
    """
    if not uuid:
        print('uuid is missing')
    else:
        # check uuid format
        prog = re.compile('^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        result = prog.match(uuid)
        if result:
            print('UUID: ' + str(uuid))
            return uuid
        print('uuid format is not correct')


def get_uuid_dir(uuid):
    return os.path.join('/tmp/', 'elivepatch-' + uuid)


class BuildLivePatch(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KernelVersion', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('UUID', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        super(BuildLivePatch, self).__init__()
        pass

    def get(self):
        return {'packs': [marshal(pack, pack_fields) for pack in packs]}

    def post(self):
        lpatch = PaTch()
        args = self.reqparse.parse_args()
        args['UUID'] = check_uuid(args['UUID'])
        if args['KernelVersion']:
            print("build livepatch: " + str(args))
            # check vmlinux presence if not rebuild the kernel
            lpatch.get_kernel_sources(args['UUID'], args['KernelVersion'])
            lpatch.build_livepatch(args['UUID'], 'vmlinux')
        pack = {
            'id': packs['id'] + 1,
            'KernelVersion': args['KernelVersion'],
            'UUID' : args['UUID']
        }
        return {'build_livepatch': marshal(pack, pack_fields)}, 201

    @staticmethod
    def build_kernel_path(uuid, kernel_version):
        kernel_absolute_path = 'linux-' + str(kernel_version) + '-gentoo'
        kernel_path = os.path.join('/tmp/', 'elivepatch-' + uuid, 'usr',
                                   'src', kernel_absolute_path)
        return kernel_path


class SendLivePatch(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KernelVersion', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('UUID', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        super(SendLivePatch, self).__init__()
        pass

    def get(self):
        args = self.reqparse.parse_args()
        print("get livepatch: " + str(args))
        # check if is a valid UUID request
        args['UUID'] = check_uuid(args['UUID'])
        uuid_dir = get_uuid_dir(args['UUID'])

        livepatch_full_path = os.path.join(uuid_dir, 'kpatch-'+ str(args['UUID']) + '-livepatch.ko')
        try:
            with open(livepatch_full_path, 'rb') as fp:
                response = make_response(fp.read())
                response.headers['content-type'] = 'application/octet-stream'
                return response
        except:
            return make_response(jsonify({'message': 'These are not the \
            patches you are looking for'}), 403)

    def post(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)


class GetFiles(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KernelVersion', type=str, required=False,
                                   help='No task title provided',
                                   location='headers')
        self.reqparse.add_argument('UUID', type=str, required=False,
                                   help='No task title provided',
                                   location='headers')
        super(GetFiles, self).__init__()
        pass

    def get(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)

    def post(self):
        args = self.reqparse.parse_args()
        args['UUID'] = check_uuid(args['UUID'])
        parse = reqparse.RequestParser()
        parse.add_argument('patch', type=werkzeug.datastructures.FileStorage,
                           location='files')
        parse.add_argument('config', type=werkzeug.datastructures.FileStorage,
                           location='files')
        file_args = parse.parse_args()
        print("file get config: " + str(file_args))
        configFile = file_args['config']
        configFile_name = file_args['config'].filename

        patchfile = file_args['patch']
        patchfile_name = file_args['patch'].filename

        configFile_name = os.path.join('/tmp','elivepatch-' + args['UUID'], configFile_name)
        if os.path.exists('/tmp/elivepatch-' + args['UUID']):
            # TODO: case the path already exist
            print('the folder: "/tmp/elivepatch-' + args['UUID'] + '" is already present')
            pass
        else:
            print('creating: "/tmp/elivepatch-' + args['UUID'])
            os.makedirs('/tmp/elivepatch-' + args['UUID'])

        configFile.save(configFile_name)

        patch_fulldir_name = os.path.join('/tmp','elivepatch-' + args['UUID'], patchfile_name)
        patchfile.save(patch_fulldir_name)

        pack = {
           'id': packs['id'] + 1,
            'KernelVersion': None,
            'UUID' : args['UUID']
        }
        return {'get_config': marshal(pack, pack_fields)}, 201


class GetID(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('UUID', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        super(GetID, self).__init__()
        pass

    def get(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)

    def post(self):
        args = self.reqparse.parse_args()
        print("get ID: " + str(args))
