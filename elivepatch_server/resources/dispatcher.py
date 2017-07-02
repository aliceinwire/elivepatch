#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later


from flask import jsonify, make_response
from flask_restful import Resource, reqparse, fields, marshal
import werkzeug
import uuid
import os

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


def set_kernel_dir(kernel_ID):
    kernel_absolute_path = 'linux-' + str(kernel_ID) + '-gentoo'
    kernel_path = os.path.join('/usr','src',kernel_absolute_path)
    lpatch.set_kernel_dir(kernel_path)

lpatch = PaTch()
kernel_dir = lpatch.get_kernel_dir()
set_kernel_dir(kernel_dir)

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
        if not args['UserID']:
            args['UserID'] = id_generate()
        else:
            print('UserID: ' + str(args['UserID']))
        if args['KernelVersion']:
            set_kernel_dir(args['KernelVersion'])
            kernel_dir = lpatch.get_kernel_dir()
        kernel_config = lpatch.get_config()
        kernel_patch = lpatch.get_patch()
        if kernel_config and kernel_patch:
            lpatch.set_lp_status('working')
            print("build livepatch: " + str(args))
            lpatch.build_livepatch(kernel_dir, kernel_dir + '/vmlinux')
        pack = {
            'id': packs['id'] + 1,
            'KernelVersion': args['KernelVersion'],
            'LivepatchStatus': lpatch.livepatch_status,
            'UserID' : args['UserID']
        }
        return {'build_livepatch': marshal(pack, pack_fields)}, 201


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
        # check if is a new user
        if not args['UserID']:
            args['UserID'] = id_generate()
        else:
            print('UserID: ' + str(args['UserID']))
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
                                   location='headers')
        super(GetConfig, self).__init__()
        pass

    def get(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)

    def post(self):
        args = self.reqparse.parse_args()
        print("json get config: " + str(args))
        if not args['UserID']:
            args['UserID'] = str(id_generate())
        else:
            print('UserID: ' + str(args['UserID']))
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage,
                           location='files')
        parse.add_argument('KernelVersion', type=str, required=False,
                                   location='json')
        parse.add_argument('LivepatchStatus', type=str, required=False,
                                   location='json')
        parse.add_argument('UserID', type=str, required=False,
                                   location='headers')
        file_args = parse.parse_args()
        print("file get config: " + str(file_args))
        audioFile = file_args['file']
        audioFile_name = file_args['file'].filename
        #print('audiofile_name: '+ str(audioFile_name))
        #print('audiofile: '+ str(audioFile))
        audioFile_name = os.path.join('/tmp','elivepatch-' + args['UserID'], audioFile_name)
        if not os.path.exists('/tmp/elivepatch-' + args['UserID']):
            os.makedirs('/tmp/elivepatch-' + args['UserID'])
        audioFile.save(audioFile_name)
        lpatch.set_config(audioFile_name)
        pack = {
            'id': packs['id'] + 1,
            'KernelVersion': None,
            'LivepatchStatus': lpatch.livepatch_status,
            'UserID' : args['UserID']
        }
        return {'get_config': marshal(pack, pack_fields)}, 201


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
                                   location='headers')
        super(GetPatch, self).__init__()
        pass

    def get(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)

    def post(self):
        args = self.reqparse.parse_args()
        print("get patch: " + str(args))
        if not args['UserID']:
            args['UserID'] = str(id_generate())
        else:
            print('UserID: ' + str(args['UserID']))
        # parse file request information's
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage,
                           location='files')
        file_args = parse.parse_args()
        audioFile = file_args['file']
        audioFile_name = file_args['file'].filename
        #print(audioFile_name)
        #print(audioFile)
        audioFile_name = os.path.join('/tmp', 'elivepatch-' + args['UserID'], audioFile_name)
        if not os.path.exists('/tmp/elivepatch-'+args['UserID']):
            os.makedirs('/tmp/elivepatch-'+args['UserID'])
        audioFile.save(audioFile_name)
        lpatch.set_patch(audioFile_name)
        pack = {
            'id': packs['id'] + 1,
            'KernelVersion': None,
            'LivepatchStatus': lpatch.livepatch_status,
            'UserID' : args['UserID']
        }
        return {'get_patch': marshal(pack, pack_fields)}, 201


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


def id_generate():
    #print('no id')
    UserID = uuid.uuid4()
    #print(UserID)
    return UserID
