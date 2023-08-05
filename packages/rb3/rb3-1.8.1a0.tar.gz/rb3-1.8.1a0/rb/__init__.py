"""
    rb3, the rb fork support Python3.7
    ~~

    The redis blaster.

    :copyright: (c) 2015 Functional Software Inc.
    :license: Apache License 2.0, see LICENSE for more details.
"""
from rb.cluster import Cluster
from rb.clients import RoutingClient, MappingClient, FanoutClient
from rb.router import BaseRouter, ConsistentHashingRouter, PartitionRouter, \
    UnroutableCommand
from rb.promise import Promise


__version__ = '1.8.1a'

__all__ = [
    # cluster
    'Cluster',

    # client
    'RoutingClient', 'MappingClient', 'FanoutClient',

    # router
    'BaseRouter', 'ConsistentHashingRouter', 'PartitionRouter',
    'UnroutableCommand',

    # promise
    'Promise',
]
