from otter.test_files import test_case

OK_FORMAT = False

name = "q21"
points = None

@test_case(points=None, hidden=False)
def test_z(env):
    assert 'z' in env, 'The variable z is not defined!'
    assert type(env['z']) == int, 'The variable z has the wrong type!'
    assert env['z'] == 5, 'The varible z holds the wrong value!'

