import importlib.util, os

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "views", "04_Biomass_Burning.py"))
spec = importlib.util.spec_from_file_location("biomass_burning", module_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
if hasattr(mod, "render"):
    mod.render()
