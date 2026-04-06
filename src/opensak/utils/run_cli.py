"""
src/opensak/utils/run_cli.py — Dynamic entry point loader for the main CLI application.

Locates and executes the root run.py script using low-level importlib utilities.
Exposes the main execution function to ensure consistent repository-wide access.
"""

from pathlib import Path
import importlib.util

repo_root = Path(__file__).parents[3].resolve()
run_path = repo_root / "run.py"

spec = importlib.util.spec_from_file_location("run", run_path)
run_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_module)

main = run_module.main