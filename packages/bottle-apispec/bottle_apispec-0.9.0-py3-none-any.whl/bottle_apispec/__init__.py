import importlib
import inspect
import pkgutil

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema

try:
    from apispec_webframeworks.bottle import BottlePlugin
except ImportError:
    from apispec.ext.bottle import BottlePlugin

IGNORED_TYPES = ['Schema']


def disable_swagger(callback):
    """
    Decorator for removing endpoint from OpenAPI Swagger JSON
    """
    callback.enable_swagger = False
    return callback


class APISpecPlugin(object):
    """
    Bottle APISpec Plugin

    Used for automagically generating OpenAPI Swagger schema based on Marshmallow models
    """
    name = 'apispec'
    api = 2

    def __init__(self, path='/schema.json', scan_package=None, *args, **kwargs):
        default_plugins = [BottlePlugin()]
        if scan_package:
            default_plugins.append(MarshmallowPlugin())
        kwargs['plugins'] = kwargs.get('plugins', ()) + tuple(default_plugins)
        self.apispec = APISpec(*args, **kwargs)
        self.apispec_path = self.apispec.add_path if hasattr(self.apispec, 'add_path') else self.apispec.path
        self.apispec_schema = self.apispec.definition if hasattr(self.apispec, 'definition') else self.apispec.components.schema
        self.scan_package = scan_package
        self.path = path

    def setup(self, app):
        if not app.routes:
            raise Exception('No routes found. Please be sure to install APISpecPlugin after declaring *all* your routes!')

        if self.scan_package:
            self._scan_marshmallow_models(self.scan_package)

        for route in app.routes:
            if hasattr(route.callback, 'enable_swagger') and not route.callback.enable_swagger:
                continue
            self.apispec_path(view=route.callback, app=app)

        @app.get(self.path)
        def schema():
            return self.apispec.to_dict()

    def apply(self, callback, route):
        return callback

    def _scan_marshmallow_models(self, base_package):
        base_module = importlib.import_module(base_package)
        if '__path__' in dir(base_module):  # package
            for _, name, _ in pkgutil.iter_modules(base_module.__path__):
                self._scan_marshmallow_models('%s.%s' % (base_package, name))
        else:  # module
            for name, obj in inspect.getmembers(base_module):
                if name not in IGNORED_TYPES and inspect.isclass(obj) and issubclass(obj, Schema):
                    try:
                        self.apispec_schema(name, schema=obj)
                    except:
                        pass
