#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import gzip
import uuid

import os
import os.path
import re
from git import Repo

from elivepatch_client.client import restful


def id_generate_uuid():
    generated_uuid = str(uuid.uuid4())
    return generated_uuid


class Kernel(object):
    """
    Manage kernels files
    """
    def __init__(self, restserver_url, session_uuid=None):
        self.config_fullpath = ''
        self.patch_fullpath = ''
        self.restserver_url = restserver_url
        self.kernel_version = None
        if session_uuid:
            self.session_uuid = session_uuid
        else:
            self.session_uuid = id_generate_uuid()
        print('This session uuid: ' + str(self.session_uuid))
        self.rest_manager = restful.ManaGer(self.restserver_url, self.kernel_version, self.session_uuid)

    def set_config(self, config_fullpath):
        self.config_fullpath = config_fullpath

    def set_patch(self, patch_fullpath):
        self.patch_fullpath = patch_fullpath

    def send_files(self):
        """
        Send config and patch files

        :return: void
        """
        path, file = (os.path.split(self.config_fullpath))
        f_action = FileAction(self.config_fullpath)
        # check the configuration file
        if re.findall("[.]gz\Z", self.config_fullpath):
            print('gz extension')
            path, file = f_action.ungz()
            # if the file is .gz the configuration path is the tmp folder uncompressed config file
            self.config_fullpath = os.path.join(path, file)

        # Get kernel version from the configuration file header
        self.kernel_version = f_action.config_kernel_version(self.config_fullpath)
        self.rest_manager.set_kernel_version(self.kernel_version)
        print('debug: kernel version = ' + self.rest_manager.get_kernel_version())

        send_api = '/elivepatch/api/v1.0/get_files'

        # send uncompressed config and patch files fullpath
        self.rest_manager.send_file(self.config_fullpath, self.patch_fullpath, send_api)

    def build_livepatch(self):
        self.rest_manager.build_livepatch()

    def get_livepatch(self):
        self.rest_manager.get_livepatch()


class CVE(object):
    """
    Check the kernel against a CVE repository
    """
    def __init__(self):
        self.git_url = "https://github.com/nluedtke/linux_kernel_cves"
        self.repo_dir = "/tmp/kernel_cve/"
        pass

    def download(self):
        Repo.clone_from(self.git_url, self.repo_dir)

    def set_repo(self, git_url, repo_dir):
        self.git_url = git_url
        self.repo_dir = repo_dir


class FileAction(object):
    """
    Work with files
    """
    def __init__(self, full_path):
        self.full_path = full_path
        pass

    def ungz(self):
        """
        Uncompress gzipped configuration
        :return: Uncompressed configuration file path
        """
        uncompressed_file_fullpath = None
        path, filename = os.path.split(self.full_path)
        path_gz_file = os.path.join(path, filename)
        temporary_path_uncompressed_file = os.path.join('/tmp', filename)
        print('path_gz_file: '+ path_gz_file + ' temporary_path_uncompressed_file: ' +
              temporary_path_uncompressed_file)
        if not os.path.isdir(path_gz_file):
            with gzip.open(path_gz_file, 'rb') as in_file:
                s = in_file.read()
            # Store uncompressed file
            uncompressed_file_fullpath = temporary_path_uncompressed_file[:-3]  # remove the filename extension
            with open(uncompressed_file_fullpath, 'wb') as f:
                f.write(s)
            print('working')
        return uncompressed_file_fullpath

    def config_kernel_version(self, uncompressed_config_file):
        """
        Find the kernel version from where the configuration as been generated
        :param uncompressed_config_file:
        :return: kernel version
        """
        with open(uncompressed_config_file) as f:
            i = 0
            while i < 2:
                f.readline()
                if i == 1:
                    kernel_line = f.readline()
                i += 1
        kernel_version_raw = (kernel_line.split(' ')[2])
        kernel_version = kernel_version_raw.split(('-'))[0]
        return kernel_version

