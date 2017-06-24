#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
# ELIVEPATCH SERVER DISPATCHER
#################################################################################
# File:       cli.py
#
#             Handles elivepatch actions via the command line interface.
#
# Copyright:
#             (c) 2017 Alice Ferrazzi
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Alice Ferrazzi <alicef@gentoo.org>
#

from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
import werkzeug

from elivepatch_server.resources.livepatch import PaTch

pack_fields = {
    'KernelVersion': fields.String,
    'LivepatchStatus': fields.String
}

packs = {
    'id': 1,
    'KernelVersion': None,
    'LivepatchStatus': None
}

lpatch = PaTch()
lpatch.set_kernel_dir('/usr/src/linux-4.10.14-gentoo/')
kernel_dir = lpatch.get_kernel_dir()


class buildLivePatch(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KernelVersion', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('LivepatchStatus', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        super(buildLivePatch, self).__init__()
        pass

    def get(self):
        lpatch.build_livepatch(kernel_dir, kernel_dir + '/vmlinux')
        return {'packs': [marshal(pack, pack_fields) for pack in packs]}

    def post(self):
        args = self.reqparse.parse_args()
        kernel_config = lpatch.get_config()
        kernel_patch = lpatch.get_patch()
        if kernel_config and kernel_patch:
            lpatch.set_lp_status('working')
            lpatch.build_livepatch(kernel_dir, kernel_dir + '/vmlinux')
        pack = {
            'id': packs['id'] + 1,
            'KernelVersion': args['KernelVersion'],
            'LivepatchStatus': lpatch.livepatch_status,
        }
        return {'agent': marshal(pack, pack_fields)}, 201


class getLivePatch(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KernelVersion', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('LivepatchStatus', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        super(getLivePatch, self).__init__()
        pass

    def get(self):
        # Getting livepatch build status
        status = lpatch.get_lp_status()
        if status == 'done':
            response = make_response()
            response.headers['content-type'] = 'application/octet-stream'
            return response
        return {'packs': [marshal(pack, pack_fields) for pack in packs]}

    def post(self):
        args = self.reqparse.parse_args()
        kernel_config = lpatch.get_config()
        kernel_patch = lpatch.get_patch()
        if kernel_config and kernel_patch:
            lpatch.set_lp_status('working')
            lpatch.build_livepatch(kernel_dir, kernel_dir + '/vmlinux')
        pack = {
            'id': packs['id'] + 1,
            'KernelVersion': args['KernelVersion'],
            'LivepatchStatus': lpatch.livepatch_status,
        }
        return {'agent': marshal(pack, pack_fields)}, 201


class getConfig(Resource):

    def __init__(self):
        pass

    def get(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'})
                             , 403)

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        audioFile = args['file']
        audioFile_name = args['file'].filename
        print(audioFile_name)
        print(audioFile)
        audioFile.save(audioFile_name)
        lpatch.set_config(audioFile_name)


class getPatch(Resource):

    def __init__(self):
        pass

    def get(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'})
                             , 403)

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        audioFile = args['file']
        audioFile_name = args['file'].filename
        print(audioFile_name)
        print(audioFile)
        audioFile.save(audioFile_name)
        lpatch.set_patch(audioFile_name)