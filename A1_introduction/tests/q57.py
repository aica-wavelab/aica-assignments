from otter.test_files import test_case

OK_FORMAT = False

name = "q57"
points = None

@test_case(points=None, hidden=False)
def test_transpose(env):
    assert 'transpose' in env, 'The function transpose is not defined!'
    assert env['transpose']([], 5) == [], f'transpose([], 5) should return [], but got {env["transpose"]([], 5)}.'
    assert env['transpose'](['C'], 0) == ['C'], f'transpose(["C"], 0) should return ["C"], but got {env["transpose"](["C"], 0)}.'
    assert env['transpose'](['C'], 1) == ['C#'], f'transpose(["C"], 1) should return ["C#"], but got {env["transpose"](["C"], 1)}.'
    assert env['transpose'](['C'], 11) == ['B'], f'transpose(["C"], 11) should return ["B"], but got {env["transpose"](["C"], 11)}.'
    assert env['transpose'](['C'], 12) == ['C'], f'transpose(["C"], 12) should return ["C"] (full octave), but got {env["transpose"](["C"], 12)}.'
    assert env['transpose'](['C'], 14) == ['D'], f'transpose(["C"], 14) should return ["D"], but got {env["transpose"](["C"], 14)}.'
    assert env['transpose'](['C'], -12) == ['C'], f'transpose(["C"], -12) should return ["C"] (full octave down), but got {env["transpose"](["C"], -12)}.'
    assert env['transpose'](['C'], -1) == ['B'], f'transpose(["C"], -1) should return ["B"], but got {env["transpose"](["C"], -1)}.'
    assert env['transpose'](['C', 'B', 'D#'], 0) == ['C', 'B', 'D#'], f'transpose(["C","B","D#"], 0) should return ["C","B","D#"], but got {env["transpose"](["C","B","D#"], 0)}.'
    assert env['transpose'](['C', 'B', 'D#'], 5) == ['F', 'E', 'G#'], f'transpose(["C","B","D#"], 5) should return ["F","E","G#"], but got {env["transpose"](["C","B","D#"], 5)}.'

