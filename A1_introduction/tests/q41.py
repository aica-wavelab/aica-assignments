from otter.test_files import test_case

OK_FORMAT = False

name = "q41"
points = None

@test_case(points=None, hidden=False)
def test_find_name_index(env):
    assert 'find_name_index' in env, 'The function find_name_index is not defined!'
    assert env['find_name_index'](['A', 'B', 'C'], 'D') == -1, 'If the name is not in the list the function should return -1'
    assert env['find_name_index'](['A', 'B', 'C'], 'B') == 1, 'Wrong index for existing name in the list'
    assert env['find_name_index']([], '') == -1, 'Empty name should always return -1'

