# The default settings which the agent will use
# can be overridden with environment variables:
# E.g.
# HIPPO_KEY=value
# or via the agent arguments,
# E.g.
# nerd_vision.start("api_key", settings={'HIPPO_KEY':'value'})
# ----------------------------------------------------------------------------
import os

nv_settings = {
    # The default instance name
    'name': os.environ.get("NV_NAME") or None,

    # Defines user tags as comma separated key values.  E.g. tags=abc=123,xyz=567
    'tags': None,

    # ----------------------------------------------------------------------------
    # Defines the license key to use and api locations
    'api_url': os.environ.get("NV_API_URL") or "https://api.nerd.vision",
    'api_key': os.environ.get("NV_API_KEY") or None,

    'license_url': os.environ.get("NV_LICENSE_URL") or None,
    'license_api': os.environ.get("NV_LICENSE_API") or "/licensing-api/agent",

    # Defines the grpc url. defaults to api.url
    'grpc_url': os.environ.get("NV_GRPC_URL") or None,
    # Define the grpc port number
    'grpc_port': os.environ.get("NV_GRPC_PORT") or 443,
    # Define the grpc reconnect attempt intervals
    'grpc_backoff_max': os.environ.get("NV_GRPC_BACKOFF_MAX") or 120,
    'grpc_backoff_multiplier': os.environ.get("NV_GRPC_BACKOFF_MULTIPLIER") or 1.2,

    'client_registration_backoff_max': os.environ.get("NV_CLIENT_REGISTRATION_BACKOFF_MAX") or 120,
    'client_registration_backoff_multiplier': os.environ.get("NV_CLIENT_REGISTRATION_BACKOFF_MULTIPLIER") or 1.2,

    # The end point for the event snapshot
    'event_snapshot_api': os.environ.get("NV_EVENT_SNAPSHOT_API") or "/context/v2/eventsnapshot",
    'event_snapshot_url': os.environ.get("NV_EVENT_SNAPSHOT_URL") or None,

    # ----------------------------------------------------------------------------
    # Defines the regex for the ENV section of the client registration step.
    'env_regex': os.environ.get("NV_ENV_REGEX") or "(?i).*sudo.*|.*pass.*",
    'env_max_str_length': os.environ.get("NV_ENV_MAX_STR_LENGTH") or 1024,

    # ----------------------------------------------------------------------------
    # Defines the regex for the network name filters
    'network_interface_regex': os.environ.get("NV_NETWORK_INTERFACE_FILTER") or '(?i).*docker.*|lo|veth.*|br-.*|tun.*',

    # ----------------------------------------------------------------------------
    # Defines the configurations for logging
    'log_file': os.environ.get("NV_LOG_FILE") or 'nerd_vision.log',
    'log_level': os.environ.get('NV_LOG_LEVEL') or 'INFO',

    # ----------------------------------------------------------------------------
    # Allows more control over debug logging
    'debug.all': False,
    'point.cut.debug': False,
    'context.debug': False,
    'client_reg.debug': False,
    'grpc.debug': False
}


def configure_agent(values=None):
    if values is None:
        return
    for key in values.keys():
        nv_settings[key] = values[key]


def get_setting(key):
    return nv_settings[key]


def get_context_url():
    url = (nv_settings['event_snapshot_url'] or nv_settings['api_url'])
    return url + nv_settings['event_snapshot_api']


def get_license_url():
    url = (nv_settings['license_url'] or nv_settings['api_url'])
    return url + nv_settings['license_api']


def get_grpc_host():
    if nv_settings['grpc_url'] is not None:
        url = truncate_url(nv_settings['grpc_url'])
    else:
        url = truncate_url(nv_settings['api_url'])
    return url + ':' + str(nv_settings['grpc_port'])


def is_point_cut_debug_enabled():
    if nv_settings.get('debug.all'):
        return True
    return nv_settings.get('point.cut.debug')


def is_context_debug_enabled():
    if nv_settings.get('debug.all'):
        return True
    return nv_settings.get('context.debug')


def is_grpc_debug_enabled():
    if nv_settings.get('debug.all'):
        return True
    return nv_settings.get('grpc.debug')


def is_client_reg_debug():
    if nv_settings.get('debug.all'):
        return True
    return nv_settings.get("client_reg.debug")


def truncate_url(url):
    host = url.split('://')[0]
    if host == 'https':
        return url[8:]
    else:
        return url[7:]
