from otter.test_files import test_case

OK_FORMAT = False

name = "q126"
points = None

@test_case(points=None, hidden=False)
def test_losses(env):
    assert 'initial_loss' in env, 'The variable initial_loss is not defined!'
    assert 'final_loss' in env, 'The variable final_loss is not defined!'
    assert env['initial_loss'] > env['final_loss'], "final_loss is not smaller than initial_loss"

