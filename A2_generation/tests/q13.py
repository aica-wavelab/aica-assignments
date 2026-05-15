from otter.test_files import test_case

OK_FORMAT = False

name = "q13"
points = None

@test_case(points=None, hidden=False)
def test_total_paintings(env):
    assert 'total_paintings' in env, 'The variable total_paintings is not defined!'
    assert env['total_paintings'] == 3 * 12 * 8, f'Expected {3 * 12 * 8}, got {env["total_paintings"]}.'

