import importlib
import pkgutil

import pluggy

from . import hooks, program


def load_plugins():
    pm = pluggy.PluginManager("kvasir")
    pm.add_hookspecs(hooks)
    from kvasir import default_plugins

    for _, name, ispkg in pkgutil.iter_modules(default_plugins.__path__):
        if ispkg:
            continue
        module_name = f"kvasir.default_plugins.{name}"
        module = importlib.import_module(module_name)
        pm.register(module)

    # Load external plugins
    pm.load_setuptools_entrypoints("kvasir")

    return pm.get_plugins()
