# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

import datetime
from tempfile import gettempdir
import streamsx.spl.op
import streamsx.spl.types
from streamsx.topology.schema import CommonSchema, StreamSchema
from streamsx.spl.types import rstring

from streamsx.toolkits import download_toolkit

_TOOLKIT_NAME = 'com.ibm.streamsx.inetserver'



def download_toolkit(url=None, target_dir=None):
    r"""Downloads the latest Inetserver toolkit from GitHub.

    Example for updating the Inetserver toolkit for your topology with the latest toolkit from GitHub::

        import streamsx.endpoint as endpoint
        # download toolkit from GitHub
        toolkit_location = endpoint.download_toolkit()
        # add the toolkit to topology
        streamsx.spl.toolkit.add_toolkit(topology, toolkit_location)

    Example for updating the topology with a specific version of the toolkit using a URL::

        import streamsx.endpoint as endpoint
        url410 = 'https://github.com/IBMStreams/streamsx.inetserver/releases/download/v4.1.0/streamsx.inetserver-4.1.0-9c07b97-20190905-1147.tgz'
        toolkit_location = endpoint.download_toolkit(url=url410)
        streamsx.spl.toolkit.add_toolkit(topology, toolkit_location)

    Args:
        url(str): Link to toolkit archive (\*.tgz) to be downloaded. Use this parameter to 
            download a specific version of the toolkit.
        target_dir(str): the directory where the toolkit is unpacked to. If a relative path is given,
            the path is appended to the system temporary directory, for example to /tmp on Unix/Linux systems.
            If target_dir is ``None`` a location relative to the system temporary directory is chosen.

    Returns:
        str: the location of the downloaded toolkit

    .. note:: This function requires an outgoing Internet connection
    """
    _toolkit_location = streamsx.toolkits.download_toolkit (toolkit_name=_TOOLKIT_NAME, url=url, target_dir=target_dir)
    return _toolkit_location


def json_injection(topology, port=0, name=None):
    """Receives HTTP POST requests.

    Args:
        topology: The Streams topology.
        port: Port number for the embedded Jetty HTTP server. If the port is set to 0, the jetty server uses a free tcp port, and the metric serverPort delivers the actual value. 
        name(str): Source name in the Streams context, defaults to a generated name.

    Returns:
        Output Stream with schema: CommonSchema.Json.
    """
    _op = _HTTPJSONInjection(topology, port=port, schema=CommonSchema.Json, name=name)
    return _op.outputs[0]


class _HTTPJSONInjection(streamsx.spl.op.Source):

    def __init__(self, topology, schema=None, certificateAlias=None, context=None, contextResourceBase=None, keyPassword=None, keyStore=None, keyStorePassword=None, port=None, trustStore=None, trustStorePassword=None, vmArg=None, name=None):
        topology = topology
        kind="com.ibm.streamsx.inet.rest::HTTPJSONInjection"
#        topology
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if certificateAlias is not None:
            params['certificateAlias'] = certificateAlias 
        if context is not None:
            params['context'] = context
        if contextResourceBase is not None:
            params['contextResourceBase'] = contextResourceBase
        if keyPassword is not None:
            params['keyPassword'] = keyPassword
        if keyStore is not None:
            params['keyStore'] = keyStore
        if keyStorePassword is not None:
            params['keyStorePassword'] = keyStorePassword
        if port is not None:
            params['port'] = port
        if trustStore is not None:
            params['trustStore'] = trustStore
        if trustStorePassword is not None:
            params['trustStorePassword'] = trustStorePassword

        super(_HTTPJSONInjection, self).__init__(topology,kind,schema,params,name)
