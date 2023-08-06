#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0
import os

from osmosis_driver_interface.data_plugin import AbstractPlugin


class Plugin(AbstractPlugin):
    IPFS_GATEWAY_ENVVAR = 'IPFS_GATEWAY'
    DEFAULT_IPFS_GATEWAY = 'https://gateway.ipfs.io'
    PROTOCOL = 'ipfs://'

    def __init__(self, config=None):
        self.config = config
        self._ipfs_gateway = os.getenv(Plugin.IPFS_GATEWAY_ENVVAR, Plugin.DEFAULT_IPFS_GATEWAY)

    def type(self):
        """str: the type of this plugin (``'IPFS'``)"""
        return 'IPFS'

    def upload(self, local_file, remote_file):
        pass

    def download(self, remote_file, local_file):
        pass

    def list(self, remote_folder):
        pass

    @staticmethod
    def parse_url(url):
        assert url and isinstance(url, str) \
               and url.startswith(Plugin.PROTOCOL), \
               f'Bad argument type `{url}`, expected ' \
               f'a str URL starting with "ipfs://"'

        cid = url.split(Plugin.PROTOCOL)[1]
        return cid

    def generate_url(self, remote_file):
        return f'{self._ipfs_gateway}/ipfs/{self.parse_url(remote_file)}'

    def delete(self, remote_file):
        pass

    def copy(self, source_path, dest_path):
        pass

    def create_directory(self, remote_folder):
        pass

    def retrieve_availability_proof(self):
        pass
