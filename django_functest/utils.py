from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY as AUTH_BACKEND_SESSION_KEY
from django.contrib.auth import HASH_SESSION_KEY as AUTH_HASH_SESSION_KEY
from django.contrib.auth import SESSION_KEY as AUTH_ID_SESSION_KEY
from django.contrib.auth import authenticate
from furl import furl

try:
    from importlib import import_module
except:
    from django.utils.importlib import import_module


class ShortcutLoginMixin(object):
    def shortcut_login(self, **credentials):
        user = authenticate(**credentials)
        if not user:
            raise ValueError("User {0} was not authenticated".format(user))

        session_auth_hash = ''
        if hasattr(user, 'get_session_auth_hash'):
            session_auth_hash = user.get_session_auth_hash()

        # Mimicking django.contrib.auth functionality
        self.set_session_vars({AUTH_ID_SESSION_KEY: user.pk,
                               AUTH_HASH_SESSION_KEY: session_auth_hash,
                               AUTH_BACKEND_SESSION_KEY: user.backend})


def get_session_store(session_key=None):
    engine = import_module(settings.SESSION_ENGINE)
    # Implement a database session store object that will contain the session key.
    store = engine.SessionStore(session_key=session_key)
    if session_key is None:
        store.save()
    else:
        store.load()
    return store


class CommonMixin(object):

    def assertUrlsEqual(self, url, other_url=None):
        """
        Asserts that the URLs match. Empty protocol or domain are ignored.
        """
        if other_url is None:
            other_url = self.current_url
        url1 = furl(url)
        url2 = furl(other_url)
        self.assertEqual(url1.path, url2.path)
        self.assertEqual(url1.query, url2.query)
        if url1.netloc and url2.netloc:
            self.assertEqual(url1.netloc, url2.netloc)
        if url1.scheme and url2.scheme:
            self.assertEqual(url1.scheme, url2.scheme)