from otter.test_files import test_case

OK_FORMAT = False

name = "q1"
points = None

@test_case(points=None, hidden=False)
def test_loss(env):
    assert 'loss' in env, 'loss is not defined.'
    assert 'accuracy' in env, 'accuracy is not defined.'
    assert env['loss'] < 5.0, 'loss should be at least smaller than 5.0'
    assert env['accuracy'] > 0.6, 'accuracy should be at least greater than 0.6'

