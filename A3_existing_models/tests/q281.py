from otter.test_files import test_case

OK_FORMAT = False

name = "q281"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_n_trainable_positive(env):
    assert 'n_trainable' in env, 'n_trainable is not defined'
    assert env['n_trainable'] > 0, 'No trainable parameters — did you forget to unfreeze some layers?'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_partial_freeze(env):
    model  = env['model_ft']
    n_tot  = sum(p.numel() for p in model.parameters())
    n_train= sum(p.numel() for p in model.parameters() if p.requires_grad)
    # Partial fine-tuning: trainable params should be strictly less than total
    assert n_train < n_tot, 'All parameters are trainable — did you freeze the early layers?'
    # And more than zero (checked above)
    assert n_train > 0

