"""
This was the original code I used to monkeypatch supoprt in
"""

import pyramid
from pyramid_beaker import BeakerSessionFactoryConfig
from beaker.util import coerce_session_params
from pyramid.interfaces import ISessionFactory
from pyramid.decorator import reify
from pyramid.settings import asbool


class ISessionHttpsFactory(ISessionFactory):
    pass


def main(global_config, **settings):

    https_options = {}
    https_prefixes = ("session_https.", "beaker.session_https.")
    for k, v in settings.items():
        for prefix in https_prefixes:
            if k.startswith(prefix):
                option_name = k[len(prefix) :]
                if option_name == "cookie_on_exception":
                    v = asbool(v)
                https_options[option_name] = v

    # setting this true should work...
    https_options["secure"] = True

    https_options = coerce_session_params(https_options)
    https_session_factory = config.maybe_dotted(
        BeakerSessionFactoryConfig(**https_options)
    )

    def register_session_https_factory():
        config.registry.registerUtility(https_session_factory, ISessionHttpsFactory)

    intr = config.introspectable(
        "session https factory",
        None,
        config.object_description(https_session_factory),
        "session https factory",
    )
    intr["factory"] = https_session_factory
    config.action(
        ISessionHttpsFactory, register_session_https_factory, introspectables=(intr,)
    )

    @reify
    def session_https(self):
        """Obtain the :term:`session_https` object associated with this
        request.  If a :term:`session_https factory` has not been registered
        during application configuration, a
        :class:`pyramid.exceptions.ConfigurationError` will be raised"""
        factory = self.registry.queryUtility(ISessionHttpsFactory)
        if factory is None:
            raise AttributeError("No session_https factory registered ")
        return factory(self)

    pyramid.request.Request.session_https = session_https
