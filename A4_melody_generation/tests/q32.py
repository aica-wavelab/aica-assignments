from otter.test_files import test_case

OK_FORMAT = False

name = "q32"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_stream_has_acceptable_duration_fails(env):
  assert 'stream' in env, 'variable stream is not initialized'
  assert env['has_acceptable_duration'](env['stream'], time_step=1.0) == False, f'{env['stream']} is has acceptable durations for time_step = 1.0'
    
@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_stream_has_acceptable_duration_success(env):
  assert 'stream' in env, 'variable stream is not initialized'
  assert env['has_acceptable_duration'](env['stream'], time_step=0.5) == True, f'{env['stream']} is has durations not acceptable for time_step = 0.5'
    
