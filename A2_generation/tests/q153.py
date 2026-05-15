from otter.test_files import test_case

OK_FORMAT = False

name = "q153"
points = None

@test_case(points=None, hidden=False)
def test_S(env):
    assert 'S' in env, 'The variable S is not defined!'
    assert env['S'].shape == (2,2), f'wrong shape {env["S"].shape} should be (2,2).'
    assert env['S'].dtype == env['torch'].float32, f'wrong data type for {env["S"]} it should be should {env["torch"].float32}.'
    assert env['torch'].equal(env['torch'].tensor([[0, 1],[1, 0]], dtype=env['torch'].float32), env['S']), f'wrong tensor.'

