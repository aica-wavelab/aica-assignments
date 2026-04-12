from otter.test_files import test_case

OK_FORMAT = False

name = "q101"
points = None

@test_case(points=None, hidden=False)
def test_nrows(env):
    assert 'nrows' in env, 'The variable nrows is not defined!'
    assert env['nrows'] == 15091, 'The variable nrows has the wrong value!'

@test_case(points=None, hidden=False)
def test_ncols(env):
    assert 'ncols' in env, 'The variable ncols is not defined!'
    assert env['ncols'] == 6, 'The variable ncols has the wrong value!'

