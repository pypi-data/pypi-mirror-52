# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Connect Python SDK.
#  For full information on usage and licensing, see https://chirp.io/
#
#  Copyright (c) 2011-2019, Asio Ltd.
#  All rights reserved.
#
# ------------------------------------------------------------------------
from datetime import datetime

import requests
from requests_futures.sessions import FuturesSession

from . import __version__
from .exceptions import ChirpSDKNetworkError

session = FuturesSession()
config_url = 'https://config.chirp.io'
analytics_url = 'https://analytics.chirp.io'


def get_config_from_network(key, secret, name=None):
    """
    Retrieve a config for an application.
    If name is specified then this config is returned, otherwise
    the default is used.

    Args:
        name (str): config name, default is used if not set

    Returns: (str) config string

    Raises:
        ChirpSDKNetworkError: If config request fails
        ValueError: If an invalid config name is requested
    """
    try:
        url = config_url + '/v3/connect'
        if name:
            url += '/' + name

        r = requests.get(url, auth=(key, secret))
        if r.status_code != 200:
            err = r.json()
            raise ChirpSDKNetworkError(err.get('message', 'Failed to retrieve config'))

        data = r.json()
        configs = [l['name'] for l in data['data']]
        if name and name not in configs:
            raise ValueError('Invalid config name')
        return data['data'][configs.index(name)]['config'] if name else data['data'][0]['config']

    except requests.exceptions.ConnectionError:
        raise ChirpSDKNetworkError('No internet connection')
    except requests.exceptions.Timeout:
        raise ChirpSDKNetworkError('Timeout')
    except requests.exceptions.RequestException as err:
        raise ChirpSDKNetworkError(str(err))


def async_request(url, auth, data):
    """
    Asynschronous request with no consequences

    Args:
        url (str): url to post data to
        auth (tuple): username and password in a tuple
        data (dict): json data to post
    """
    try:
        session.post(url, auth=auth, json=data)
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.RequestException as err:
        pass


def create_instantiate(key, secret, uid):
    """
    Instantiated the SDK

    Args:
        key (str): Chirp application key
        secret (str): Chirp application secret
        uid (str): unique device id
    """
    url = analytics_url + '/v3/connect/instantiate'
    async_request(url, (key, secret), {
        'client_id': uid,
        'timestamp': datetime.now().isoformat(),
        'platform': 'python',
        'sdk_version': __version__
    })


def create_send(key, secret, uid, length, protocol_name, protocol_version):
    """
    Sent a payload

    Args:
        key (str): Chirp application key
        secret (str): Chirp application secret
        uid (str): unique device id
        length (int): length of payload sent
        protocol_name (str): name of protocol used
        protocol_version (int): version of protocol used
    """
    url = analytics_url + '/v3/connect/send'
    async_request(url, (key, secret), {
        'client_id': uid,
        'timestamp': datetime.now().isoformat(),
        'payload_length': length,
        'protocol_name': protocol_name,
        'protocol_version': protocol_version,
        'platform': 'python',
        'sdk_version': __version__
    })


def create_receive(key, secret, uid, length, protocol_name, protocol_version):
    """
    Received a payload

    Args:
        key (str): Chirp application key
        secret (str): Chirp application secret
        uid (str): unique device id
        length (int): length of payload sent
        protocol_name (str): name of protocol used
        protocol_version (int): version of protocol used
    """
    url = analytics_url + '/v3/connect/receive'
    async_request(url, (key, secret), {
        'client_id': uid,
        'timestamp': datetime.now().isoformat(),
        'success': length != 0,
        'payload_length': length,
        'protocol_name': protocol_name,
        'protocol_version': protocol_version,
        'platform': 'python',
        'sdk_version': __version__
    })
