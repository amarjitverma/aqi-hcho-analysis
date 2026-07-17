import importlib.util, os

# Resolve path to the corresponding view module
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "views", "02_Map_View.py"))
spec = importlib.util.spec_from_file_location("map_view", module_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
# Execute the page's render function
if hasattr(mod, "render"):
    mod.render()
