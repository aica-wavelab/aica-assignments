from otter.test_files import test_case

OK_FORMAT = False

name = "q91"
points = None

@test_case(points=None, hidden=False)
def test_median(env):
    np = env['np']
    assert 'median' in env, 'The variable median is not defined!'
    assert type(env['median']) == np.float64 or type(env['median']) == np.float32
    assert abs(env['median'] - 850.0) < 0.01

