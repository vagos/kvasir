from . import hooks
from . import program
import importlib
import pluggy
import pkgutil

def load_plugins():
    pm = pluggy.PluginManager("kvasir")
    pm.add_hookspecs(hooks)
    from kvasir import default_plugins

    for _, name, ispkg in pkgutil.iter_modules(default_plugins.__path__):
        if ispkg: continue
        module_name = f"kvasir.default_plugins.{name}"
        module = importlib.import_module(module_name)
        pm.register(module)

    # Load external plugins
    pm.load_setuptools_entrypoints("kvasir")

    # Register program subclasses from plugins
    for impl in pm.hook.language_support():
        assert impl, "Plugin must return a program subclass"
        lang = impl.language
        program.ProgramMeta.registry[lang] = impl

    return pm.get_plugins()
