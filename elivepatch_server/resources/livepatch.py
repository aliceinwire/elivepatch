#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
# ELIVEPATCH SERVER LIVEPATCH
#################################################################################
# File:       livepatch.py
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

import subprocess

class PaTch(object):

    def __init__(self):
        self.config_file = None
        self.patch_file = None

    def set_config(self, config_file):
        self.config_file = config_file

    def set_patch(self, patch_file):
        self.patch_file = patch_file

    def get_config(self):
        return self.config_file

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
        self.kernel_path =''
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
        bashCommand = 'kpatch-build'
        bashCommand += ' -s '+ kernel_source
        bashCommand += ' -v '+ vmlinux
        bashCommand += ' -c '+ self.config_file
        bashCommand += ' ' + self.patch_file
        bashCommand += ' --skip-gcc-check'
        print(bashCommand)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)
