import importlib.util, os
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "views", "09_Admin_Panel.py"))
spec = importlib.util.spec_from_file_location("admin_panel", module_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
