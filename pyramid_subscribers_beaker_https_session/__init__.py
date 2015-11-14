from pyramid.settings import asbool

from pyramid_beaker import BeakerSessionFactoryConfig
from beaker.util import coerce_session_params

import pyramid_https_session_core


# ==============================================================================


class RedisConfigurator(pyramid_https_session_core.SessionBackendConfigurator):

    # used to ensure compatibility
    compatibility_options = {'secure': 'secure',
                             'httponly': 'cookie_httponly',
                             }
    # ensure the backend gets `type`
    allowed_passthrough_options = ('type',
                                   )


def initialize_https_session_support(config, settings):
    """
    Parses config settings, builds a https session factory, registers it
    """
    https_options = {}
    https_prefixes = ('session_https.',
                      'beaker.session_https.',
                      )
    for k, v in settings.items():
        for prefix in https_prefixes:
            if k.startswith(prefix):
                option_name = k[len(prefix):]
                if option_name == 'cookie_on_exception':
                    v = asbool(v)
                https_options[option_name] = v

    # ensure compatibility with our options
    RedisConfigurator.ensure_compatibility(https_options)
    RedisConfigurator.ensure_security(config, https_options)
    RedisConfigurator.cleanup_options(https_options)

    # build a session
    https_options = coerce_session_params(https_options)
    https_session_factory = config.maybe_dotted(BeakerSessionFactoryConfig(**https_options))
    
    # okay!  register our factory
    pyramid_https_session_core.register_https_session_factory(config,
                                                              settings,
                                                              https_session_factory
                                                              )
