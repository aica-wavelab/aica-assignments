from otter.test_files import test_case

OK_FORMAT = False

name = "q24"
points = None

@test_case(points=None, hidden=False)
def test_list_numbers(env):
    assert 'numbers' in env, 'The variable numbers is not defined!'
    assert type(env['numbers']) == list, 'The variable numbers has the wrong type!'
    assert env['numbers'] == [0, 1, 2, 3, 4, 5], 'The varible numbers holds the wrong value!'

