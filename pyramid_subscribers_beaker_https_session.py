from pyramid_beaker import BeakerSessionFactoryConfig
from beaker.util import coerce_session_params
from pyramid.interfaces import ISessionFactory 
from pyramid.settings import asbool

class ISessionHttpsFactory(ISessionFactory):
    pass

def add_https_session(event):
    factory = event.request.registry.queryUtility(ISessionHttpsFactory)
    if factory is None:
        raise AttributeError(
            'No session_https factory registered '
            )
    event.request.session_https= factory(event.request)
    print "add_https_session"

def initialize_https_session( config, settings ):
    """Startup support"""
    https_options = {}
    https_prefixes = ('session_https.', 'beaker.session_https.')
    for k, v in settings.items():
        for prefix in https_prefixes:
            if k.startswith(prefix):
                option_name = k[len(prefix):]
                if option_name == 'cookie_on_exception':
                    v = asbool(v)
                https_options[option_name] = v
    # force secure...
    https_options['secure'] = True
    https_options = coerce_session_params(https_options)
    https_session_factory = config.maybe_dotted( BeakerSessionFactoryConfig(**https_options) )
    def register_session_https_factory():
        config.registry.registerUtility(https_session_factory, ISessionHttpsFactory)
    intr = config.introspectable('session https factory', None,
                               config.object_description(https_session_factory),
                               'session https factory')
    intr['factory'] = https_session_factory
    config.action(ISessionHttpsFactory, register_session_https_factory, introspectables=(intr,))
    config.add_subscriber(add_https_session, 'pyramid.events.NewRequest')