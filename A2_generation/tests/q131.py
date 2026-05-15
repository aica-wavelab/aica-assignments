from otter.test_files import test_case

OK_FORMAT = False

name = "q131"
points = None

@test_case(points=None, hidden=False)
def test_avg_income(env):
    assert 'avg_income' in env, 'The variable avg_income is not defined!'
    assert abs(env['avg_income']-3.8707) < 0.001, 'Variable avg_income has the wrong value.'

@test_case(points=None, hidden=False)
def test_n_samples(env):
    assert 'n_samples' in env, 'The variable n_samples is not defined!'
    assert env['n_samples'] == 20640, 'Variable n_samples has the wrong value.'

