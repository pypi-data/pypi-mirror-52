from functools import wraps
import inspect

from django_injector.scope import RequestScope, request_scope

from django.apps import apps as django_apps
from injector import inject as inject_


__version__ = '0.1.1'
__all__ = ['RequestScope', 'request_scope', 'inject']
default_app_config = 'django_injector.apps.DjangoInjectorConfig'


def inject(func):
    """Prepare a function or merhod for dependency injection.

    This decorator is used to mark functions and methods as injectable. The target
    can still receive non injected arguments. The order of arguments is important,
    all **non** injectable arguments should be listed first. All the injected arguments
    should have appropirate type annotations.

    >>> @inject
    >>> def my_view(request, some_instance: SomeClass, **kwargs):
    >>>     ...
    """
    signature = inspect.signature(func)
    is_method = 'self' in signature.parameters  # There must be a better way to do this

    func = inject_(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        injector = django_apps.get_app_config('django_injector').injector

        if is_method:
            self_, *args = args
        else:
            self_ = None

        return injector.call_with_injection(func, self_=self_, args=tuple(args), kwargs=kwargs)

    return wrapper
