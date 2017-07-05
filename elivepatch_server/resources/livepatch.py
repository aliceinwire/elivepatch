#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import subprocess
import os


class PaTch(object):

    def __init__(self):
        self.config_file = None
        self.patch_file = None
        self.kernel_version = None
        self.livepatch_status = "Not started"
        self.kernel_dir = None

    def set_kernel_dir(self, kernel_dir):
        self.kernel_dir = kernel_dir

    def get_kernel_dir(self):
        return self.kernel_dir

    def set_lp_status(self, livepatch_status):
        self.livepatch_status = livepatch_status

    def get_lp_status(self):
        return self.livepatch_status

    def update_lp_status(self, livepatch):
        if os.path.isfile(livepatch):
            self.livepatch_status = 'done'
        return self.livepatch_status

    def set_kernel_version(self, kernel_version):
        self.kernel_version = kernel_version

    def get_kernel_version(self):
        return self.kernel_version

    def get_config(self):
        return self.config_file

    def set_config(self, config_file):
        self.config_file = config_file

    def set_patch(self, patch_file):
        self.patch_file = patch_file

    def get_patch(self):
        return self.patch_file

    def kernel_version(self):
        pass

    def compare_kernel_config(self):
        pass

    def recompile_kernel(self):
        pass

    def search_kernel_source_path(self):
        pass

    def get_kernel_source_path(self):
        self.kernel_path = ''
        return self.kernel_path

    # kpatch-build/kpatch-build -s /usr/src/linux-4.9.16-gentoo/
    # -v /usr/src/linux-4.9.16-gentoo/vmlinux examples/test.patch
    # -c ../elivepatch/elivepatch_server/config --skip-gcc-check
    def build_livepatch(self, kernel_source, vmlinux):
        """
        
        :param kernel_source: 
        :param vmlinux: 
        :return: 
        """
        debug=True
        bashCommand = ['sudo','kpatch-build']
        bashCommand.extend(['-s',kernel_source])
        bashCommand.extend(['-v',vmlinux])
        bashCommand.extend(['-c',self.config_file])
        bashCommand.extend([self.patch_file])
        bashCommand.extend(['--skip-gcc-check'])
        if debug:
            bashCommand.extend(['--skip-cleanup'])
            bashCommand.extend(['--debug'])
        print(bashCommand)
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)

    def build_kernel(self, kernel_source_dir):
        bashCommand = (['sudo','make','oldconfig'])
        print(bashCommand)
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, cwd=kernel_source_dir)
        output, error = process.communicate()
        print(output)

        bashCommand = (['sudo','make'])
        print(bashCommand)
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, cwd=kernel_source_dir)
        output, error = process.communicate()
        print(output)

    def get_kernel(self, kernel_version):
        bashCommand = ['sudo','emerge','-q','"=sys-kernel/gentoo-sources-'+kernel_version+'"']
        print(bashCommand)
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)
