from otter.test_files import test_case

OK_FORMAT = False

name = "q13"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_my_score(env):
  m21 = env['m21']
  assert 'my_score' in env, 'variable my_score is not initialized'
  score = env['my_score']
  assert isinstance(score, m21.stream.Score), 'my_score is not of type Score'
  all_elements = [e for e in score.recurse()]
  assert isinstance(all_elements[0], m21.stream.Part), 'Your Score does not consist of a Part'
  notes_and_rests = [e for e in score.recurse().notesAndRests]
  assert all([isinstance(e, (m21.note.Note, m21.note.Rest)) for e in notes_and_rests]), 'Not all elements of your part are Notes or Rests'

