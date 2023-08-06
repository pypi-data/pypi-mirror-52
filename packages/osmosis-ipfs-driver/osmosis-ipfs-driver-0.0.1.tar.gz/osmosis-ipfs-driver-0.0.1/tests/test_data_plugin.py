#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0
import pytest

from osmosis_ipfs_driver.data_plugin import Plugin

plugin = Plugin()


def test_driver_type():
    assert plugin.type() == 'IPFS'


def test_parse_url():
    # Invalid urls
    # None
    url = None
    with pytest.raises(AssertionError):
        plugin.parse_url(url)

    # Empty str
    url = ''
    with pytest.raises(AssertionError):
        plugin.parse_url(url)
    # str with no ipfs://
    url = 'ip://ZnOfotxMMnLTXCCW0GPVYT8gtEugghgD8Hgz'
    with pytest.raises(AssertionError):
        plugin.parse_url(url)

    cid = 'some-valid-ipfs-cid'
    url = f'ipfs://{cid}'
    assert plugin.parse_url(url) == cid


def test_generate_url():
    cid = 'some-valid-ipfs-cid'
    url = f'ipfs://{cid}'
    resolved_url = f'{plugin.DEFAULT_IPFS_GATEWAY}/ipfs/{plugin.parse_url(url)}'
    assert plugin.generate_url(url) == resolved_url
