from django.conf import settings
from django.contrib.auth.models import AnonymousUser

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

USER_ATTR_NAME = '_current_user'


def _do_set_current_user(user_fun):
    setattr(_thread_locals, USER_ATTR_NAME, user_fun.__get__(user_fun, local))


class ThreadLocalUserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request.user closure; asserts laziness;
        # memorization is implemented in
        # request.user (non-data descriptor)
        _do_set_current_user(lambda self: getattr(request, 'user', None))
        response = self.get_response(request)
        return response

def get_current_user():
    current_user = getattr(_thread_locals, USER_ATTR_NAME, None)
    if callable(current_user):
        return current_user()
    return current_user


def get_current_authenticated_user():
    current_user = get_current_user()
    if isinstance(current_user, AnonymousUser):
        return None
    return current_user

