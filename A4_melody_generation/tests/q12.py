from otter.test_files import test_case

OK_FORMAT = False

name = "q12"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_chromatic_stream(env):
  m21 = env['m21']
  assert 'chromatic_stream' in env, 'variable chromatic_stream is not initialized'
  pitch_classes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
  pitch_classes.reverse()
  for note in env['chromatic_stream']:
    expected = pitch_classes.pop()
    n = m21.note.Note(expected)
    assert abs((note.pitch.midi%12) - (n.pitch.midi%12)) < 0.01, f'{note.name} is not equal to {expected}'

    
