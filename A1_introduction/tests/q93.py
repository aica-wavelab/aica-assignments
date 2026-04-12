from otter.test_files import test_case

OK_FORMAT = False

name = "q93"
points = None

@test_case(points=None, hidden=False)
def test_range_price(env):
    np = env['np']
    assert 'price_range' in env, 'The variable price_range is not defined!'
    assert type(env['price_range']) == np.int32 or type(env['price_range']) == np.int64, 'The variable price_range has the wrong data type'
    assert env['price_range'] == 9750, 'The variable price_range has the wrong value'

