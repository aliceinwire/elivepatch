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
    'targetHost': fields.String,
    'targetOS': fields.String,
    'packageName': fields.String,
    'packageVersion': fields.String,
    'packageAction': fields.String,
    'uri': fields.Url('packages')
}

result_fields = {
    'Result': fields.String,
    'uri': fields.Url('packages')
}

packs = None

lpatch = PaTch()

class getLivePatch(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('targetHost', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        super(getLivePatch, self).__init__()

    def get(self):
        lpatch.build_livepatch('/usr/src/linux-4.10.16-gentoo/', '/usr/src/linux-4.10.16-gentoo/vmlinux')
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'})
                             , 403)
        # return {'packs': [marshal(pack, pack_fields) for pack in packs]}

    def post(self):
        args = self.reqparse.parse_args()
        pack = {
            'id': packs[-1]['id'] + 1,
            'targetHost': args['targetHost'],
            'targetOS': args['targetOS'],
            'packageName': args['packageName'],
            'packageVersion': args['packageVersion'],
            'packageAction': args['packageAction'],
        }
        # result = livepatch_work.package_get(pack)
        result = {'Result':'result'}
        return {'agent': marshal(result, result_fields)}, 201


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