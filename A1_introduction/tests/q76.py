from otter.test_files import test_case

OK_FORMAT = False

name = "q76"
points = None

@test_case(points=None, hidden=False)
def test_transpose(env):
    assert 'transpose' in env, 'The function transpose is not defined!'
    assert env['transpose'](['C'], 0) == ['C'], 'transposing C by 0 should be equal to C'
    assert env['transpose'](['C'], 1) == ['C#'], 'transposing C by 1 should be equal to C#'
    assert env['transpose'](['C'], 11) == ['B'], 'transposing C by 11 should be equal to B'
    assert env['transpose'](['C'], 12) == ['C'], 'transposing C by 12 should be equal to C'
    assert env['transpose'](['C'], 14) == ['D'], 'transposing C by 14 should be equal to D'
    assert env['transpose'](['C'], -12) == ['C'], 'transposing C by -12 should be equal to C'
    assert env['transpose'](['C'], -1) == ['B'], 'transposing C by -1 should be equal to B'
    assert env['transpose'](['C', 'B', 'D#'], 0) == ['C', 'B', 'D#'], 'transposing C,B,D# by 0 should be equal to C,B,D#'
    assert env['transpose'](['C', 'B', 'D#'], 5) == ['F', 'E', 'G#'], 'transposing C,B,D# by 5 should be equal to F,E,G#'

