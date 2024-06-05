from otter.test_files import test_case

OK_FORMAT = False

name = "q1"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_c5_frequency(env):
  m21 = env['m21']
  assert 'c5_frequency' in env, 'variable c5_frequency is not initialized'
  assert abs(env['c5_frequency'] - m21.note.Note(nameWithOctave='C5').pitch.frequency) < 0.01, 'wrong value for c5_frequency'
    
@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_c6_frequency(env):
  m21 = env['m21']
  assert 'c6_frequency' in env, 'variable c6_frequency is not initialized'
  assert abs(env['c6_frequency'] - m21.note.Note(nameWithOctave='C6').pitch.frequency) < 0.01, 'wrong value for c6_frequency'
    
@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_ratio(env):
  assert 'ratio' in env, 'variable ratio is not initialized'
  assert abs(env['ratio']-2.0) < 0.01, 'wrong value for ratio'
    
