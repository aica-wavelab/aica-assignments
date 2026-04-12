from otter.test_files import test_case

OK_FORMAT = False

name = "q133"
points = None

@test_case(points=None, hidden=False)
def test_n_old_districts(env):
    assert 'n_old_districts' in env, 'The variable n_old_districts is not defined!'
    assert env['n_old_districts'] == 9495, 'Variable n_old_districts has the wrong value.'

