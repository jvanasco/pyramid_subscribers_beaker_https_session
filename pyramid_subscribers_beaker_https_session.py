from pyramid_beaker import BeakerSessionFactoryConfig
from beaker.util import coerce_session_params
from pyramid.interfaces import ISessionFactory 
from pyramid.settings import asbool
from zope.interface import ( Attribute )


class ISessionHttpsFactory(ISessionFactory):
    """subclass of ISessionFactory; needs to be unique class"""
    pass

class NotHttpsRequest(Exception):
    """Raised when we're not an HTTPS request, and the application is configured to ensure_scheme"""
    pass


def _initialize_settings_and_factory( config, settings ):
    """Parses config settings, registers ISessionHttpsFactory with Pyramid"""
    https_options = {}
    https_prefixes = ('session_https.', 'beaker.session_https.')
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
    config.registry.settings['pyramid_subscribers_beaker_https_session.ensure_scheme']= ensure_scheme

    # force secure...
    https_options['secure'] = True
    https_options = coerce_session_params(https_options)
    https_session_factory = config.maybe_dotted( BeakerSessionFactoryConfig(**https_options) )

    #push the ensure_scheme onto the factory...
    https_session_factory.ensure_scheme = ensure_scheme

    def register_session_https_factory():
        config.registry.registerUtility(https_session_factory, ISessionHttpsFactory)

    intr = config.introspectable( 'session https factory', \
            None,
            config.object_description(https_session_factory),
            'session https factory'
        )
    intr['factory'] = https_session_factory
    config.action(ISessionHttpsFactory, register_session_https_factory, introspectables=(intr,))


def _subscriber_add_https_session(event):
    """Subscriber method - provides the session_https attribute onto a request"""
    factory = event.request.registry.queryUtility(ISessionHttpsFactory)
    if factory is None:
        raise AttributeError(
            'No session_https factory registered '
            )
    if event.request.scheme != 'https':
        return None
    event.request.session_https= factory(event.request)


def initialize_https_session_subscriber( config, settings ):
    """Public method - initializes `session_https` via a subscriber"""
    _initialize_settings_and_factory( config, settings )
    config.add_subscriber(_subscriber_add_https_session, 'pyramid.events.NewRequest')


def _session_https(request):
    """Public method - initializes `session_https` via a subscriber"""
    # are we ensureing https?
    if request.registry.settings['pyramid_subscribers_beaker_https_session.ensure_scheme']:
        if request.scheme != 'https':
            return None
    factory = request.registry.queryUtility(ISessionHttpsFactory)
    if factory is None:
        raise AttributeError(
            'No session_https factory registered '
            )
    return factory(request)

    
def initialize_https_session_set_request_property( config, settings ):
    """Public method - initializes `session_https` via a config.set_request_property"""
    _initialize_settings_and_factory( config, settings )
    config.set_request_property(_session_https, 'session_https', reify=True )    