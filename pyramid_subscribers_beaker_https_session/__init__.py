from pyramid_beaker import BeakerSessionFactoryConfig
from beaker.util import coerce_session_params

from pyramid.settings import asbool

import pyramid_https_session_core


# ==============================================================================


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

    # note if we're going to ensure the https scheme... default to True
    ensure_scheme = True
    if 'ensure_scheme' in https_options:
        ensure_scheme = asbool(https_options['ensure_scheme'])
    config.registry.settings['pyramid_https_session_core.ensure_scheme'] = ensure_scheme

    # force secure...
    https_options['secure'] = True
    https_options = coerce_session_params(https_options)
    https_session_factory = config.maybe_dotted(BeakerSessionFactoryConfig(**https_options))

    # push the ensure_scheme onto the factory...
    https_session_factory.ensure_scheme = ensure_scheme

    # okay!  register our factory
    pyramid_https_session_core.register_https_session_factory(config,
                                                              settings,
                                                              https_session_factory
                                                              )
