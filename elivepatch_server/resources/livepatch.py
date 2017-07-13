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
        self.patch_filename = None
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

    def set_patch_filename(self, patch_filename):
        self.patch_filename = patch_filename

    def get_patch_filename(self):
        return self.patch_filename

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
    def build_livepatch(self, uuid, vmlinux):
        """
        Function for building the livepatch

        :param kernel_source: directory of the kernel source
        :param vmlinux: path to the vmlinux file
        :return: void
        """
        kernel_source = os.path.join('/tmp/','elivepatch-' + uuid, 'usr/src/linux/')
        uuid_dir = os.path.join('/tmp/','elivepatch-' + uuid)
        vmlinux_source = os.path.join(kernel_source, vmlinux)
        if not os.path.isfile(vmlinux_source):
            self.build_kernel(uuid)
        debug=True
        bashCommand = ['sudo','kpatch-build']
        bashCommand.extend(['-s',kernel_source])
        bashCommand.extend(['-v',vmlinux_source])
        bashCommand.extend(['-c',self.config_file])
        bashCommand.extend([self.patch_file])
        bashCommand.extend(['--skip-gcc-check'])
        if debug:
            bashCommand.extend(['--skip-cleanup'])
            bashCommand.extend(['--debug'])
        command(bashCommand, uuid_dir)

    def get_kernel_sources(self, uuid_dir, kernel_version):
        """
        Function for download the kernel sources

        :return: void
        """
        try:
            command(['git','clone','https://github.com/aliceinwire/gentoo-sources_overlay.git'])
        except:
            print('Gentoo-sources overlay already present.')
        command(['sudo','ROOT=/tmp/elivepatch-' + uuid_dir,'ebuild','gentoo-sources_overlay/sys-kernel/gentoo-sources/gentoo-sources-' + kernel_version + '.ebuild', 'clean'])
        command(['sudo','ROOT=/tmp/elivepatch-' + uuid_dir,'ebuild','gentoo-sources_overlay/sys-kernel/gentoo-sources/gentoo-sources-' + kernel_version + '.ebuild', 'merge'])

    def build_kernel(self, uuid_dir):
        kernel_source_dir = '/tmp/elivepatch-' + uuid_dir + '/usr/src/linux/'
        command(['sudo','cp','/tmp/elivepatch-' + uuid_dir + '/config',kernel_source_dir + '.config'])
        command(['sudo','make','oldconfig'], kernel_source_dir)
        command(['sudo','make'], kernel_source_dir)
        command(['sudo','make', 'modules'], kernel_source_dir)
        command(['sudo','make', 'modules_install'], kernel_source_dir)


def command(bashCommand, kernel_source_dir=None):
        """
        Popen override function

        :param bashCommand: List of command arguments to execute
        :param kernel_source_dir: the source directory of the kernel
        :return: void
        """
        if kernel_source_dir:
            print(bashCommand)
            process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE,  cwd=kernel_source_dir)
            output, error = process.communicate()
            print(output)
        else:
            print(bashCommand)
            process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
            output, error = process.communicate()
            print(output)
