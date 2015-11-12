`pyramid_subscribers_beaker_https_session` allows you to add a https-only session based cookie to your application.

To configure:
=============

1. As of the initial release it mimics the code in pyramid_beaker, with two changes:

* The prefix must either be `session_https` or `beaker_session_https`
* This package forces `secure` to be `True`


2. In your app/__init__.py main:

	import pyramid_subscribers_beaker_https_session

	## initialize https session
    pyramid_subscribers_beaker_https_session.initialize_https_session_support(config, settings)


3. You will now have a `session_https` attribute on your `request` objects

support for https awareness
===========================

default values are `true`.  They can be set to `false`

*	session_https.ensure_scheme = true
*	beaker_session_https.ensure_scheme = true

If `request.scheme` is not "https", then `session_https` will be `None`.

`request.scheme` can be supported for backend proxies via paste deploy's prefix middleware:

Add this to your environment.ini's [app:main]

	filter-with = proxy-prefix

Then add this section

	[filter:proxy-prefix]
	use = egg:PasteDeploy#prefix


requirements
============

this package (obviously) requires pyramid and beaker

As of v 0.1.0, this package requires `pyramid_https_session_core`


license
=======

Large sections of this code were based on pyramid_beaker, which is released under
the `repoze license`.
