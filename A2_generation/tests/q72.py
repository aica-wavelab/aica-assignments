from otter.test_files import test_case

OK_FORMAT = False

name = "q72"
points = None

@test_case(points=None, hidden=False)
def test_find_name_index(env):
    assert 'find_name_index' in env, 'The function find_name_index is not defined!'
    assert env['find_name_index'](['A', 'B', 'C'], 'A') == 0, f'find_name_index(["A","B","C"], "A") should return 0, but got {env["find_name_index"](["A","B","C"], "A")}.'
    assert env['find_name_index'](['A', 'B', 'C'], 'B') == 1, f'find_name_index(["A","B","C"], "B") should return 1, but got {env["find_name_index"](["A","B","C"], "B")}.'
    assert env['find_name_index'](['A', 'B', 'C'], 'D') == -1, f'find_name_index(["A","B","C"], "D") should return -1 when the name is not in the list, but got {env["find_name_index"](["A","B","C"], "D")}.'
    assert env['find_name_index']([], 'A') == -1, f'find_name_index([], "A") should return -1 for an empty list, but got {env["find_name_index"]([], "A")}.'

