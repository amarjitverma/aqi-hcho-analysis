import importlib.util, os
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "views", "08_Data_Sources.py"))
spec = importlib.util.spec_from_file_location("data_sources", module_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
if hasattr(mod, "render"):
    mod.render()
