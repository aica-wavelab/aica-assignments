from otter.test_files import test_case

OK_FORMAT = False

name = "q11"
points = None

@test_case(points=None, hidden=False)
def test_x(env):
    assert 'x' in env, 'The variable x is not defined!'
    assert env['x'] == 5 - 12, f'x should be {5 - 12}, but got {env["x"]}.'

