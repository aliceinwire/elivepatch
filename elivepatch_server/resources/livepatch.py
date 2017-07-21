#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import subprocess
import os


class PaTch(object):

    def __init__(self):
        pass

    # kpatch-build/kpatch-build -s /usr/src/linux-4.9.16-gentoo/
    # -v /usr/src/linux-4.9.16-gentoo/vmlinux examples/test.patch
    # -c ../elivepatch/elivepatch_server/config --skip-gcc-check
    def build_livepatch(self, uuid, vmlinux):
        """
        Function for building the livepatch

        :param uuid: UUID session identification
        :param vmlinux: path to the vmlinux file
        :return: void
        """
        # TODO: use $CACHEDIR for define the .kpatch folder, if needed
        kernel_source = os.path.join('/tmp/','elivepatch-' + uuid, 'usr/src/linux/')
        uuid_dir = os.path.join('/tmp/','elivepatch-' + uuid)
        vmlinux_source = os.path.join(kernel_source, vmlinux)
        if not os.path.isfile(vmlinux_source):
            self.build_kernel(uuid)
        debug=True
        bashCommand = ['sudo', 'kpatch-build']
        bashCommand.extend(['-s',kernel_source])
        bashCommand.extend(['-v',vmlinux_source])
        bashCommand.extend(['-c','config'])
        bashCommand.extend(['01.patch'])
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
            print('git clone failed.')

        ebuild_path = os.path.join('gentoo-sources_overlay', 'sys-kernel', 'gentoo-sources', 'gentoo-sources-' + kernel_version + '.ebuild')
        print(ebuild_path)
        if os.path.isfile(ebuild_path):
            command(['sudo', 'ROOT=/tmp/elivepatch-' + uuid_dir, 'ebuild', ebuild_path, 'clean', 'merge'])
        else:
            print('ebuild not present')

    def build_kernel(self, uuid_dir):
        kernel_source_dir = '/tmp/elivepatch-' + uuid_dir + '/usr/src/linux/'
        command(['sudo','cp','/tmp/elivepatch-' + uuid_dir + '/config',kernel_source_dir + '.config'])
        # olddefconfig default everything that is new from the configuration file
        command(['sudo','make','olddefconfig'], kernel_source_dir)
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
