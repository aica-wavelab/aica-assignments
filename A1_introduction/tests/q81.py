from otter.test_files import test_case

OK_FORMAT = False

name = "q81"
points = None

@test_case(points=None, hidden=False)
def test_pandas_installed(env):
    import importlib
    assert importlib.util.find_spec('pandas') is not None

