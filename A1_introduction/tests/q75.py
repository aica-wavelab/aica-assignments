from otter.test_files import test_case

OK_FORMAT = False

name = "q75"
points = None

@test_case(points=None, hidden=False)
def test_largest(env):
    assert 'largest' in env, 'The function largest is not defined!'
    assert env['largest']([-1]) == -1
    assert env['largest']([100, 200, 300, -300]) == 300

