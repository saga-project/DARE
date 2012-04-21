"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""

from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html.tags import *
from webhelpers.html import literal
from webhelpers import paginate

#from webhelpers.pylonslib.flash import Flash as _Flash
#flash = _Flash()

class Flash(object):
    def __call__(self, message):
        session = self._get_session()
        session["flash"] = message
        session.save()

    def pop_message(self):
        session = self._get_session()
        message = session.pop("flash", None)
        if not message:
            return None
        session.save()
        return message

    def _get_session(self):
        from pylons import session
        return session

flash = Flash()


# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
