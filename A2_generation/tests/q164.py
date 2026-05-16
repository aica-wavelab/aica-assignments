from otter.test_files import test_case

OK_FORMAT = False

name = "q164"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_xor_network(env):
  X = [(0,0), (0,1), (1,0), (1,1)]
  y = [0, 1, 1, 0]
  assert all(env['xor_network'](x) == y[i] for i, x in enumerate(X)), "incorrect result"

