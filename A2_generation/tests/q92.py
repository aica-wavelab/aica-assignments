from otter.test_files import test_case

OK_FORMAT = False

name = "q92"
points = None

@test_case(points=None, hidden=False)
def test_min_price(env):
    np = env['np']
    assert 'price_min' in env, 'The variable price_min is not defined!'
    assert type(env['price_min']) == int or type(env['price_min']) == np.int32 or type(env['price_min']) == np.int64, 'The variable price_min has the wrong data type'
    assert env['price_min'] == 250, 'The variable price_min has the wrong value'

@test_case(points=None, hidden=False)
def test_max_price(env):
    np = env['np']
    assert 'price_max' in env, 'The variable price_max is not defined!'
    assert type(env['price_max']) == int or type(env['price_max']) == np.int32 or type(env['price_max']) == np.int64, 'The variable price_max has the wrong data type'
    assert env['price_max'] == 10000, 'The variable price_max has the wrong value'

