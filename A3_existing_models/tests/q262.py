from otter.test_files import test_case

OK_FORMAT = False

name = "q262"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_sim_pair_1(env):
    assert 'sim_pair_1' in env, 'variable sim_pair_1 is not defined'
    assert -1.0 <= env['sim_pair_1'] <= 1.0, 'cosine similarity must be in [-1, 1]'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_sim_pair_2(env):
    assert 'sim_pair_2' in env, 'variable sim_pair_2 is not defined'
    assert -1.0 <= env['sim_pair_2'] <= 1.0, 'cosine similarity must be in [-1, 1]'

