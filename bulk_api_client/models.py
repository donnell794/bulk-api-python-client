import re
import sys

from bulk_api_client.env_client import env_client

models = sys.modules[__name__]
__all__ = []


def _snake_to_camel(name):
    return re.sub(r"(?:^|_)([a-z])", lambda x: x.group(1).upper(), name)


class App:
    def __init__(self, app_name):
        self.app = env_client.app(app_name)
        setattr(models, app_name, self)
        __all__.append(app_name)

    def add_model(self, model_name):
        setattr(self, _snake_to_camel(model_name), self.app.model(model_name))


for definition in env_client.definitions.keys():
    app_name, model_name = definition.split(".")
    app = getattr(models, app_name, None)
    if not app:
        app = App(app_name)
    app.add_model(model_name)
