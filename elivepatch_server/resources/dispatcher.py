#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later


import uuid

import os
import werkzeug
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, fields, marshal

from elivepatch_server.resources.livepatch import PaTch

pack_fields = {
    'KernelVersion': fields.String,
    'LivepatchStatus': fields.String,
    'UserID': fields.String

}

packs = {
    'id': 1,
    'KernelVersion': None,
    'LivepatchStatus': None,
    'UserID': None
}


def id_generate():
    UserID = str(uuid.uuid4())
    return UserID


def check_uuid(uuid):
    if not uuid:
        print('Generating new uuid')
        return id_generate()
    else:
        print('UserID: ' + str(uuid))
        return uuid


def get_uuid_dir(uuid):
    return os.path.join('/tmp/', 'elivepatch-' + uuid)


def set_kernel_dir(uuid, kernel_version):
    kernel_absolute_path = 'linux-' + str(kernel_version) + '-gentoo'
    kernel_path = os.path.join('/tmp/', 'elivepatch-' + uuid, 'usr', 'src', kernel_absolute_path)
    lpatch.set_kernel_dir(kernel_path)

lpatch = PaTch()
kernel_dir = lpatch.get_kernel_dir()


class BuildLivePatch(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KernelVersion', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('LivepatchStatus', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('UserID', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        super(BuildLivePatch, self).__init__()
        pass

    def get(self):
        # lpatch.build_livepatch(kernel_dir, kernel_dir + '/vmlinux')
        return {'packs': [marshal(pack, pack_fields) for pack in packs]}

    def post(self):
        args = self.reqparse.parse_args()
        args['UserID'] = check_uuid(args['UserID'])
        if args['KernelVersion']:
            set_kernel_dir(args['UserID'], args['KernelVersion'])
            kernel_config = lpatch.get_config()
            kernel_patch = lpatch.get_patch()
            if kernel_config and kernel_patch:
                lpatch.set_lp_status('working')
                print("build livepatch: " + str(args))
                # check vmlinux presence if not rebuild the kernel
                lpatch.get_kernel_sources(args['UserID'], args['KernelVersion'])
                lpatch.build_livepatch(args['UserID'], 'vmlinux')
        pack = {
            'id': packs['id'] + 1,
            'KernelVersion': args['KernelVersion'],
            'LivepatchStatus': lpatch.livepatch_status,
            'UserID' : args['UserID']
        }
        return {'build_livepatch': marshal(pack, pack_fields)}, 201


class SendLivePatch(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KernelVersion', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('UserID', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        super(SendLivePatch, self).__init__()
        pass

    def get(self):
        args = self.reqparse.parse_args()
        print("get livepatch: " + str(args))
        # check if is a new user
        args['UserID'] = check_uuid(args['UserID'])
        uuid_dir = get_uuid_dir(args['UserID'])
        patch_name = lpatch.get_patch_filename()

        # change patch extension to .ko
        base = os.path.splitext(patch_name)[0]
        livepatch_name = base + ".ko"

        # Getting livepatch build status
        livepatch_full_path = os.path.join(uuid_dir, 'kpatch-'+livepatch_name)
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
        self.reqparse.add_argument('UserID', type=str, required=False,
                                   help='No task title provided',
                                   location='headers')
        super(GetFiles, self).__init__()
        pass

    def get(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)

    def post(self):
        args = self.reqparse.parse_args()
        args['UserID'] = check_uuid(args['UserID'])
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

        configFile_name = os.path.join('/tmp','elivepatch-' + args['UserID'], configFile_name)
        if not os.path.exists('/tmp/elivepatch-' + args['UserID']):
            os.makedirs('/tmp/elivepatch-' + args['UserID'])
        configFile.save(configFile_name)
        lpatch.set_config(configFile_name)

        patch_fulldir_name = os.path.join('/tmp','elivepatch-' + args['UserID'], patchfile_name)
        if not os.path.exists('/tmp/elivepatch-' + args['UserID']):
            os.makedirs('/tmp/elivepatch-' + args['UserID'])
        patchfile.save(patch_fulldir_name)
        lpatch.set_patch(patch_fulldir_name)
        lpatch.set_patch_filename(patchfile_name)

        pack = {
           'id': packs['id'] + 1,
            'KernelVersion': None,
            'UserID' : args['UserID']
        }
        return {'get_config': marshal(pack, pack_fields)}, 201


class GetID(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('UserID', type=str, required=False,
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



