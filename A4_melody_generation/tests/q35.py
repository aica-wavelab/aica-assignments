from otter.test_files import test_case

OK_FORMAT = False

name = "q35"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_piano_rolls(env):
  assert 'streams_folk_songs' in env, 'variable streams_folk_songs is not initialized'
  assert 'piano_rolls' in env, 'variable piano_rolls is not initialized'
  assert 'time_step' in env, 'variable time_step is not initialized'
  piano_roll_encoder = env['PianoRollEncoder'](time_step=env['time_step'])
  expected_piana_rolls, _ = piano_roll_encoder.encode_streams(env['streams_folk_songs'])
  assert len(expected_piana_rolls) == len(env['piano_rolls']), f'expected length of piano_rolls is incorrect.'
  for i in range(len(expected_piana_rolls)):
    roll = env['piano_rolls'][i]
    expected_roll = expected_piana_rolls[i]
    assert len(roll) == len(expected_roll), f'the length of the {i}-th piano roll is incorrect.'
    for j in range(len(expected_roll)):
      assert roll[j] == expected_roll[j], f'{j}-th symbol of the {i}-th roll is incorrect.'
    
@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_enc_piano_rolls(env):
  assert 'streams_folk_songs' in env, 'variable streams_folk_songs is not initialized'
  assert 'piano_rolls' in env, 'variable piano_rolls is not initialized'
  assert 'time_step' in env, 'variable time_step is not initialized'
  assert 'enc_piano_rolls' in env, 'variable enc_piano_rolls is not initialized'
  piano_roll_encoder = env['PianoRollEncoder'](time_step=env['time_step']) 
  expected_piana_rolls, _ = piano_roll_encoder.encode_streams(env['streams_folk_songs'])
  stoi_encoder = env['StringToIntEncoder'](expected_piana_rolls)
  expected_enc_piana_rolls = stoi_encoder.encode_sequences(expected_piana_rolls)

  assert len(expected_enc_piana_rolls) == len(env['enc_piano_rolls']), f'expected length of enc_piano_rolls is incorrect.'
  for i in range(len(expected_enc_piana_rolls)):
    roll = env['enc_piano_rolls'][i]
    expected_roll = expected_enc_piana_rolls[i]
    assert len(roll) == len(expected_roll), f'the length of the {i}-th encoded piano roll is incorrect.'
    for j in range(len(expected_roll)):
      assert roll[j] == expected_roll[j], f'{j}-th symbol of {i}-th encoded roll is incorrect.'
    
