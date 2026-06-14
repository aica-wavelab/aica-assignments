from otter.test_files import test_case

OK_FORMAT = False

name = "q292"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_n_trainable_lora_positive(env):
    assert 'n_trainable_lora' in env, 'n_trainable_lora is not defined'
    assert env['n_trainable_lora'] > 0, \
        'No trainable parameters found — did you call inject_lora?'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_n_trainable_lora_small(env):
    model = env['model_lora']
    n_tot   = sum(p.numel() for p in model.parameters())
    n_train = sum(p.numel() for p in model.parameters() if p.requires_grad)
    assert n_train < n_tot, \
        'All parameters are trainable — did inject_lora freeze the pre-trained weights?'
    assert n_train < 0.3 * n_tot, (
        f'Expected < 30% trainable params, got {100*n_train/n_tot:.1f}%. '
        'Check that only LoRA matrices (lora_A, lora_B) are trainable.'
    )

