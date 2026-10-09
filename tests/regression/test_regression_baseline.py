import os
import importlib.util


def test_regression_baseline():
    """Full regression baseline (tests/regression/golden.npz). Any difference is a regression unless a fix
    intentionally changes those keys - then regenerate with: python tests/regression/baseline.py generate"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baseline.py")
    spec = importlib.util.spec_from_file_location("debyetools_regression_baseline", path)
    mod = importlib.util.module_from_spec(spec)
    cwd = os.getcwd()
    try:
        spec.loader.exec_module(mod)
        assert mod.run_check() == 0
    finally:
        os.chdir(cwd)
