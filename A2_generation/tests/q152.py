from otter.test_files import test_case

OK_FORMAT = False

name = "q152"
points = None

@test_case(points=None, hidden=False)
def test_W(env):
    assert 'W' in env, 'The variable W is not defined!'
    assert env['W'].shape[0] == 2, f'wrong shape {env["W"].shape[0]} should be 2.'
    assert env['W'].dtype == env['torch'].float32, f'wrong data type for {env["W"]} it should be should {env["torch"].float32}.'

