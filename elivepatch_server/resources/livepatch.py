#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import subprocess
import os
import fileinput
import tempfile


class PaTch(object):

    def __init__(self):
        pass

    def build_livepatch(self, uuid, vmlinux, debug=True):
        """
        Function for building the livepatch

        :param uuid: UUID session identification
        :param vmlinux: path to the vmlinux file
        :param debug: copy build.log in the uuid directory
        :return: void
        """
        kernel_source = os.path.join('/tmp/', 'elivepatch-' + uuid, 'usr/src/linux/')
        uuid_dir = os.path.join('/tmp/', 'elivepatch-' + uuid)
        vmlinux_source = os.path.join(kernel_source, vmlinux)
        kpatch_cachedir = os.path.join(uuid_dir, 'kpatch')

        os.makedirs(kpatch_cachedir)
        if not os.path.isfile(vmlinux_source):
            self.build_kernel(uuid)

        bashCommand = ['kpatch-build']
        bashCommand.extend(['-s', kernel_source])
        bashCommand.extend(['-v', vmlinux_source])
        bashCommand.extend(['-c', 'config'])
        bashCommand.extend(['main.patch'])
        bashCommand.extend(['--skip-gcc-check'])
        if debug:
            bashCommand.extend(['--skip-cleanup'])
            bashCommand.extend(['--debug'])
        _command(bashCommand, uuid_dir, {'CACHEDIR': kpatch_cachedir})
        if debug:
            _command(['cp', '-f', os.path.join(kpatch_cachedir, 'build.log'), uuid_dir])

    def get_kernel_sources(self, uuid, kernel_version):
        """
        Function for download the kernel sources

        :return: void
        """
        try:
            _command(['git', 'clone', 'https://github.com/aliceinwire/gentoo-sources_overlay.git'])
        except:
            print('git clone failed.')

        uuid_dir = os.path.join('/tmp/', 'elivepatch-' + uuid)
        ebuild_path = os.path.join('gentoo-sources_overlay', 'sys-kernel', 'gentoo-sources', 'gentoo-sources-' + kernel_version + '.ebuild')
        print(ebuild_path)
        if os.path.isfile(ebuild_path):
            # Use a private tmpdir for portage
            with tempfile.TemporaryDirectory(dir=uuid_dir) as portage_tmpdir:
                print('uuid_dir: ' + str(uuid_dir) + ' PORTAGE_TMPDIR: ' + str(portage_tmpdir))
                # portage_tmpdir is not always working with root priviledges
                env = {'ROOT': uuid_dir, 'PORTAGE_CONFIGROOT': uuid_dir, 'PORTAGE_TMPDIR': portage_tmpdir}
                _command(['ebuild', ebuild_path, 'clean', 'digest', 'merge'], env=env)
                kernel_sources_status = True
        else:
            print('ebuild not present')
            kernel_sources_status = None
        return kernel_sources_status

    def build_kernel(self, uuid):
        kernel_source_dir = '/tmp/elivepatch-' + uuid + '/usr/src/linux/'
        uuid_dir_config = '/tmp/elivepatch-' + uuid + '/config'
        if 'CONFIG_DEBUG_INFO=y' in open(uuid_dir_config).read():
            print("DEBUG_INFO correctly present")
        elif 'CONFIG_DEBUG_INFO=n' in open(uuid_dir_config).read():
            print("changing DEBUG_INFO to yes")
            for line in fileinput.input(uuid_dir_config, inplace=1):
                print(line.replace("CONFIG_DEBUG_INFO=n", "CONFIG_DEBUG_INFO=y"))
        else:
            print("Adding DEBUG_INFO for getting kernel debug symbols")
            for line in fileinput.input(uuid_dir_config, inplace=1):
                print(line.replace("# CONFIG_DEBUG_INFO is not set", "CONFIG_DEBUG_INFO=y"))
        _command(['cp', '/tmp/elivepatch-' + uuid + '/config', kernel_source_dir + '.config'])
        # olddefconfig default everything that is new from the configuration file
        _command(['make', 'olddefconfig'], kernel_source_dir)
        _command(['make'], kernel_source_dir)
        _command(['make', 'modules'], kernel_source_dir)


def _command(bashCommand, kernel_source_dir=None, env=None):
        """
        Popen override function

        :param bashCommand: List of command arguments to execute
        :param kernel_source_dir: String with the directory where the command is executed
        :param env: Dictionary for setting system environment variable
        :return: void
        """
        # Inherit the parent environment and update the private copy
        if env:
            process_env = os.environ.copy()
            process_env.update(env)
            env = process_env

        if kernel_source_dir:
            print(bashCommand)
            process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE,  cwd=kernel_source_dir, env=env)
            output, error = process.communicate()
            for output_line in output.split(b'\n'):
                print(output_line.strip())
        else:
            print(bashCommand)
            process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, env=env)
            output, error = process.communicate()
            for output_line in output.split(b'\n'):
                print(output_line.strip())
