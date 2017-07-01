#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later


from flask import jsonify, make_response
from flask_restful import Resource, reqparse, fields, marshal
import werkzeug

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

lpatch = PaTch()
lpatch.set_kernel_dir('/usr/src/linux-4.9.29-gentoo/')
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
        kernel_config = lpatch.get_config()
        kernel_patch = lpatch.get_patch()
        if kernel_config and kernel_patch:
            lpatch.set_lp_status('working')
            print("build livepatch: " + str(args))
            # lpatch.build_livepatch(kernel_dir, kernel_dir + '/vmlinux')
        pack = {
            'id': packs['id'] + 1,
            'KernelVersion': args['KernelVersion'],
            'LivepatchStatus': lpatch.livepatch_status,
        }
        return {'agent': marshal(pack, pack_fields)}, 201


class GetLivePatch(Resource):

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
        super(GetLivePatch, self).__init__()
        pass

    def get(self):
        args = self.reqparse.parse_args()
        print("get livepatch: " + str(args))
        # Getting livepatch build status
        status = lpatch.update_lp_status("kpatch-1.ko")
        if status == 'done':
            with open('kpatch-1.ko', 'rb') as fp:
                response = make_response(fp.read())
                response.headers['content-type'] = 'application/octet-stream'
                return response
        return {'packs': [marshal(pack, pack_fields) for pack in packs]}

    def post(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)


class GetConfig(Resource):

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
        super(GetConfig, self).__init__()
        pass

    def get(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)

    def post(self):
        args = self.reqparse.parse_args()
        print("get config: " + str(args))
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage,
                           location='files')
        args = parse.parse_args()
        audioFile = args['file']
        audioFile_name = args['file'].filename
        print(audioFile_name)
        print(audioFile)
        audioFile.save(audioFile_name)
        lpatch.set_config(audioFile_name)


class GetPatch(Resource):

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
        super(GetPatch, self).__init__()
        pass

    def get(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)

    def post(self):
        args = self.reqparse.parse_args()
        print("get patch: " + str(args))
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage,
                           location='files')
        args = parse.parse_args()
        audioFile = args['file']
        audioFile_name = args['file'].filename
        print(audioFile_name)
        print(audioFile)
        audioFile.save(audioFile_name)
        lpatch.set_patch(audioFile_name)


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


#def id_check()
