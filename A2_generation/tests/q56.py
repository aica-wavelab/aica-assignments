from otter.test_files import test_case

OK_FORMAT = False

name = "q56"
points = None

@test_case(points=None, hidden=False)
def test_largest(env):
    assert 'largest' in env, 'The function largest is not defined!'
    assert env['largest']([-1]) == -1, f'largest([-1]) should return -1, but got {env["largest"]([-1])}.'
    assert env['largest']([100, 200, 300, -300]) == 300, f'largest([100, 200, 300, -300]) should return 300, but got {env["largest"]([100, 200, 300, -300])}.'
    assert env['largest']([-5, -3, -1]) == -1, f'largest([-5, -3, -1]) should return -1, but got {env["largest"]([-5, -3, -1])}. Make sure you do not initialise your maximum with 0!'
    assert env['largest']([7, 7, 7]) == 7, f'largest([7, 7, 7]) should return 7, but got {env["largest"]([7, 7, 7])}.'

