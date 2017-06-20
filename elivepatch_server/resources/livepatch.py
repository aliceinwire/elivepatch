# (c) 2015, Alice Ferrazzi <alice.ferrazzi@gmail.com>
#
# This file is part of elivepatch
#
# elivepatch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# elivepatch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with elivepatch.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
import werkzeug

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

class LivePAtchActionAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('targetHost', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('targetOS', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('packageName', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('packageVersion', type=unicode,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('packageAction', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        super(LivePAtchActionAPI, self).__init__()

    def get(self):
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
