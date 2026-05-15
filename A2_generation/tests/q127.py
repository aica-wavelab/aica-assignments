from otter.test_files import test_case

OK_FORMAT = False

name = "q127"
points = None

@test_case(points=None, hidden=False)
def test_last_improvements(env):
    assert abs(env["histor_improved"][-2] - env["histor_improved"][-1]) < 0.001, "your model could be improved!"

