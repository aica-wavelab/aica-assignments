from otter.test_files import test_case

OK_FORMAT = False

name = "q21"
points = None

@test_case(points=None, hidden=False)
def test_z(env):
    assert 'k' in env, 'The variable z is not defined!'
    assert type(env['k']) == int, f'z should be of type int, but got type {type(env["k"])}.'
    assert env['k'] == 5, f'z should be 5, but got {env["k"]}.'

