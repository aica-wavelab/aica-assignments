from otter.test_files import test_case

OK_FORMAT = False

name = "q132"
points = None

@test_case(points=None, hidden=False)
def test_min_price(env):
    assert 'min_price' in env, 'The variable min_price is not defined!'
    assert abs(env['min_price']-0.15) < 0.0001, 'Variable min_price has the wrong value.'

@test_case(points=None, hidden=False)
def test_max_price(env):
    assert 'max_price' in env, 'The variable max_price is not defined!'
    assert abs(env['max_price']-5.00) < 0.0001, 'Variable max_price has the wrong value.'

