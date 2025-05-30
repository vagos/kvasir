from . import hooks
import importlib
import pluggy
import pkgutil

def load_plugins():
    pm = pluggy.PluginManager("llm")
    pm.add_hookspecs(hooks)
    from kvasir import default_plugins

    for _, name, ispkg in pkgutil.iter_modules(default_plugins.__path__):
        if ispkg:
            continue
        module_name = f"kvasir.default_plugins.{name}"
        module = importlib.import_module(module_name)
        pm.register(module)

    # 2. Optionally load external plugins via entry points
    try:
        pm.load_setuptools_entrypoints("kvasir_plugins")
    except Exception:
        pass  # Ignore entrypoint loading errors for now

    return pm.get_plugins()
